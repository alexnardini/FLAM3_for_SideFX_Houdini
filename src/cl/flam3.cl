#include "interpolate.h" 
float lerpConstant( constant float * in, int size, float pos);


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
    int    RES,
    int IW_length,
    global int * restrict IW_index,
    global float * restrict IW,
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
    global float2 * restrict O
)
{
    int idx = get_global_id(0);
    if (idx >= P_length)
        return;
    
    float2 pos = (float2)(0.0f, 0.0f);
    uint state = (uint)get_global_id(0) * 1234567u + 890123u;
        
    for (int i = 0; i < 1024; ++i){
    
        // Init
        float2 tmp = pos;
    
        // Random number
        state ^= state << 13;
        state ^= state >> 17;
        state ^= state << 5;
        float r = (float)(state & 0x00FFFFFFu) / 16777215.0f;
        
        // Xform selection
        int idx_xf = sample_cdf_binary(IW, RES, r);
        
        // PRE Affine
        affine_local(&tmp, X[idx_xf], Y[idx_xf], O[idx_xf]);
            
        // Update
        pos = tmp;
    }
    
    vstore3((float3)(pos.x, pos.y, 0), idx, P);

}