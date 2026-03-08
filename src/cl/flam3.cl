#define USE_FMA     // Enable fused multiply-add if desired
#define USE_NATIVE  // Enable native ocl functions for speed but less accuracy
#define PSCL 0.001f

// ----------------------------
// Constants
// ----------------------------
enum {
    MAX_XFORMS                  = 20, 
    MAX_XFORMS_XAOS_SIZE        = MAX_XFORMS * MAX_XFORMS, 
    MAX_XFORM_VARS              = 4,
    MAX_XFORM_PP_VARS           = 3,

    SHD_NUM_SIZE                = 3,

    // ----------------------------
    // PRM F sizes  
    // ----------------------------
    PRM_NUM_F                   = 7,
    PRM_NUM_F_SIZE              = PRM_NUM_F * MAX_XFORMS,
    // ----------------------------
    // PRM F parametrics indexes  
    // ----------------------------
    PRM_F_IDX_RINGS2VAL         = 0,    // value
    PRM_F_IDX_BIPOLARSHIFT      = 1,    // shift
    PRM_F_IDX_CELLSIZE          = 2,    // size
    PRM_F_IDX_RADIALBLUR        = 3,    // angle
    PRM_F_IDX_ESCHERBETA        = 4,    // beta
    PRM_F_IDX_POPCORN2C         = 5,    // c
    PRM_F_IDX_FLUXSPREAD        = 6,    // spread

    // ----------------------------
    // PRM F2 sizes  
    // ----------------------------
    PRM_NUM_F2                  = 29,
    PRM_NUM_F2_SIZE             = PRM_NUM_F2 * MAX_XFORMS,
    // ----------------------------
    // PRM F2 parametrics indexes  
    // ----------------------------
    PRM_F2_IDX_CURL             = 0,    // c1, c2
    PRM_F2_IDX_JULIAN           = 1,    // power, distance
    PRM_F2_IDX_JULIASCOPE       = 2,    // power, distance
    PRM_F2_IDX_FAN2             = 3,    // x, y
    PRM_F2_IDX__RECTANGLES      = 4,    // x, y
    PRM_F2_IDX_DISC2            = 5,    // rot, twist
    PRM_F2_IDX_FLOWER           = 6,    // petals, holes
    PRM_F2_IDX_CONIC            = 7,    // eccentricity, holes
    PRM_F2_IDX_PARABOLA         = 8,    // height, width
    PRM_F2_IDX_BENT2            = 9,    // x, y
    PRM_F2_IDX_LAZYSUSAN        = 10,   // x, y
    PRM_F2_IDX_MODULUS          = 11,   // x, y
    PRM_F2_IDX_POPCORN2         = 12,   // x, y
    PRM_F2_IDX_SEPARATION       = 13,   // x, y
    PRM_F2_IDX_SEPARATIONIN     = 14,   // inside_x, inside_y
    PRM_F2_IDX_SPLIT            = 15,   // x, y
    PRM_F2_IDX_SPLITS           = 16,   // x, y
    PRM_F2_IDX_STRIPES          = 17,   // space, warp
    PRM_F2_IDX_WHORL            = 18,   // inside, outside
    PRM_F2_IDX_WAVES2SCALE      = 19,   // scale_x, scale_y
    PRM_F2_IDX_WAVES2FREQ       = 20,   // frequency_x,  frequency_y
    PRM_F2_IDX_CURVELENGTH      = 21,   // lenght_x, lenght_y
    PRM_F2_IDX_CURVEAMP         = 22,   // amplitude_x, amplitude_y
    PRM_F2_IDX_PERSP            = 23,   // angle, distance
    PRM_F2_IDX_BWRAPTWIST       = 24,   // in_twist, out_twist
    PRM_F2_IDX_POLYNOMIALPOW    = 25,   // pow_x, pow_y
    PRM_F2_IDX_POLYNOMIALLC     = 26,   // Lc_x, Lc_y
    PRM_F2_IDX_POLYNOMIALSC     = 27,   // Sc_x, Sc_y
    PRM_F2_IDX_CROP             = 28,   // area, zero

