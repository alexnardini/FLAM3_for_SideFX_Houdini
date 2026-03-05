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


// ----------------------------
// CL FLAM3 CDF binary
// ----------------------------
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


// ----------------------------
// CL FLAM3 affine transform
// ----------------------------
inline float2 affine(const float2 pos, const float2 X, const float2 Y, const float2 O)
{
    float px = pos.x;
    float py = pos.y;

    return (float2)(
        /*A*/px * X.x + /*B*/py * Y.x + /*C*/O.x,
        /*D*/px * X.y + /*E*/py * Y.y + /*F*/O.y
    );
}




// ----------------------------
// CL FLAM3 helper functions
//
// They are used across all variations to perform their computation.
// Mostly proted from the CVEX code base but alsode upgraded using OpenCL specific instructions.
// They all make distinctions for native and not native OpenCl functions.
// ----------------------------

#define EPS     2.220446049250313e-016
#define M_TAU   6.283185307179586476925
#define M_1_2PI 0.159154943091895335769
// #define M_1_PI  0.318309886183790671538
// #define M_2_PI  0.636619772367581343076
#define FLOAT_MAX_TAN 8388607.0f
#define FLOAT_MIN_TAN -FLOAT_MAX_TAN

inline float ATAN(const float2 p){return atan2(p.x, p.y); }

inline float ATANYX(const float2 p){ return atan2(p.y, p.x); }

inline float SUMSQ(const float2 p){ return dot(p, p); }

