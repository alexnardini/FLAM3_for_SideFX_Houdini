#include "interpolate.h" 
float lerpConstant( constant float * in, int size, float pos);


uint rotate_left(uint x, int k) {
    return (x << k) | (x >> (32 - k));
}
// returns random float [0,1), updates s0/s1
float rand_xoroshiro(uint *s0, uint *s1) {
    uint result = (*s0 + *s1);

    uint t = *s1 ^ *s0;
    *s0 = rotate_left(*s0, 26) ^ t ^ (t << 9);
    *s1 = rotate_left(t, 13);

    return (float)(result & 0x00FFFFFFu) / 16777216.0f;
}



// NOT USED
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


inline int sample_cdf_binary(__global const float* CDF, int length, float u_rand) {
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

// NOT USED
inline float2 affine(float2 p, float2 X, float2 Y, float2 O)
{
    return (float2)(
        p.x * X.x + p.y * Y.x + O.x,
        p.x * X.y + p.y * Y.y + O.y
    );
}

kernel void flam3( 
    int P_length,
    global float * restrict P,
    int my_clr_length,
    global float * restrict my_clr,
    int    RES,
    int X_length,
    int X_tuplesize,
    global int * restrict X_index,
    global float2 * restrict X,
    int Y_length,
    int Y_tuplesize,
    global int * restrict Y_index,
    global float2 * restrict Y,
    int O_length,
    int O_tuplesize,
    global int * restrict O_index,
    global float2 * restrict O,
    int IW_length,
    int IW_tuplesize,
    global int * restrict IW_index,
    global float * restrict IW,
    int SHD_length,
    int SHD_tuplesize,
    global int * restrict SHD_index,
    global float * restrict SHD
)
{
    int gid = get_global_id(0);
    if (gid >= P_length)
        return;
    
    float2 pos = (float2)(0.0f, 0.0f);
    float prev_clr = 0.0f;
    float clr = 0;
    
    
    uint s0 = gid;
    uint s1 = gid ^ 0x9E3779B9u;
        
    #pragma unroll 4
    for (int i = 0; i < 1024; ++i){
    
        // Init
        float2 tmp = pos;
    
        // Random number float in [0,1)
        float r = rand_xoroshiro(&s0, &s1);
        
        // Xform selection
        int idx_xf = sample_cdf_binary(IW, RES, r);
        
        // Pre-affine transform
        affine_local(&tmp, X[idx_xf], Y[idx_xf], O[idx_xf]);

        // Pre-affine transform (inline)
        // float x0 = tmp.x;
        // float y0 = tmp.y;
        // tmp.x = x0 * X[idx_xf].x + y0 * Y[idx_xf].x + O[idx_xf].x;
        // tmp.y = x0 * X[idx_xf].y + y0 * Y[idx_xf].y + O[idx_xf].y;

        // Color (minimize repeated global reads)
        prev_clr = clr = SHD[idx_xf] + SHD[RES + idx_xf] * prev_clr;
        
        // Update
        pos = tmp;
    }

    // OUT
    vstore(clr, gid, my_clr);
    vstore3((float3)(pos.x, pos.y, 0), gid, P);

}