    // ----------------------------
    // PRM F3 sizes  
    // ----------------------------
    PRM_NUM_F3                  = 9,
    PRM_NUM_F3_SIZE             = PRM_NUM_F3 * MAX_XFORMS,
    // ----------------------------
    // PRM F3 parametrics indexes  
    // ----------------------------
    PRM_F3_IDX_BLOB             = 0,    // low, high, wave
    PRM_F3_IDX_PIE              = 1,    // slices, thickness, rotation
    PRM_F3_IDX_SUPERSHAPE       = 2,    // m, rnd, holes
    PRM_F3_IDX_SUPERSHAPEN      = 3,    // n1, n2, n3
    PRM_F3_IDX_CPOW             = 4,    // power, r, i
    PRM_F3_IDX_LAZYSUSAN        = 5,    // spin, twist, space
    PRM_F3_IDX_LAZYSUSANSTS     = 6,    // spin, twist, space
    PRM_F3_IDX_BWRAPS           = 7,    // size, space, gain
    PRM_F3_IDX_PTSYM            = 8,    // order, center_x, center_y

    // ----------------------------
    // PRM F4 sizes  
    // ----------------------------
    PRM_NUM_F4                  = 11,
    PRM_NUM_F4_SIZE             = PRM_NUM_F4 * MAX_XFORMS,
    // ----------------------------
    // PRM F4 parametrics indexes  
    // ----------------------------
    PRM_F4_IDX_NGON             = 0,    // pow, sides, corners, circle
    PRM_F4_IDX_NGON_PRECALC     = 1,    // cpower, csides, csidesinv, 1.0
    PRM_F4_IDX_PDJW             = 2,    // wA, wB, wC, wD
    PRM_F4_IDX_OSCOPE           = 3,    // frequency, amplitude, damping, separation
    PRM_F4_IDX_WEDGE            = 4,    // swirl, angle, hole, count
    PRM_F4_IDX_WEDGEJULIA       = 5,    // power, angle, dist, count
    PRM_F4_IDX_WEDGESPH         = 6,    // swirl, angle, hole, count
    PRM_F4_IDX_AUGER            = 7,    // frequency, scale, symmetry, weight
    PRM_F4_IDX_MOBIUSRE         = 8,    // reA, reB, reC, reD
    PRM_F4_IDX_MOBIUSIM         = 9,    // imA, imB, imC, imD
    PRM_F4_IDX_CROPLTRB         = 10,    // left, top, right, bottom

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
// 32-byte aligned
// ----------------------------
typedef struct {
    float4 xy;  // X.x X.y Y.x Y.y
    float4 o;   // O.x O.y unused unused
} affine_t;
inline float2 affine(__private const float2 in, __private const affine_t affine)
{
    // Referece affine
    // /*A*/in.x * X.x + /*B*/in.y * Y.x + /*C*/O.x,
    // /*D*/in.x * X.y + /*E*/in.y * Y.y + /*F*/O.y

    /*
    Correct mapping:

        affine.xy.x → X.x

        affine.xy.y → X.y

        affine.xy.z → Y.x

        affine.xy.w → Y.y

        affine.o.x → O.x

        affine.o.y → O.y
    */

#ifdef USE_FMA
    return (float2)(
        fma(in.x, affine.xy.x, fma(in.y, affine.xy.z, affine.o.x)),
        fma(in.x, affine.xy.y, fma(in.y, affine.xy.w, affine.o.y))
    );
#else
    return (float2)(
        /*A*/in.x * affine.xy.x + /*B*/in.y * affine.xy.z + /*C*/affine.o.x,
        /*D*/in.x * affine.xy.y + /*E*/in.y * affine.xy.w + /*F*/affine.o.y
    );
#endif
}




// ----------------------------
// CL FLAM3 helper functions
//
// They are used across all variations to perform their computation.
// Mostly proted from the CVEX code base but alsode upgraded using OpenCL specific instructions.
// They all make distinctions for native and not native OpenCl functions.
// ----------------------------

#define EPS     2.220446049250313e-016f
#define M_TAU   6.283185307179586476925f
#define M_1_2PI 0.159154943091895335769f
// #define M_1_PI  0.318309886183790671538f
// #define M_2_PI  0.636619772367581343076f
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

// To be used with an improved Elliptic version which helps with rounding errors.
// For 64bit(DP, when and if I'll find the time to add support for it)
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
// and they have been upgraded for OpenCL.
// ----------------------------

// ----------------------------
// 000 VAR LINEAR
// ----------------------------
float2 CL_V_LINEAR( __private const float2 in, 
                    __private const float w
                    )
{
    return w * in;
}
// ----------------------------
// 001 VAR SINUSOIDAL
// ----------------------------
float2 CL_V_SINUSOIDAL( __private const float2 in, 
                        __private const float w
                        )
{
#ifdef USE_NATIVE
    return w * native_sin(in);
#else
    return w * sin(in);
#endif
}
// ----------------------------
// 002 VAR SPHERICAL
// ----------------------------
float2 CL_V_SPHERICAL(  __private const float2 in, 
                        __private const float w
                        )
{
    float r2 = w / Zeps(SUMSQ(in));
    return r2 * in;
}
// ----------------------------
// 003 VAR SWIRL
// ----------------------------
float2 CL_V_SWIRL(  __private float2 in, 
                    __private float w
                    )
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
float2 CL_V_HORSESHOE(  __private const float2 in, 
                        __private const float w
                        )
{
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
float2 CL_V_POLAR(  __private const float2 in, 
                    __private const float w
                    )
{
    float nx, ny;
    nx = ATAN(in) * M_1_PI;
    ny = SQRT(in) - 1.0;

    return w * (float2)(nx, ny);
}
// ----------------------------
// 006 VAR HANDKERCHIEF
// ----------------------------
float2 CL_V_HANDKERCHIEF(   __private const float2 in, 
                            __private const float w
                            )
{
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
float2 CL_V_HEART(  __private const float2 in, 
                    __private const float w
                    )
{
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
float2 CL_V_DISC(   __private const float2 in, 
                    __private const float w
                    )
{
    float a, r, sr, cr;
    a  = ATAN(in) * M_1_PI;
    r = SQRT(in) * M_PI;
    sincos_fast(r, &sr, &cr);

    return w * a * (float2)(sr, cr);
}
// ----------------------------
// 009 VAR SPIRAL
// ----------------------------
float2 CL_V_SPIRAL( __private const float2 in, 
                    __private const float w
                    )
{
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
float2 CL_V_HIPERBOLIC( __private const float2 in, 
                        __private const float w
                        )
{
    float _SQRT = SQRT(in);
    float rr = Zeps(_SQRT);
    float2 precalc = in / _SQRT;

    return w * (float2)(precalc.x / rr, precalc.y * rr);
}
// ----------------------------
// 011 VAR DIAMOND
// ----------------------------
float2 CL_V_DIAMOND(__private const float2 in,
                    __private const float w
                    )
{
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
float2 CL_V_EX( __private const float2 in, 
                __private const float w
                )
{
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
float2 CL_V_JULIA(  __private const float2 in, 
                    __private const float w, 
                    __private x128_state_t* state
                    )
{
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
float2 CL_V_BENT(   __private const float2 in, 
                    __private const float w
                    )
{
    float nx = select(in.x, in.x * 2.0f, in.x < 0.0f);
    float ny = select(in.y, in.y * 0.5f, in.y < 0.0f);

    return w * (float2)(nx, ny);
}
// ----------------------------
// 015 VAR WAVES
// ----------------------------
float2 CL_V_WAVES(  __private const float2 in, 
                    __private const float w, 
                    __private const float b, 
                    __private const float c, 
                    __private const float e, 
                    __private const float f
                    )
{
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
float2 CL_V_FISHEYE(__private const float2 in, 
                    __private const float w
                    )
{
    float r = SQRT(in);
    r = 2.0f * w / (r + 1.0f);

    return r * in;
}
// ----------------------------
// 017 VAR POPCORN
// ----------------------------
float2 CL_V_POPCORN(__private const float2 in, 
                    __private const float w, 
                    __private const float c, 
                    __private const float f
                    )
{
#ifdef USE_NATIVE
    return w * in + (float2)(c, f) * native_sin(native_tan(3.0f * in.yx));
#else
    return w * in + (float2)(c, f) * sin(tan(3.0f * in.yx));
#endif
}
// ----------------------------
// 018 VAR EXPONENTIAL
// ----------------------------
float2 CL_V_EXPONENTIAL(__private const float2 in, 
                        __private const float w
                        )
{
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
float2 CL_V_POWER(  __private const float2 in, 
                    __private const float w
                    )
{
    float r2 = in.x * in.x + in.y * in.y;
    if (r2 == 0.0f)
        return (float2)(0.0f, 0.0f);

    float inv_r = native_rsqrt(r2);
    float r = r2 * inv_r;
    float2 n = in * inv_r;
#ifdef USE_NATIVE
    float amp = w * native_exp(n.x * native_log(r));
#else
    float amp = w * exp(n.x * log(r));
#endif

    return amp * (float2)(n.y, n.x);
}
// ----------------------------
// 020 VAR COSINE
// ----------------------------
float2 CL_V_COSINE( __private const float2 in, 
                    __private const float w
                    )
{
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
float2 CL_V_RINGS(  __private const float2 in, 
                    __private const float w, 
                    __private const float c
                    )
{
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
float2 CL_V_FAN(__private const float2 in, 
                __private const float w, 
                __private const float c, 
                __private const float f
                )
{
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
float2 CL_V_BUBBLE( __private const float2 in, 
                    __private const float w
                    )
{
    float r = w / (0.25f * SUMSQ(in) + 1.0f);

    return r * in;
}
// ----------------------------
// 024 VAR CYLINDER
// ----------------------------
float2 CL_V_CYLINDER(   __private const float2 in, 
                        __private const float w
                        )
{
#ifdef USE_NATIVE
    return w * (float2)(native_sin(in.x), in.y);
#else
    return w * (float2)(sin(in.x), in.y);
#endif
}
// ----------------------------
// 025 VAR EYEFISH
// ----------------------------
float2 CL_V_EYEFISH(__private const float2 in, 
                    __private const float w
                    )
{
    float r =  (w * 2.0f) / (1.0f + SQRT(in));

    return r * in;
}
// ----------------------------
// 026 VAR BLUR
// ----------------------------
float2 CL_V_BLUR(   __private const float2 in, 
                    __private const float w, 
                    __private x128_state_t* state
                    )
{
    float tmpr, sr, cr, r;
    tmpr = x128_next_float(state) * M_TAU;
    sincos_fast(tmpr, &sr, &cr);
    r = w * x128_next_float(state);

    return r * (float2)(cr, sr);
}
// ----------------------------
// 027 VAR CURL
// ----------------------------
float2 CL_V_CURL(   __private const float2 in, 
                    __private const float w, 
                    __private const float2 c
                    )
{
    float re, im, r;
    
    re = 1.0f + c.x * in.x + c.y * ((in.x * in.x) - (in.y * in.y));
    im = c.x * in.y + (2.0f * c.y) *  in.x * in.y;
    r = w / Zeps((re * re) + (im * im));

    return r * (float2)(
        in.x * re + in.y * im, 
        in.y * re - in.x * im
    );
}
// ----------------------------
// 028 VAR NGON
// ----------------------------
float2 CL_V_NGON(   __private const float2 in, 
                    __private const float w, 
                    __private const float4 ngon, 
                    __private const float4 ngon_precalc // cpower csides csidesinv unused
                    )
{
    float r2 = in.x * in.x + in.y * in.y;
#ifdef USE_NATIVE
    float r_factor = (r2 == 0.0f) ? 0.0f : native_exp(ngon_precalc.x * native_log(r2));
#else
    float r_factor = (r2 == 0.0f) ? 0.0f : exp(ngon_precalc.x * log(r2));
#endif

    float theta = atan2(in.y, in.x);

    float phi = theta - ngon_precalc.y * floor(theta * ngon_precalc.z);
    phi -= ngon_precalc.y * (phi > 0.5f * ngon_precalc.y);
#ifdef USE_NATIVE
    float amp = (ngon.z * (1.0f / native_cos(phi) - 1.0f) + ngon.w) * w * r_factor;
#else
    float amp = (ngon.z * (1.0f / cos(phi) - 1.0f) + ngon.w) * w * r_factor;
#endif

    return amp * in;
}
// ----------------------------
// 029 VAR PDG
// ----------------------------
float2 CL_V_PDJ(__private const float2 in, 
                __private const float w, 
                __private const float4 pdj  // wA wB wC wD
                )
{
#ifdef USE_NATIVE
    float ox = native_sin(pdj.x * in.y) - native_cos(pdj.y * in.x);
    float oy = native_sin(pdj.z * in.x) - native_cos(pdj.w * in.y);
#else
    float ox = sin(pp.x * in.y) - cos(pp.y * in.x);
    float oy = sin(pp.z * in.x) - cos(pp.w * in.y);
#endif

    return w * (float2)(ox, oy);
}
// ----------------------------
// 030 VAR BLOB
// ----------------------------
float2 CL_V_BLOB(   __private const float2 in, 
                    __private const float w, 
                    __private const float4 blob // low high wave unused
                    )
{
    float _SQRT, low, high, wave, blob_coeff, rr, aa, bdiff;
    _SQRT = SQRT(in);
    float2 precalc = in / _SQRT;

    aa = ATAN(in);
    bdiff = blob.y - blob.x;
#ifdef USE_NATIVE
    rr = _SQRT * (blob.x + bdiff * (0.5f + 0.5f * native_sin(blob.z * aa)));
#else
    rr = _SQRT * (blob.x + bdiff * (0.5f + 0.5f * sin(blob.z * aa)));
#endif

    return w * rr * precalc;
}
// ----------------------------
// 031 VAR JULIAN
// ----------------------------
float2 CL_V_JULIAN( __private const float2 in, 
                    __private const float w, 
                    x128_state_t* state, 
                    __private const float2 julian   // power distance
                    )
{
    int t_rnd;
    float inv_jx, julian_cn, rr, tmpr, sa, ca;
#ifdef USE_NATIVE
    inv_jx = native_recip(julian.x);
#else
    inv_jx = recip(julian.x);
#endif
    julian_cn = julian.y * inv_jx * 0.5f;

    float r2 = SUMSQ(in);
    float a  = ATANYX(in);

    t_rnd = (int)(julian.x * x128_next_float(state));
    tmpr = (a + M_TAU * t_rnd) * inv_jx;
#ifdef USE_NATIVE
    rr = w * native_powr(r2, julian_cn);
#else
    rr = w * powr(r2, julian_cn);
#endif

    sincos_fast(tmpr, &sa, &ca);

    return rr * (float2)(ca, sa);
}
// ----------------------------
// 032 VAR JULIASCOPE
// ----------------------------
float2 CL_V_JULIASCOPE( __private const float2 in, 
                        __private const float w, 
                        x128_state_t* state, 
                        __private const float2 juliascope   // power distance
                        )
{
    int t_rnd;
    float _ATANYX, julian_rN, sign, julian_cn, tmpr, rr, sa, ca;

    float inv_jx = 1.0f / juliascope.x;

    _ATANYX = ATANYX(in);
    julian_rN = juliascope.x;
    julian_cn = juliascope.y * inv_jx * 0.5f;

    t_rnd = (int)(julian_rN * x128_next_float(state));

    sign = (t_rnd & 1) ? -1.0f : 1.0f;
    tmpr = (M_TAU * t_rnd + sign * _ATANYX) * inv_jx;

    sincos_fast(tmpr, &sa, &ca);
#ifdef USE_NATIVE
    rr = w * native_powr(SUMSQ(in), julian_cn);
#else
    rr = w * powr(SUMSQ(in), julian_cn);
#endif

    return rr * (float2)(ca, sa);
}
// ----------------------------
// 033 VAR GAUSSIAN BLUR
// ----------------------------
float2 CL_V_GAUSSIAN_BLUR(  __private const float2 in, 
                            __private const float w, 
                            __private x128_state_t* state
                            )
{
    float ang, rr, sa, ca;
    ang = x128_next_float(state) * M_TAU;
    rr = w * (x128_next_float(state) + x128_next_float(state) + x128_next_float(state) + x128_next_float(state) - 2.0f);
    sincos_fast(ang, &sa, &ca);

    return rr * (float2)(ca, sa);
}
// ----------------------------
// 034 VAR FAN2
// ----------------------------
float2 CL_V_FAN2(   __private const float2 in, 
                    __private const float w, 
                    __private const float2 fan2 // x y
                    )
{
    float dx, dx2, inv_dx, a, r, ady, tt, sa, ca;
    dx  = M_PI_F * Zeps(fan2.x * fan2.x);
    dx2 = 0.5f * dx;
#ifdef USE_NATIVE
    inv_dx = native_recip(dx);
#else
    inv_dx = recip(dx);
#endif

    a = ATAN(in);
#ifdef USE_NATIVE
    r = w * native_sqrt(SUMSQ(in));
#else
    r = w * sqrt(SUMSQ(in));
#endif

    ady = a + fan2.y;
    tt = ady - dx * (int)(ady * inv_dx);
    a += dx2 * (1.0f - 2.0f * step(dx2, tt));

    sincos_fast(a, &sa, &ca);

    return r * (float2)(sa, ca);
}
// ----------------------------
// 035 VAR RINGS2
// ----------------------------
float2 CL_V_RINGS2( __private const float2 in, 
                    __private const float w, 
                    __private const float rings2val // value
                    )
{
    float _SQRT, rr, dx;
    int nrand;
    _SQRT = SQRT(in);
    float2 precalc = in / _SQRT;
    rr = _SQRT;
    dx = rings2val * rings2val;
    rr += -2.0f * dx * (int)((rr + dx)/(2.0f * dx)) + rr * (1.0f - dx);

    return w * rr * precalc;
}


// ----------------------------
// CL FLAM3 variations dispatch
//
// Each iterations of the chaos game will select one variation to be applied to the incoming point/sample.
// The dispatch will take care of finding the one and execute it.
// ----------------------------

float2 CL_V_DISPATCH(
    __private const int type, 
    __private const float2 in, 
    __private const float w, 
    __private const float2 y,
    __private const float2 o, 
    __private x128_state_t* state, 
    __local const float* PRM_F, 
    __local const float2* PRM_F2, 
    __local const float4* PRM_F3,   // Casted as float4 instead of float3 so it map correctly
    __local const float4* PRM_F4 
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
        case 27:    return CL_V_CURL(in, w, PRM_F2[PRM_F2_IDX_CURL]);
        case 28:    return CL_V_NGON(in, w, PRM_F4[PRM_F4_IDX_NGON], PRM_F4[PRM_F4_IDX_NGON_PRECALC]);
        case 29:    return CL_V_PDJ(in, w, PRM_F4[PRM_F4_IDX_PDJW]);
        case 30:    return CL_V_BLOB(in, w, PRM_F3[PRM_F3_IDX_BLOB]);
        case 31:    return CL_V_JULIAN(in, w, state, PRM_F2[PRM_F2_IDX_JULIAN]);
        case 32:    return CL_V_JULIASCOPE(in, w, state, PRM_F2[PRM_F2_IDX_JULIASCOPE]);
        case 33:    return CL_V_GAUSSIAN_BLUR(in, w, state);
        case 34:    return CL_V_FAN2(in, w, PRM_F2[PRM_F2_IDX_FAN2]);
        case 35:    return CL_V_RINGS2(in, w, PRM_F[PRM_F_IDX_RINGS2VAL]);

        default:    return w * in;
    }
}



/*
// I like this method but I do not like the idea
// to have all the variations functions share the same arguments set.

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
    __global float4 * restrict VW,
    int PRM_F_length,
    int PRM_F_tuplesize,
    __global int * restrict PRM_F_index,
    __global float * restrict PRM_F,
    int PRM_F2_length,
    int PRM_F2_tuplesize,
    __global int * restrict PRM_F2_index,
    __global float2 * restrict PRM_F2,
    int PRM_F3_length,
    int PRM_F3_tuplesize,
    __global int * restrict PRM_F3_index,
    __global float4 * restrict PRM_F3,   // Casted as float4 instead of float3 so it map correctly
    int PRM_F4_length,
    int PRM_F4_tuplesize,
    __global int * restrict PRM_F4_index,
    __global float4 * restrict PRM_F4
)
{
    int gid = get_global_id(0);
    if (gid >= P_length || RES > MAX_XFORMS)
        return;
        
    // copy data to local memory
    int lid = get_local_id(0);
    int lsize = get_local_size(0);
    
    // CDF
    __local float local_IW[MAX_XFORMS];

    // XAOS
    __local float local_XST[MAX_XFORMS_XAOS_SIZE];

    // shader
    __local float local_SHD[MAX_XFORMS * 3];

    __local affine_t local_PRE_AFFINE[MAX_XFORMS];
    __local affine_t local_POST_AFFINE[MAX_XFORMS];
    __local int local_POST[MAX_XFORMS]; // post affine toggles

    // VAR variations
    __local int4 local_VT[MAX_XFORMS];
    __local float4 local_VW[MAX_XFORMS];

    // PRE, VAR and POST parameterics
    __local float local_PRM_F[PRM_NUM_F_SIZE];
    __local float2 local_PRM_F2[PRM_NUM_F2_SIZE];
    __local float4 local_PRM_F3[PRM_NUM_F3_SIZE];
    __local float4 local_PRM_F4[PRM_NUM_F4_SIZE];

    // copy cooperatively
    for(int i = lid; i < RES; i += lsize){
        // CDF
        local_IW[i] = IW[i];
        // pre affine
        local_PRE_AFFINE[i].xy = (float4)(X[i], Y[i]);
        local_PRE_AFFINE[i].o = (float4)(O[i], 0, 0);
        // post affine
        local_POST_AFFINE[i].xy = (float4)(PX[i], PY[i]);
        local_POST_AFFINE[i].o = (float4)(PO[i], 0, 0);
        // post affine toggles
        local_POST[i] = POST[i];

        // VAR variations
        local_VT[i] = convert_int4(VT[i]);
        local_VW[i] = VW[i];
    }
    // shader
    int TOTAL_ELEMENTS = RES * SHD_NUM_SIZE;
    for(int i = lid; i < TOTAL_ELEMENTS; i += lsize){
        local_SHD[i] = SHD[i];
    }
    // parametrics float
    TOTAL_ELEMENTS = RES * PRM_NUM_F;
    for(int i = lid; i < TOTAL_ELEMENTS; i += lsize){
        local_PRM_F[i] = PRM_F[i];
    }
    // parametrics float2
    TOTAL_ELEMENTS = RES * PRM_NUM_F2;
    for(int i = lid; i < TOTAL_ELEMENTS; i += lsize){
        local_PRM_F2[i] = PRM_F2[i];
    }
    // parametrics float3
    TOTAL_ELEMENTS = RES * PRM_NUM_F3;
    for(int i = lid; i < TOTAL_ELEMENTS; i += lsize){
        local_PRM_F3[i] = PRM_F3[i];
    }
    // parametrics float4
    TOTAL_ELEMENTS = RES * PRM_NUM_F4;
    for(int i = lid; i < TOTAL_ELEMENTS; i += lsize){
        local_PRM_F4[i] = PRM_F4[i];
    }
    if(XS){
        // Xaos
        TOTAL_ELEMENTS = RES * RES;
        for(int i = lid; i < TOTAL_ELEMENTS; i += lsize){
            local_XST[i] = XST[i];
        }
    }
    barrier(CLK_LOCAL_MEM_FENCE);   // Wait to complete the copy
    
    // init
    int idx;
    int4 _vt;
    float clr = 0.0f;
    float _prev_clr = 0.0f;
    float2 mem, _tmp, _y, _o;
    float4 _vw;
    
    // RNG init
    float r;
    x128_state_t rng;
    rng_init(&rng, gid + OPID);  // unique per thread, per node
    
    // build starting sample (Biunit)
    mem = (float2)(x128_next_neg1pos1(&rng), x128_next_neg1pos1(&rng));
    
    // if XAOS, pick a starting iterator from distribution
    if(XS) idx = sample_cdf_binary(local_IW, RES, x128_next_float(&rng));
    
    for (int i = 0; i < 1024; ++i){
        
        // xform selection
        r = x128_next_float(&rng);
        idx = (XS) ? sample_cdf_binary(&local_XST[idx * RES], RES, r) : sample_cdf_binary(local_IW, RES, r);
        
        // parameterics data
        __local float* xf_prm_f   = &local_PRM_F[idx * PRM_NUM_F];
        __local float2* xf_prm_f2 = &local_PRM_F2[idx * PRM_NUM_F2];
        __local float4* xf_prm_f3 = &local_PRM_F3[idx * PRM_NUM_F3];
        __local float4* xf_prm_f4 = &local_PRM_F4[idx * PRM_NUM_F4];
        
        // pre affine 
        affine_t pa = local_PRE_AFFINE[idx];
        mem = affine(mem, pa);
        
        

        // VAR
        _vt = local_VT[idx];
        _vw = local_VW[idx];
        _tmp = (float2)(0.0f, 0.0f);
        if (_vw.x != 0.0f) _tmp += CL_V_DISPATCH(_vt.x, mem, _vw.x, pa.xy.zw, pa.o.xy, &rng, xf_prm_f, xf_prm_f2, xf_prm_f3, xf_prm_f4);
        if (_vw.y != 0.0f) _tmp += CL_V_DISPATCH(_vt.y, mem, _vw.y, pa.xy.zw, pa.o.xy, &rng, xf_prm_f, xf_prm_f2, xf_prm_f3, xf_prm_f4);
        if (_vw.z != 0.0f) _tmp += CL_V_DISPATCH(_vt.z, mem, _vw.z, pa.xy.zw, pa.o.xy, &rng, xf_prm_f, xf_prm_f2, xf_prm_f3, xf_prm_f4);
        if (_vw.w != 0.0f) _tmp += CL_V_DISPATCH(_vt.w, mem, _vw.w, pa.xy.zw, pa.o.xy, &rng, xf_prm_f, xf_prm_f2, xf_prm_f3, xf_prm_f4);

        
        
        if(local_POST[idx]){
            affine_t po = local_POST_AFFINE[idx];
            _tmp = affine(_tmp, po);
            }

        // color
        _prev_clr = clr = local_SHD[idx] + local_SHD[idx + RES] * _prev_clr;
        
        // update
        mem = _tmp;
    }
    
    // Alpha value
    float a = local_SHD[idx + RES + RES];
    
    // OUT
    vstore3((float3)(mem, 0.0f), gid, P);
    vstore(PSCL * a, gid, PSCALE);
    vstore(clr, gid, COLOR);
    vstore(a, gid, ALPHA);
    
}
