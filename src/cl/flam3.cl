#pragma once

#define USEFMA 1    // Enable fused multiply-add if desired
#define PSCL 0.001f

// ----------------------------
// Constants
// ----------------------------
enum {
    MAX_XFORMS           = 64, 
    MAX_AFFINE_SIZE      = MAX_XFORMS * 3, 
    MAX_XFORMS_XAOS      = 20, 
    MAX_XFORMS_XAOS_SIZE = MAX_XFORMS_XAOS * MAX_XFORMS_XAOS
};


// ----------------------------
// GPU RNG: Xoroshiro128+
//
// This RNG was originally MWC64X in Fractorium.
// Updated to use Xoroshiro128+ instead for better randomness and longer period.
// It is basically upgrading MWC64X functionality while keeping the same type of helper functions.
// ----------------------------

// ----------------------------
// RNG state per thread
// ----------------------------
typedef struct {
    uint s0;
    uint s1;
    uint s2;
    uint s3;
} x128_state_t;

// ----------------------------
// Rotate left
// ----------------------------
inline uint rotate_left(uint x, int k) {
    return (x << k) | (x >> (32 - k));
}

// ----------------------------
// SplitMix32 for per-thread seeding
// ----------------------------
inline uint splitmix32(uint seed) {
    uint z = seed + 0x9E3779B9u;
    z = (z ^ (z >> 16)) * 0x85EBCA6Bu;
    z = (z ^ (z >> 13)) * 0xC2B2AE35u;
    return z ^ (z >> 16);
}

// ----------------------------
// Initialize RNG state for a work-item
// gid = get_global_id(0) or other unique thread index
// ----------------------------
inline void rng_init(x128_state_t* state, uint gid) {
    state->s0 = splitmix32(gid + 0);
    state->s1 = splitmix32(gid + 1);
    state->s2 = splitmix32(gid + 2);
    state->s3 = splitmix32(gid + 3);
}

// ----------------------------
// Next uint32 random
// ----------------------------
inline uint x128_next_uint(x128_state_t* state) {
    uint result = state->s0 + state->s3;

    uint t = state->s1 << 9;

    state->s2 ^= state->s0;
    state->s3 ^= state->s1;
    state->s1 ^= state->s2;
    state->s0 ^= state->s3;

    state->s2 ^= t;

    state->s3 = rotate_left(state->s3, 11);

    return result;
}

// ----------------------------
// Float in [0,1)
// ----------------------------
inline float x128_next_float(x128_state_t* state) {
    uint r = x128_next_uint(state);
    return (float)(r >> 8) * (1.0f / 16777216.0f); // 1/2^24
}

// ----------------------------
// Float in [lower, upper)
// ----------------------------
inline float x128_next_float_range(x128_state_t* state, float lower, float upper) {
    float f = x128_next_float(state);
#ifdef USEFMA
    return fma(f, upper - lower, lower);
#else
    return f * (upper - lower) + lower;
#endif
}

// ----------------------------
// Float in [-1,1)
// ----------------------------
inline float x128_next_neg1pos1(x128_state_t* state) {
    float f = x128_next_float(state);
#ifdef USEFMA
    return fma(f, 2.0f, -1.0f);
#else
    return f * 2.0f - 1.0f;
#endif
}

// ----------------------------
// Float in [-0.5,0.5)
// ----------------------------
inline float x128_next_0505(x128_state_t* state) {
    float f = x128_next_float(state);
    return f - 0.5f;
}


// ----------------------------
// GPU RNG: xoroshiro64+ variant (outputs float in [0,1) using top 24 bits)
float rand_x64(uint *s0, uint *s1) {
    uint _s0 = *s0;
    uint _s1 = *s1;
    uint result = (_s0 + _s1);

    uint t = _s1 ^ _s0;
    *s0 = rotate_left(_s0, 26) ^ t ^ (t << 9);
    *s1 = rotate_left(t, 13);

    return (float)(result >> 8) / 16777216.0f; // Get the upper 24bit for more uniform randomness
}


inline int sample_cdf(__global const float* CDF, int length, float u_rand) {
    if (length <= 0) return 0;

    // scale u_rand to the range of the CDF
    float target = u_rand * CDF[length - 1];

    // find first index where CDF[idx] > target
    for (int idx = 0; idx < length; ++idx) {
        if (CDF[idx] > target) return idx;
    }

    // fallback (should never happen if CDF is well-formed)
    return length - 1;
}


inline int sample_cdf_binary(__local const float* CDF, int length, float u_rand) {
    if (length <= 0) return 0;

    // scale u_rand to the range of the CDF
    float target = u_rand * CDF[length - 1];

    int low = 0;
    int high = length - 1;

    // binary search for first CDF[idx] > target
    while (low < high) {
        int mid = low + (high - low) / 2;
        if (CDF[mid] > target) {
            high = mid;
        } else {
            low = mid + 1;
        }
    }

    return low; // first index where CDF[idx] > target
}


