#define USE_FMA     // Enable fused multiply-add if desired
#define USE_NATIVE  // Enable native ocl functions for speed but less accuracy
#define PSCL 0.001f

// ----------------------------
// Constants
// ----------------------------
enum {
    MAX_XFORMS           = 20, 
    MAX_XFORMS_XAOS_SIZE = MAX_XFORMS * MAX_XFORMS, 
    MAX_XFORM_VARS       = 4
};


// ----------------------------
// GPU RNG: Xoroshiro128+
//
// This RNG was originally MWC64X in Fractorium.
// Updated to use Xoroshiro128+ instead for better randomness and longer period.
// It is basically upgrading MWC64X functionality while keeping the same type of helper functions.
// Source: https://prng.di.unimi.it/xoshiro128plus.c
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
#ifdef USE_FMA
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
#ifdef USE_FMA
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


inline int sample_cdf(__global const float* CDF, const int length, const float u_rand) {
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


inline int sample_cdf_binary(__local const float* CDF, const int length, const float u_rand) {
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


inline float2 affine(const float2 pos, const float2 X, const float2 Y, const float2 O)
{
    float px = pos.x;
    float py = pos.y;

    return (float2)(
        /*A*/px * X.x + /*B*/py * Y.x + /*C*/O.x,
        /*D*/px * X.y + /*E*/py * Y.y + /*F*/O.y
    );
}





#define EPS     2.220446049250313e-016
// #define M_TAU   6.283185307179586476925
#define M_1_2PI 0.159154943091895335769
// #define M_1_PI  0.318309886183790671538
// #define M_2_PI  0.636619772367581343076
#define FLOAT_MAX_TAN 8388607.0f
#define FLOAT_MIN_TAN -FLOAT_MAX_TAN

inline float ATAN(const float2 p){ return atan2(p.x, p.y); }
inline float ATANYX(const float2 p){ return atan2(p.y, p.x); }
inline float SUMSQ(const float2 p){ return p.x * p.x + p.y * p.y; }
inline float SQRT(const float2 p){
#ifdef USE_NATIVE
    return native_sqrt(p.x * p.x + p.y * p.y);
#else
    return sqrt(p.x * p.x + p.y * p.y);
#endif
}
inline float SafeTan(const float x){ 
#ifdef USE_NATIVE
    return native_tan(clamp(x, FLOAT_MIN_TAN, FLOAT_MAX_TAN));
#else
    return tan(clamp(x, FLOAT_MIN_TAN, FLOAT_MAX_TAN)); 
#endif
}
inline float Zeps(const float x) { return x + (x == 0) * EPS; }
// inline float sgn(const float n){ return (n < 0) ? -1 : (n > 0) ? 1 : 0; }
inline float sgn(const float n){ return (float)((0 < n) - (n < 0)); }
// inline float fmod_custom(const float a, const float b){ return (a-floor(a/b)*b); }
inline float fmod_custom(const float a, const float b){ return a - trunc(a / b) * b; }
inline void sincos(const float a, float* sa, float* ca){
#ifdef USE_NATIVE
    *sa = native_sin(a);
    *ca = native_cos(a);
#else
    *sa = sin(a);
    *ca = cos(a);
#endif
}
// To be used with an improved Elliptic version which helps with rounding errors. For 64bit(DP, when and if I'll get to add support for it)
// Source: https://mathr.co.uk/blog/2017-11-01_a_more_accurate_elliptic_variation.html
inline float Sqrt1pm1(const float x){
    if (-0.0625 < x && x < 0.0625)
    {
        float num = 0;
        float den = 0;
        num += 1.0 / 32;
        den += 1.0 / 256;
        num *= x;
        den *= x;
        num += 5.0 / 16;
        den += 5.0 / 32;
        num *= x;
        den *= x;
        num += 3.0 / 4;
        den += 15.0 / 16;
        num *= x;
        den *= x;
        num += 1.0 / 2;
        den += 7.0 / 4;
        num *= x;
        den *= x;
        den += 1;
        return num / den;
    }
#ifdef USE_NATIVE
    return native_sqrt(1 + x) - 1;
#else
    return sqrt(1 + x) - 1;
#endif
}
/*
// UNROLLED
// select() is branchless, but floating-point evaluation of (x > -0.0625f) & (x < 0.0625f) may be handled slightly differently by the GPU hardware.
// This can result in tiny differences at the boundary (x ≈ -0.0625 or 0.0625) due to rounding.
inline float Sqrt1pm1(const float x) {
    // Small-x approximation using rational polynomial
    float num = (((1.0f/32.0f * x + 5.0f/16.0f) * x + 3.0f/4.0f) * x + 1.0f/2.0f) * x + 1.0f/32.0f * x; 
    float den = ((((1.0f/256.0f * x + 5.0f/32.0f) * x + 15.0f/16.0f) * x + 7.0f/4.0f) * x + 1.0f);
    
    float approx = num / den;
#ifdef USE_NATIVE
    float normal = native_sqrt(1.0f + x) - 1.0f;
#else
    float normal = sqrt(1.0f + x) - 1.0f;

    // Use approximation for small x, normal formula otherwise
    return select(normal, approx, (x > -0.0625f) & (x < 0.0625f));
}
*/




float2 OCL_V_LINEAR(const float2 in, const float w){
    return w * in;
}
float2 OCL_V_SINUSOIDAL(const float2 in, const float w){
#ifdef USE_NATIVE
    return w * native_sin(in);
#else
    return w * sin(in);
#endif
}
float2 OCL_V_SPHERICAL(const float2 in, const float w){
    float r2 = w / Zeps(SUMSQ(in));
    return r2 * in;
}


float2 OCL_V_DISPATCH(const int type, const float2 in, const float w, const float2 X, const float2 Y){
    switch(type)
    {
        case 0: return OCL_V_LINEAR(in, w);
        case 1: return OCL_V_SINUSOIDAL(in, w);
        case 2: return OCL_V_SPHERICAL(in, w);
        default: return w * in;
    }
}


__kernel void flam3( 
    uint OPID,
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
    int    XS,
    int XST_length,
    int XST_tuplesize,
    __global int * restrict XST_index,
    __global float * restrict XST,
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
    int VT_length,
    int VT_tuplesize,
    __global int * restrict VT_index,
    __global float4 * restrict VT,
    int VW_length,
    int VW_tuplesize,
    __global int * restrict VW_index,
    __global float4 * restrict VW
)
{
    int gid = get_global_id(0);
    if (gid >= P_length || RES > MAX_XFORMS)
        return;
        
    // Copy data to local memory
    int lid = get_local_id(0);
    int lsize = get_local_size(0);
    
    __local float local_IW[MAX_XFORMS];
    __local float local_XST[MAX_XFORMS_XAOS_SIZE];

    __local float local_SHD[MAX_XFORMS * 3];

    __local float2 local_X[MAX_XFORMS];
    __local float2 local_Y[MAX_XFORMS];
    __local float2 local_O[MAX_XFORMS];

    __local int local_POST[MAX_XFORMS];
    __local float2 local_PX[MAX_XFORMS];
    __local float2 local_PY[MAX_XFORMS];
    __local float2 local_PO[MAX_XFORMS];

    __local int4 local_VT[MAX_XFORMS];
    __local float4 local_VW[MAX_XFORMS];

    // Copy cooperatively
    for(int i = lid; i < RES; i += lsize){
        // CDF
        local_IW[i] = IW[i];
        // Pre affine
        local_X[i] = X[i];
        local_Y[i] = Y[i];
        local_O[i] = O[i];
        // Post affine
        local_POST[i] = POST[i];
        local_PX[i] = PX[i];
        local_PY[i] = PY[i];
        local_PO[i] = PO[i];

        local_VT[i] = convert_int4(VT[i]);
        local_VW[i] = VW[i];
    }
    
    int TOTAL_ELEMENTS = RES * 3;
    for(int i = lid; i < TOTAL_ELEMENTS; i += lsize){
        // Shader
        local_SHD[i] = SHD[i];
    }
    int TOTAL_ELEMENTS_XAOS = RES * RES;
    for(int i = lid; i < TOTAL_ELEMENTS_XAOS; i += lsize){
        // Xaos
        local_XST[i] = XST[i];
    }
    barrier(CLK_LOCAL_MEM_FENCE);   // Wait to complete the copy
    
    // Init
    int idx;
    int4 _vt;
    float clr = 0.0f;
    float _prev_clr = 0.0f;
    float2 _x, _y, _tmp, mem;
    float4 _vw;
    
    // RNG init
    float r;
    x128_state_t rng;
    rng_init(&rng, gid + OPID);  // unique per thread, per node

    // Build starting sample (Biunit)
    mem = (float2)(x128_next_neg1pos1(&rng), x128_next_neg1pos1(&rng));
    
    // If XAOS, pick a starting iterator from distribution
    if(XS) idx = sample_cdf_binary(local_IW, RES, x128_next_float(&rng));
    
    for (int i = 0; i < 1024; ++i){
    
        // Xform selection
        r = x128_next_float(&rng);
        idx = (XS) ? sample_cdf_binary(&local_XST[idx * RES], RES, r) : sample_cdf_binary(local_IW, RES, r);
        
        // pre affine
        _x = local_X[idx]; _y = local_Y[idx];
        mem = affine(mem, _x, _y, local_O[idx]);
        
        
        
        // VAR
        _vt = local_VT[idx];
        _vw = local_VW[idx];
        _tmp = (float2)(0.0f, 0.0f);
        if (_vw.x != 0.0f) _tmp += OCL_V_DISPATCH(_vt.x, mem, _vw.x, _x, _y);
        if (_vw.y != 0.0f) _tmp += OCL_V_DISPATCH(_vt.y, mem, _vw.y, _x, _y);
        if (_vw.z != 0.0f) _tmp += OCL_V_DISPATCH(_vt.z, mem, _vw.z, _x, _y);
        if (_vw.w != 0.0f) _tmp += OCL_V_DISPATCH(_vt.w, mem, _vw.w, _x, _y);
        
        ////////////////////////////////////////////////////////////////////////
        

        
        
        // post affine
        if(local_POST[idx]) _tmp = affine(_tmp, local_PX[idx], local_PY[idx], local_PO[idx]);

        // Color
        _prev_clr = clr = local_SHD[idx] + local_SHD[idx + RES] * _prev_clr;
        
        // Update
        mem = _tmp;
    }
    
    // Get this sample Alpha value
    float a = local_SHD[idx + RES + RES];
    
    // OUT
    vstore3((float3)(mem, 0.0f), gid, P);
    vstore(PSCL * a, gid, PSCALE);
    vstore(clr, gid, COLOR);
    vstore(a, gid, ALPHA);
    
}