inline float SQRT(const float2 p){
#ifdef USE_NATIVE
    return native_sqrt(dot(p, p));
#else
    return sqrt(dot(p, p));
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

inline float fmod_custom(const float a, const float b){ return a - trunc(a / b) * b; }

inline void sincos_fast(float a, float* s, float* c)
{
#ifdef USE_NATIVE
    *s = native_sin(a);
    *c = native_cos(a);
#else
    *s = sincos(a, c);
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



// ----------------------------
// CL FLAM3 variations
//
// All the variations/plugins being implemented.
// The CVEX code base has been the starting point
// and they all have been upgraded for OpenCL.
// ----------------------------

// ----------------------------
// 000 VAR LINEAR
// ----------------------------
float2 CL_V_LINEAR(const float2 in, const float w){
    return w * in;
}
// ----------------------------
// 001 VAR SINUSOIDAL
// ----------------------------
float2 CL_V_SINUSOIDAL(const float2 in, const float w){
#ifdef USE_NATIVE
    return w * native_sin(in);
#else
    return w * sin(in);
#endif
}
// ----------------------------
// 002 VAR SPHERICAL
// ----------------------------
float2 CL_V_SPHERICAL(const float2 in, const float w){
    float r2 = w / Zeps(SUMSQ(in));
    return r2 * in;
}
// ----------------------------
// 003 VAR SWIRL
// ----------------------------
float2 CL_V_SWIRL(float2 in, float w)
{
    float r = SUMSQ(in);

    float sr, cr;
    sincos_fast(r, &sr, &cr);

    return w * (float2)(
        sr * in.x - cr * in.y,
        cr * in.x + sr * in.y
    );
}
// ----------------------------
// 004 VAR HORSESHOWE
// ----------------------------
float2 CL_V_HORSESHOE(const float2 in, const float w){
    float x = in.x;
    float y = in.y;

    float xx = x * x;
    float yy = y * y;
    float xy = x * y;

    float r = w / Zeps(SQRT(in));

    return (float2)(
        (xx - yy) * r,
        (2.0f * xy) * r
    );
}
// ----------------------------
// 005 VAR POLAR
// ----------------------------
float2 CL_V_POLAR(const float2 in, const float w){
    float nx, ny;
    nx = ATAN(in) * M_1_PI;
    ny = SQRT(in) - 1.0;

    return w * (float2)(nx, ny);
}
// ----------------------------
// 006 VAR HANDKERCHIEF
// ----------------------------
float2 CL_V_HANDKERCHIEF(const float2 in, const float w){
    float a = ATAN(in);
    float _SQRT = SQRT(in);
#ifdef USE_NATIVE
    return w * _SQRT * (float2)(native_sin(a + _SQRT), native_cos(a - _SQRT));
#else
    return w * _SQRT * (float2)(sin(a + _SQRT), cos(a - _SQRT));
#endif
}
// ----------------------------
// 007 VAR HEART
// ----------------------------
float2 CL_V_HEART(const float2 in, const float w){
    float _SQRT, a, r;
    _SQRT = SQRT(in);
    a = _SQRT * ATAN(in);
    r = w * _SQRT;
#ifdef USE_NATIVE
    return (float2)(
        r * native_sin(a),
        (-r) * native_cos(a)
    );
#else
    return (float2)(
        r * sin(a),
        (-r) * cos(a)
    );
#endif
}
// ----------------------------
// 008 VAR DISC
// ----------------------------
float2 CL_V_DISC(const float2 in, const float w){
    float a, r, sr, cr;
    a  = ATAN(in) * M_1_PI;
    r = SQRT(in) * M_PI;
    sincos_fast(r, &sr, &cr);

    return w * a * (float2)(sr, cr);
}
// ----------------------------
// 009 VAR SPIRAL
// ----------------------------
float2 CL_V_SPIRAL(const float2 in, const float w){
    float _SQRT, r, r1, sr, cr;
    _SQRT = SQRT(in);
    float2 precalc = in / _SQRT;
    r = Zeps(_SQRT);
    r1 = w / r;
    sincos_fast(r, &sr, &cr);

    return r1 * (float2)((precalc.y + sr), (precalc.x - cr));
}
// ----------------------------
// 010 VAR HIPERBOLIC
// ----------------------------
float2 CL_V_HIPERBOLIC(const float2 in, const float w){
    float _SQRT = SQRT(in);
    float rr = Zeps(_SQRT);
    float2 precalc = in / _SQRT;

    return w * (float2)(precalc.x / rr, precalc.y * rr);
}
// ----------------------------
// 011 VAR DIAMOND
// ----------------------------
float2 CL_V_DIAMOND(const float2 in, const float w){
    float a, r;
    a = atan2(in.x, in.y);
    r = SQRT(in);

#ifdef USE_NATIVE
    return w * (float2)(
        native_sin(a) * native_cos(r), 
        native_cos(a) * native_sin(r)
    );
#else
    return w * (float2)(
        sin(a) * cos(rr), 
        cos(a) * sin(rr)
    );
#endif
}
// ----------------------------
// 012 VAR EX
// ----------------------------
float2 CL_V_EX(const float2 in, const float w){
    float a, r, n0, n1, m0, m1;
    a = ATAN(in);
    r = SQRT(in);
#ifdef USE_NATIVE
    n0 = native_sin(a + r);
    n1 = native_cos(a - r);
#else
    n0 = sin(a + r);
    n1 = cos(a - r);
#endif
    m0 = n0 * n0 * n0 * r;
    m1 = n1 * n1 * n1 * r;

    return w * (float2)(
        m0 + m1, 
        m0 - m1
    );
}
// ----------------------------
// 013 VAR JULIA
// ----------------------------
float2 CL_V_JULIA(const float2 in, const float w, x128_state_t* state){
    float r, a, sa, ca;
    a = 0.5 * ATAN(in);
    if(x128_next_float(state) < 0.5)
        a += M_PI;
    r = w * sqrt(SQRT(in));
    sincos_fast(a, &sa, &ca);

    return r * (float2)(ca, sa);
}
// ----------------------------
// 014 VAR BENT
// ----------------------------
float2 CL_V_BENT(const float2 in, const float w){
    float nx = select(in.x, in.x * 2.0f, in.x < 0.0f);
    float ny = select(in.y, in.y * 0.5f, in.y < 0.0f);

    return w * (float2)(nx, ny);
}
// ----------------------------
// 015 VAR WAVES
// ----------------------------
float2 CL_V_WAVES(const float2 in, const float w, const float b, const float c, const float e, const float f){
    float m_Dx2 = 1.0f / Zeps(c * c);
    float m_Dy2 = 1.0f / Zeps(f * f);
    
#ifdef USE_NATIVE
    return w * (float2)(
        in.x + b * native_sin(in.y * m_Dx2), 
        in.y + e * native_sin(in.x * m_Dy2)
    );
#else
    return w * (float2)(
        in.x + b * sin(in.y * m_Dx2), 
        in.y + e * sin(in.x * m_Dy2)
    );
#endif
}
// ----------------------------
// 016 VAR FISHEYE
// ----------------------------
float2 CL_V_FISHEYE(const float2 in, const float w){
    float r = SQRT(in);
    r = 2.0f * w / (r + 1.0f);

    return r * in;
}
// ----------------------------
// 017 VAR POPCORN
// ----------------------------
float2 CL_V_POPCORN(const float2 in, const float w, const float c, const float f){
#ifdef USE_NATIVE
    return w * in + (float2)(c, f) * native_sin(native_tan(3.0f * in.yx));
#else
    return w * in + (float2)(c, f) * sin(tan(3.0f * in.yx));
#endif
}
// ----------------------------
// 018 VAR EXPONENTIAL
// ----------------------------
float2 CL_V_EXPONENTIAL(const float2 in, const float w){
    float dx, dy, sdy, cdy;
#ifdef USE_NATIVE
    dx = w * native_exp(in.x - 1.0f);
#else
    dx = w * exp(in.x - 1.0f);
#endif
    dy = M_PI * in.y;
    sincos_fast(dy, &sdy, &cdy);

    return dx * (float2)(cdy, sdy);
}
// ----------------------------
// 019 VAR POWER
// ----------------------------
float2 CL_V_POWER(const float2 in, const float w){
    float _SQRT = SQRT(in);
    float2 precalc = in / _SQRT;
    float r = w * pow(_SQRT, precalc[0]);

    return r * precalc.yx;
}
// ----------------------------
// 020 VAR COSINE
// ----------------------------
float2 CL_V_COSINE(const float2 in, const float w){
    float a, sa, ca;
    a = in.x * M_PI;
    sincos_fast(a, &sa, &ca);

    return w * (float2)(
        ca  * cosh(in.y), 
        -sa * sinh(in.y)
    );
}
// ----------------------------
// 021 VAR RINGS
// ----------------------------
float2 CL_V_RINGS(const float2 in, const float w, const float c){
    float _SQRT, dx, r;
    _SQRT = SQRT(in);
    float2 precalc = in / _SQRT;

    dx = Zeps(c * c);
    r = w * (fmod(_SQRT + dx, 2.0f * dx) - dx + _SQRT * (1.0f - dx));

    return r * precalc.yx;
}
// ----------------------------
// 022 VAR FAN
// ----------------------------
float2 CL_V_FAN(const float2 in, const float w, const float c, const float f){
    float dx, dx2, a, sa, ca;
    dx = M_PI * Zeps(c * c);
    dx2 = 0.5f * dx;
    a = ATAN(in);
    a += (fmod(a + f, dx) > dx2) ? -dx2 : dx2;
    sincos_fast(a, &sa, &ca);

    return w * SQRT(in) * (float2)(ca, sa);
}
// ----------------------------
// 023 VAR BUBBLE
// ----------------------------
float2 CL_V_BUBBLE(const float2 in, const float w){
    float r = w / (0.25f * SUMSQ(in) + 1.0f);

    return r * in;
}
// ----------------------------
// 024 VAR CYLINDER
// ----------------------------
float2 CL_V_CYLINDER(const float2 in, const float w){
#ifdef USE_NATIVE
    return w * (float2)(native_sin(in.x), in.y);
#else
    return w * (float2)(sin(in.x), in.y);
#endif
}
// ----------------------------
// 025 VAR EYEFISH
// ----------------------------
float2 CL_V_EYEFISH(const float2 in, const float w){
    float r =  (w * 2.0f) / (1.0f + SQRT(in));

    return r * in;
}
// ----------------------------
// 026 VAR BLUR
// ----------------------------
float2 CL_V_BLUR(const float2 in, const float w, x128_state_t* state){
    float tmpr, sr, cr, r;
    tmpr = x128_next_float(state) * M_TAU;
    sincos_fast(tmpr, &sr, &cr);
    r = w * x128_next_float(state);

    return r * (float2)(cr, sr);
}



// ----------------------------
// CL FLAM3 variations dispatch
//
// Each iterations of the chaos game will select one variation to be applied to the incoming point/sample.
// The dispatch functions will take care of finding the one and execute it.
// OpenCL 2.0 has function pointers (along with many other improvements that this implementation will massively benefit from),
// but meanwhile this seem to be working great and much more performant than the CVEX code base solution.
// ----------------------------

float2 CL_V_DISPATCH(
    const int type, 
    const float2 in, 
    const float w, 
    const float2 y,
    const float2 o,  
    x128_state_t* state
    )
{
    switch(type)
    {
        case 0:     return CL_V_LINEAR(in, w);
        case 1:     return CL_V_SINUSOIDAL(in, w);
        case 2:     return CL_V_SPHERICAL(in, w);
        case 3:     return CL_V_SWIRL(in, w);
        case 4:     return CL_V_HORSESHOE(in, w);
        case 5:     return CL_V_POLAR(in, w);
        case 6:     return CL_V_HANDKERCHIEF(in, w);
        case 7:     return CL_V_HEART(in, w);
        case 8:     return CL_V_DISC(in, w);
        case 9:     return CL_V_SPIRAL(in, w);
        case 10:    return CL_V_HIPERBOLIC(in, w);
        case 11:    return CL_V_DIAMOND(in, w);
        case 12:    return CL_V_EX(in, w);
        case 13:    return CL_V_JULIA(in, w, state);
        case 14:    return CL_V_BENT(in, w);
        case 15:    return CL_V_WAVES(in, w, y.x, o.x, y.y, o.y);
        case 16:    return CL_V_FISHEYE(in, w);
        case 17:    return CL_V_POPCORN(in, w, o.x, o.y);
        case 18:    return CL_V_EXPONENTIAL(in, w);
        case 19:    return CL_V_POWER(in, w);
        case 20:    return CL_V_COSINE(in, w);
        case 21:    return CL_V_RINGS(in, w, o.x);
        case 22:    return CL_V_FAN(in, w, o.x, o.y);
        case 23:    return CL_V_BUBBLE(in, w);
        case 24:    return CL_V_CYLINDER(in, w);
        case 25:    return CL_V_EYEFISH(in, w);
        case 26:    return CL_V_BLUR(in, w, state);

        default:    return w * in;
    }
}




/*
#define OCL_VAR_LIST            \
    VAR(0, CL_V_LINEAR)        \
    VAR(1, CL_V_SINUSOIDAL)    \
    VAR(2, CL_V_SPHERICAL)     \
    VAR(3, CL_V_SWIRL)         \
    VAR(4, CL_V_HORSESHOE)     \
    VAR(5, CL_V_POLAR)         \
    VAR(6, CL_V_HANDKERCHIEF)  \
    VAR(7, CL_V_HEART)         \
    VAR(8, CL_V_DISC)          


float2 CL_V_DISPATCH_COMPILER(
    const int type, 
    const float2 in, 
    const float w, 
    const float2 x, 
    const float2 y
    )
{
    switch(type)
    {
        #define CASE(ID, OCL_VAR) case ID: return OCL_VAR(in, w, x, y);
        OCL_VAR_LIST
        #undef CASE
    }
    return (float2)(0.0f, 0.0f);
}
*/



// ----------------------------
// CL FLAM3 kernel
//
// The main Kernel function.
// This will be called from the Houdini OpenCL node.
// ----------------------------

__kernel void flam3cl( 
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
        
    // copy data to local memory
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

    // copy cooperatively
    for(int i = lid; i < RES; i += lsize){
        // CDF
        local_IW[i] = IW[i];
        // pre affine
        local_X[i] = X[i];
        local_Y[i] = Y[i];
        local_O[i] = O[i];
        // post affine
        local_POST[i] = POST[i];
        local_PX[i] = PX[i];
        local_PY[i] = PY[i];
        local_PO[i] = PO[i];

        local_VT[i] = convert_int4(VT[i]);
        local_VW[i] = VW[i];
    }
    
    int TOTAL_ELEMENTS = RES * 3;
    for(int i = lid; i < TOTAL_ELEMENTS; i += lsize){
        // shader
        local_SHD[i] = SHD[i];
    }
    if(XS){
        int TOTAL_ELEMENTS_XAOS = RES * RES;
        for(int i = lid; i < TOTAL_ELEMENTS_XAOS; i += lsize){
            // Xaos
            local_XST[i] = XST[i];
        }
    }
    barrier(CLK_LOCAL_MEM_FENCE);   // Wait to complete the copy
    
    // init
    int idx;
    int4 _vt;
    float clr = 0.0f;
    float _prev_clr = 0.0f;
    float2 _y, _o, _tmp, mem;
    float4 _vw;
    
    // RNG init
    float r;
    x128_state_t rng;
    rng_init(&rng, gid + OPID);  // unique per thread, per node
    
    // Build starting sample (Biunit)
    mem = (float2)(x128_next_neg1pos1(&rng), x128_next_neg1pos1(&rng));
    
    // if XAOS, pick a starting iterator from distribution
    if(XS) idx = sample_cdf_binary(local_IW, RES, x128_next_float(&rng));
    
    for (int i = 0; i < 1024; ++i){
    
        // xform selection
        r = x128_next_float(&rng);
        idx = (XS) ? sample_cdf_binary(&local_XST[idx * RES], RES, r) : sample_cdf_binary(local_IW, RES, r);
        
        // pre affine
        _y = local_Y[idx]; _o = local_O[idx];
        mem = affine(mem, local_X[idx], _y, _o);
        
        
        
        // VAR
        _vt = local_VT[idx];
        _vw = local_VW[idx];
        _tmp = (float2)(0.0f, 0.0f);
        if (_vw.x != 0.0f) _tmp += CL_V_DISPATCH(_vt.x, mem, _vw.x, _y, _o, &rng);
        if (_vw.y != 0.0f) _tmp += CL_V_DISPATCH(_vt.y, mem, _vw.y, _y, _o, &rng);
        if (_vw.z != 0.0f) _tmp += CL_V_DISPATCH(_vt.z, mem, _vw.z, _y, _o, &rng);
        if (_vw.w != 0.0f) _tmp += CL_V_DISPATCH(_vt.w, mem, _vw.w, _y, _o, &rng);
        

        
        
        // post affine
        if(local_POST[idx]) _tmp = affine(_tmp, local_PX[idx], local_PY[idx], local_PO[idx]);

        // color
        _prev_clr = clr = local_SHD[idx] + local_SHD[idx + RES] * _prev_clr;
        
        // update
        mem = _tmp;
    }
    
    // get this sample Alpha value
    float a = local_SHD[idx + RES + RES];
    
    // OUT
    vstore3((float3)(mem, 0.0f), gid, P);
    vstore(PSCL * a, gid, PSCALE);
    vstore(clr, gid, COLOR);
    vstore(a, gid, ALPHA);
    
}