inline void affine_local(float2* pos, float2 X, float2 Y, float2 O) {
    float2 p = *pos;
    pos->x = p.x * X.x + p.y * Y.x + O.x;
    pos->y = p.x * X.y + p.y * Y.y + O.y;
}


inline float2 affine(float2 p, float2 X, float2 Y, float2 O)
{
    return (float2)(
        p.x * X.x + p.y * Y.x + O.x,
        p.x * X.y + p.y * Y.y + O.y
    );
}

__kernel void flam3( 
    int P_length,
    __global float * restrict P,
    int PSCALE_length,
    __global float * restrict PSCALE,
    int COLOR_length,
    __global float * restrict COLOR,
    int ALPHA_length,
    __global float * restrict ALPHA,
    int    RES,
    int IW_length,
    int IW_tuplesize,
    __global int * restrict IW_index,
    __global float * restrict IW,
    int SHD_length,
    int SHD_tuplesize,
    __global int * restrict SHD_index,
    __global float * restrict SHD,
    int X_length,
    int X_tuplesize,
    __global int * restrict X_index,
    __global float2 * restrict X,
    int Y_length,
    int Y_tuplesize,
    __global int * restrict Y_index,
    __global float2 * restrict Y,
    int O_length,
    int O_tuplesize,
    __global int * restrict O_index,
    __global float2 * restrict O,
    int POST_length,
    int POST_tuplesize,
    __global int * restrict POST_index,
    __global int * restrict POST,
    int PX_length,
    int PX_tuplesize,
    __global int * restrict PX_index,
    __global float2 * restrict PX,
    int PY_length,
    int PY_tuplesize,
    __global int * restrict PY_index,
    __global float2 * restrict PY,
    int PO_length,
    int PO_tuplesize,
    __global int * restrict PO_index,
    __global float2 * restrict PO,
    int V1T_length,
    int V1T_tuplesize,
    __global int * restrict V1T_index,
    __global float * restrict V1T,
    int V1W_length,
    int V1W_tuplesize,
    __global int * restrict V1W_index,
    __global float * restrict V1W
)
{
    int gid = get_global_id(0);
    if (gid >= P_length)
        return;
        
    // Copy data to local memory
    int lid = get_local_id(0);
    int lsize = get_local_size(0);
    __local float local_IW[MAX_XFORMS];
    __local float local_SHD[MAX_XFORMS];
    __local float2 local_X[MAX_AFFINE_SIZE];
    __local float2 local_Y[MAX_AFFINE_SIZE];
    __local float2 local_O[MAX_AFFINE_SIZE];

    __local int local_POST[MAX_XFORMS];
    __local float2 local_PX[MAX_AFFINE_SIZE];
    __local float2 local_PY[MAX_AFFINE_SIZE];
    __local float2 local_PO[MAX_AFFINE_SIZE];

    // Copy cooperatively among work-items in the group
    int TOTAL_AFFINE = RES * 3;
    for(int i = lid; i < TOTAL_AFFINE; i += lsize){
        local_SHD[i] = SHD[i];
        local_X[i] = X[i];
        local_Y[i] = Y[i];
        local_O[i] = O[i];
        local_PX[i] = PX[i];
        local_PY[i] = PY[i];
        local_PO[i] = PO[i];
        local_POST[i] = POST[i];
    }
    // This will always be smaller, so one work-item will copy the remaining data
    if (lid == 0) {
         for(int i = 0; i < RES; ++i){
            local_IW[i] = IW[i];
        }
    }
    // Wait to complete the copy
    barrier(CLK_LOCAL_MEM_FENCE);
    
    int idx;
    float2 pos = (0.0f, 0.0f);
    float prev_clr = 0.0f;
    float clr = 0.0f;
    
    
    x128_state_t rng;
    rng_init(&rng, gid);  // unique per thread
        
    for (int i = 0; i < 1024; ++i){
    
        // Init
        float2 tmp = pos;
    
        // Random number float in [0,1)
        float r = x128_next_float(&rng);
        
        // Xform selection
        idx = sample_cdf_binary(local_IW, RES, r);
        
        // Pre-affine transform
        affine_local(&tmp, local_X[idx], local_Y[idx], local_O[idx]);
        
        
        
        // Apply variations (not implemented yet)
        float w = V1W[idx];
        tmp *= w;
        
        
        
        // Post-affine transform
        if(local_POST[idx]) affine_local(&tmp, local_PX[idx], local_PY[idx], local_PO[idx]);

        // Color
        prev_clr = clr = local_SHD[idx] + local_SHD[RES + idx] * prev_clr;
        
        // Update
        pos = tmp;
    } 
    
    // Get this sample Alpha value
    float a = local_SHD[RES + RES + idx];
    
    // OUT
    vstore3((float3)(pos.x, pos.y, 0), gid, P);
    vstore(PSCL * a, gid, PSCALE);
    vstore(clr, gid, COLOR);
    vstore(a, gid, ALPHA);
    
}
