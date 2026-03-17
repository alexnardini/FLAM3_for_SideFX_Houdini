/*  
 /  Tested on:  Houdini 21.0
 /
 /  Title:      FLAM3H™. SideFX Houdini FLAM3: 2D
 /  Author:     Alessandro Nardini
 /  date:       January 2026, Last revised March 2026
 /  License:    GPL
 /  Copyright:  2021, © F stands for liFe ( made in Italy )
 /
 /  info:       Based on the original: "The Fractal Flame Algorithm"
 /  Authors:    Scott Draves, Erik Reckase
 /
 /  Paper:      https://flam3.com/flame_draves.pdf
 /  Date:       September 2003, Last revised November 2008
 /
 /  Github:     https://github.com/scottdraves/flam3
 /  Date:       December 2002, Last revised May 2015
 /
 /  Name:       CL FLAM3 "OPENCL"
 /
 /  Comment:    OpenCL FLAM3
*/


/* For now we are compiling using: -cl-fast-relaxed-math
 / so the USE_NATIVE wont make much difference as the compiler will optimize aggressively anyway.
 / In the future will add the following as a compiler kernel options inside houdini.
*/

#define USE_FMA         1   // Enable fused multiply-add if desired
#define USE_NATIVE      1   // Enable native ocl functions for speed but less accuracy
#define USE_RNG_X128    1   // Use RNG x128 random number generator instead of x64 (32bit vs 24bit)

// This is defined in the Houdini environment and must match.
#define PSCL 0.001f         // Default point scale ( @pscale )

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
    // RES PRM FF -> FF and PP (2)  
    // ----------------------------
    FF_RES_PRM                  = 2,

    // ----------------------------
    // PRM F sizes  
    // ----------------------------
    PRM_NUM_F                   = 7,
    PRM_NUM_F_SIZE              = PRM_NUM_F * MAX_XFORMS,
    FF_PRM_NUM_F_SIZE           = PRM_NUM_F * FF_RES_PRM,
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
    FF_PRM_NUM_F2_SIZE          = PRM_NUM_F2 * FF_RES_PRM,
    // ----------------------------
    // PRM F2 parametrics indexes  
    // ----------------------------
    PRM_F2_IDX_CURL             = 0,    // c1, c2
    PRM_F2_IDX_JULIAN           = 1,    // power, distance
    PRM_F2_IDX_JULIASCOPE       = 2,    // power, distance
    PRM_F2_IDX_FAN2             = 3,    // x, y
    PRM_F2_IDX_RECTANGLES       = 4,    // x, y
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
    FF_PRM_NUM_F3_SIZE          = PRM_NUM_F3 * FF_RES_PRM,
    // ----------------------------
    // PRM F3 parametrics indexes  
    // ----------------------------
    PRM_F3_IDX_BLOB             = 0,    // low, high, wave
    PRM_F3_IDX_PIE              = 1,    // slices, thickness, rotation
    PRM_F3_IDX_SUPERSHAPE       = 2,    // m, rnd, holes
    PRM_F3_IDX_SUPERSHAPEN      = 3,    // n1, n2, n3
    PRM_F3_IDX_CPOW             = 4,    // power, r, i
    PRM_F3_IDX_LAZYSUSANSTS     = 5,    // spin, twist, space
    PRM_F3_IDX_BWRAPS           = 6,    // size, space, gain
    PRM_F3_IDX_PTSYM            = 7,    // order, center_x, center_y
    // ----------------------------
    // PRM F3 precalc  
    PRM_F3_IDX_DISC2_PRECALC    = 8,    // timespi, sinadd, cosadd, unused(1.0)

    // ----------------------------
    // PRM F4 sizes  
    // ----------------------------
    PRM_NUM_F4                  = 11,
    PRM_NUM_F4_SIZE             = PRM_NUM_F4 * MAX_XFORMS,
    FF_PRM_NUM_F4_SIZE          = PRM_NUM_F4 * FF_RES_PRM,
    // ----------------------------
    // PRM F4 parametrics indexes  
    // ----------------------------
    PRM_F4_IDX_NGON             = 0,    // pow, sides, corners, circle
    PRM_F4_IDX_PDJW             = 1,    // wA, wB, wC, wD
    PRM_F4_IDX_OSCOPE           = 2,    // frequency, amplitude, damping, separation
    PRM_F4_IDX_WEDGE            = 3,    // swirl, angle, hole, count
    PRM_F4_IDX_WEDGEJULIA       = 4,    // power, angle, dist, count
    PRM_F4_IDX_WEDGESPH         = 5,    // swirl, angle, hole, count
    PRM_F4_IDX_AUGER            = 6,    // frequency, scale, symmetry, weight
    PRM_F4_IDX_MOBIUSRE         = 7,    // reA, reB, reC, reD
    PRM_F4_IDX_MOBIUSIM         = 8,    // imA, imB, imC, imD
    PRM_F4_IDX_CROPLTRB         = 9,    // left, top, right, bottom
    // ----------------------------
    // PRM F4 precalc  
    PRM_F4_IDX_NGON_PRECALC     = 10,   // cpower, csides, csidesinv, unusued(1.0)

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
static inline uint rotate_left(uint x, int k) {
    return (x << k) | (x >> (32 - k));
}

// ----------------------------
// SplitMix32 for per-thread seeding
// ----------------------------
static inline uint splitmix32(uint seed) {
    uint z = seed + 0x9E3779B9u;
    z = (z ^ (z >> 16)) * 0x85EBCA6Bu;
    z = (z ^ (z >> 13)) * 0xC2B2AE35u;
    return z ^ (z >> 16);
}

// ----------------------------
// Initialize x64 RNG state for a work-item
// gid = get_global_id(0) or other unique thread index
// ----------------------------
static inline void x64_rng_init(x128_state_t* state, uint gid) {
    state->s0 = splitmix32(gid + 0);
    state->s1 = splitmix32(gid + 1);
}
// ----------------------------
// Initialize x128 RNG state for a work-item
// gid = get_global_id(0) or other unique thread index
// ----------------------------
static inline void x128_rng_init(x128_state_t* state, uint gid) {
    state->s0 = splitmix32(gid + 0);
    state->s1 = splitmix32(gid + 1);
    state->s2 = splitmix32(gid + 2);
    state->s3 = splitmix32(gid + 3);
}
// ----------------------------
// Helper to init either x128 or x64
// gid = get_global_id(0) or other unique thread index
// ----------------------------
static inline void rng_init(x128_state_t* state, uint gid) {
#if USE_RNG_X128
    x128_rng_init(state, gid);
#else
    x64_rng_init(state, gid);
#endif
}

// ----------------------------
// Next uint32 random
// ----------------------------
static inline uint x128_next_uint(x128_state_t* state) {
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
static inline float x128_next_float(x128_state_t* state) {
    uint r = x128_next_uint(state);
    return (float)(r >> 8) * (1.0f / 16777216.0f); // 1/2^24
}

// ----------------------------
// Float in [lower, upper)
// ----------------------------
static inline float x128_next_float_range(x128_state_t* state, float lower, float upper) {
    float f = x128_next_float(state);
#if USE_FMA
    return fma(f, upper - lower, lower);
#else
    return f * (upper - lower) + lower;
#endif
}

// ----------------------------
// Float in [-1,1)
// ----------------------------
static inline float x128_next_neg1pos1(x128_state_t* state) {
    float f = x128_next_float(state);
#if USE_FMA
    return fma(f, 2.0f, -1.0f);
#else
    return f * 2.0f - 1.0f;
#endif
}

// ----------------------------
// Float in [-0.5,0.5)
// ----------------------------
static inline float x128_next_0505(x128_state_t* state) {
    float f = x128_next_float(state);
    return f - 0.5f;
}

// ----------------------------
// Float in [0,1)
// ----------------------------
static inline float x64_next_float(uint *s0, uint *s1) {
    uint result = (*s0 + *s1);

    uint t = *s1 ^ *s0;
    *s0 = rotate_left(*s0, 26) ^ t ^ (t << 9);
    *s1 = rotate_left(t, 13);

    // return (float)(result & 0x00FFFFFFu) / 16777216.0f;
    return (float)(result >> 8) / 16777216.0f; // Get the upper 24bit for more uniform randomness
}
// ----------------------------
// Float in [-1,1)
// ----------------------------
static inline float x64_next_neg1pos1(x128_state_t* state) {
    float f = x64_next_float(&state->s0, &state->s1);
#if USE_FMA
    return fma(f, 2.0f, -1.0f);
#else
    return f * 2.0f - 1.0f;
#endif
}

// ----------------------------
// Helper to either x128 or x64
// Float in [0,1)
// ----------------------------
static inline float rng_next_float(x128_state_t* state){
#if USE_RNG_X128
    return x128_next_float(state);
#else
    return x64_next_float(&state->s0, &state->s1);
#endif
}
// ----------------------------
// Helper to either x128 or x64
// Float in [-1,1)
// ----------------------------
static inline float rng_next_neg1pos1(x128_state_t* state){
#if USE_RNG_X128
    return x128_next_neg1pos1(state);
#else
    return x64_next_neg1pos1(state);
#endif
}

// ----------------------------
// CL FLAM3 CDF binary
// ----------------------------
static inline int sample_cdf_binary(__local const float* CDF, const int length, const float u_rand) {
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
static inline float2 affine(__private const float2 in, __private const affine_t affine)
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

#if USE_FMA
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
// Mostly ported from the CVEX code base but also upgraded using OpenCL specific instructions.
// They can make distinctions between native and not native OpenCl functions.
// ----------------------------

// The following should be automatically included from within Houdini
// but just in case
#ifndef M_PI
    #define M_PI 3.141592653589793238462f
#endif
#ifndef M_1_PI
    #define M_1_PI  0.318309886183790671538f
#endif
#ifndef M_2_PI
    #define M_2_PI  0.636619772367581343076f
#endif
// end just in case

#define EPS     2.220446049250313e-016f
#define M_TAU   6.283185307179586476925f
#define M_1_2PI 0.159154943091895335769f
#define FLOAT_MAX_TAN 8388607.0f
#define FLOAT_MIN_TAN -FLOAT_MAX_TAN

static inline float ATAN(const float2 p){return atan2(p.x, p.y); }

static inline float ATANYX(const float2 p){ return atan2(p.y, p.x); }

static inline float SUMSQ(const float2 p){ return dot(p, p); }

static inline float SQRT(const float2 p){
#if USE_NATIVE
    return native_sqrt(dot(p, p));
#else
    return sqrt(dot(p, p));
#endif
}

static inline float SafeTan(const float x){ 
#if USE_NATIVE
    return native_tan(clamp(x, FLOAT_MIN_TAN, FLOAT_MAX_TAN));
#else
    return tan(clamp(x, FLOAT_MIN_TAN, FLOAT_MAX_TAN)); 
#endif
}

static inline float Zeps(const float x) { return x + (x == 0) * EPS; }

static inline float sgn(const float n){ return (float)((0.0f < n) - (n < 0.0f)); }

static inline float fmod_custom(const float a, const float b){ return a - trunc(a / b) * b; }

static inline void sincos_fast(float a, float* s, float* c)
{
#if USE_NATIVE
    *s = native_sin(a);
    *c = native_cos(a);
#else
    *s = sincos(a, c);
#endif
}

// To be used with an improved Elliptic version which helps with rounding errors.
// For 64bit(DP, when and if I'll find the time to add support for it)
// Source: https://mathr.co.uk/blog/2017-11-01_a_more_accurate_elliptic_variation.html
static inline float Sqrt1pm1(const float x){
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
#if USE_NATIVE
    return native_sqrt(1 + x) - 1;
#else
    return sqrt(1 + x) - 1;
#endif
}


// ----------------------------
// CL FLAM3 variations
//
// All the variations/plugins being implemented.
// The CVEX code base has been the starting point
// and they have been upgraded to be GPU friendly.
// ----------------------------

// ----------------------------
// 000 VAR LINEAR
// ----------------------------
static float2 CL_V_LINEAR(__private const float2 in, 
                        __private const float w
                        )
{
    return w * in;
}
// ----------------------------
// 001 VAR SINUSOIDAL
// ----------------------------
static float2 CL_V_SINUSOIDAL(__private const float2 in, 
                            __private const float w
                            )
{
#if USE_NATIVE
    return w * native_sin(in);
#else
    return w * sin(in);
#endif
}
// ----------------------------
// 002 VAR SPHERICAL
// ----------------------------
static float2 CL_V_SPHERICAL(__private const float2 in, 
                            __private const float w
                            )
{
    float r2 = w / Zeps(SUMSQ(in));

    return r2 * in;
}
// ----------------------------
// 003 VAR SWIRL
// ----------------------------
static float2 CL_V_SWIRL(__private float2 in, 
                        __private float w
                        )
{
    float r, sr, cr;
    
    r = SUMSQ(in);
    sincos_fast(r, &sr, &cr);

    return w * (float2)(
        sr * in.x - cr * in.y,
        cr * in.x + sr * in.y
    );
}
// ----------------------------
// 004 VAR HORSESHOWE
// ----------------------------
static float2 CL_V_HORSESHOE(__private const float2 in, 
                            __private const float w
                            )
{
    float xx, yy, xy, r;

    xx = in.x * in.x;
    yy = in.y * in.y;
    xy = in.x * in.y;

    r = w / Zeps(SQRT(in));

    return r * (float2)(
        (xx - yy),
        (2.0f * xy)
    );
}
// ----------------------------
// 005 VAR POLAR
// ----------------------------
static float2 CL_V_POLAR(__private const float2 in, 
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
static float2 CL_V_HANDKERCHIEF(__private const float2 in, 
                                __private const float w
                                )
{
    float _SQRT, a_SQRT, a;

    a = ATAN(in);
    _SQRT = SQRT(in);
    a_SQRT = w * _SQRT;

#if USE_NATIVE
    return a_SQRT * (float2)(
        native_sin(a + _SQRT), 
        native_cos(a - _SQRT)
    );
#else
    return a_SQRT * (float2)(
        sin(a + _SQRT), 
        cos(a - _SQRT)
    );
#endif
}
// ----------------------------
// 007 VAR HEART
// ----------------------------
static float2 CL_V_HEART(__private const float2 in, 
                        __private const float w
                        )
{
    float _SQRT, a, r;

    _SQRT = SQRT(in);
    a = _SQRT * ATAN(in);
    r = w * _SQRT;

#if USE_NATIVE
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
static float2 CL_V_DISC(__private const float2 in, 
                        __private const float w
                        )
{
    float a, r, sr, cr;

    a  = ATAN(in) * M_1_PI;
    r  = SQRT(in) * M_PI;
    sincos_fast(r, &sr, &cr);

    float wa = w * a;

    return wa * (float2)(sr, cr);
}
// ----------------------------
// 009 VAR SPIRAL
// ----------------------------
static float2 CL_V_SPIRAL(__private const float2 in, 
                        __private const float w
                        )
{
    float r, r1, sr, cr;

#if USE_NATIVE
    float inv_sqrt = native_rsqrt(dot(in, in));
    float2 precalc = in * inv_sqrt;
    r = Zeps(native_recip(inv_sqrt));
#else
    float inv_sqrt = rsqrt(dot(in, in));
    float2 precalc = in * inv_sqrt;
    r = Zeps(1.0f / inv_sqrt);
#endif
    r1 = w / r;
    sincos_fast(r, &sr, &cr);

    return r1 * (float2)(
        precalc.y + sr,
        precalc.x - cr
    );
}
// ----------------------------
// 010 VAR HIPERBOLIC
// ----------------------------
static float2 CL_V_HIPERBOLIC(__private const float2 in, 
                            __private const float w
                            )
{
    float _SQRT, r;

    _SQRT = SQRT(in);
    r = Zeps(_SQRT);
    float2 precalc = in / _SQRT;

    return w * (float2)(
        precalc.x / r, 
        precalc.y * r
    );
}
// ----------------------------
// 011 VAR DIAMOND
// ----------------------------
static float2 CL_V_DIAMOND(__private const float2 in,
                        __private const float w
                        )
{
    float a, r;

    a = atan2(in.x, in.y);
    r = SQRT(in);

#if USE_NATIVE
    return w * (float2)(
        native_sin(a) * native_cos(r), 
        native_cos(a) * native_sin(r)
    );
#else
    return w * (float2)(
        sin(a) * cos(r), 
        cos(a) * sin(r)
    );
#endif
}
// ----------------------------
// 012 VAR EX
// ----------------------------
static float2 CL_V_EX(__private const float2 in, 
                    __private const float w
                    )
{
    float a, r, n0, n1, m0, m1;

    a = ATAN(in);
    r = SQRT(in);
#if USE_NATIVE
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
static float2 CL_V_JULIA(__private const float2 in, 
                        __private const float w, 
                        __private x128_state_t* state
                        )
{
    float r, a, sa, ca;

    a = 0.5 * ATAN(in);
    a += select(0.0f, (float)M_PI, rng_next_float(state) < 0.5f);
#if USE_NATIVE
    r = w * native_sqrt(SQRT(in));
#else
    r = w * sqrt(SQRT(in));
#endif
    sincos_fast(a, &sa, &ca);

    return r * (float2)(ca, sa);
}
// ----------------------------
// 014 VAR BENT
// ----------------------------
static float2 CL_V_BENT(__private const float2 in, 
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
static float2 CL_V_WAVES(__private const float2 in, 
                        __private const float w, 
                        __private const float b, 
                        __private const float c, 
                        __private const float e, 
                        __private const float f
                        )
{
    float m_Dx2, m_Dy2;
#if USE_NATIVE
    m_Dx2 = native_recip(Zeps(c * c));
    m_Dy2 = native_recip(Zeps(f * f));
#else
    m_Dx2 = 1.0f / Zeps(c * c);
    m_Dy2 = 1.0f / Zeps(f * f);
#endif
    
#if USE_NATIVE
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
static float2 CL_V_FISHEYE(__private const float2 in, 
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
static float2 CL_V_POPCORN(__private const float2 in, 
                        __private const float w, 
                        __private const float c, 
                        __private const float f
                        )
{
#if USE_NATIVE
    return w * in + (float2)(c, f) * native_sin(native_tan(3.0f * in.yx));
#else
    return w * in + (float2)(c, f) * sin(tan(3.0f * in.yx));
#endif
}
// ----------------------------
// 018 VAR EXPONENTIAL
// ----------------------------
static float2 CL_V_EXPONENTIAL(__private const float2 in, 
                            __private const float w
                            )
{
    float dx, dy, sdy, cdy;

#if USE_NATIVE
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
static float2 CL_V_POWER(__private const float2 in, 
                        __private const float w
                        )
{
    float r, r2, inv_r, amp;

    r2 = SUMSQ(in);
    if (r2 == 0.0f)
        return (float2)(0.0f, 0.0f);
#if USE_NATIVE
    inv_r = native_rsqrt(r2);
#else
    inv_r = rsqrt(r2);
#endif
    r = r2 * inv_r;
    float2 n = in * inv_r;
#if USE_NATIVE
    amp = w * native_exp(n.x * native_log(r));
#else
    amp = w * exp(n.x * log(r));
#endif

    return amp * (float2)(n.y, n.x);
}
// ----------------------------
// 020 VAR COSINE
// ----------------------------
static float2 CL_V_COSINE(__private const float2 in, 
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
static float2 CL_V_RINGS(__private const float2 in, 
                        __private const float w, 
                        __private const float c
                        )
{
    float dx, r;

#if USE_NATIVE
    float inv_sqrt = native_rsqrt(dot(in, in));
#else
    float inv_sqrt = rsqrt(dot(in, in));
#endif
    float2 precalc = in * inv_sqrt;

    dx = Zeps(c);
    r = w * (fmod(inv_sqrt + dx, 2.0f * dx) - dx + inv_sqrt * (1.0f - dx));

    return r * precalc.yx;
}
// ----------------------------
// 022 VAR FAN
// ----------------------------
static float2 CL_V_FAN(__private const float2 in, 
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
static float2 CL_V_BUBBLE(__private const float2 in, 
                        __private const float w
                        )
{
#if USE_FMA
    float r = w / fma(0.25f, SUMSQ(in), 1.0f);
#else
    float r = w / (0.25f * SUMSQ(in) + 1.0f);
#endif

    return r * in;
}
// ----------------------------
// 024 VAR CYLINDER
// ----------------------------
static float2 CL_V_CYLINDER(__private const float2 in, 
                            __private const float w
                            )
{
#if USE_NATIVE
    return w * (float2)(
        native_sin(in.x), 
        in.y
    );
#else
    return w * (float2)(
        sin(in.x), 
        in.y
    );
#endif
}
// ----------------------------
// 025 VAR EYEFISH
// ----------------------------
static float2 CL_V_EYEFISH(__private const float2 in, 
                        __private const float w
                        )
{
    float r = (w * 2.0f) / (1.0f + SQRT(in));

    return r * in;
}
// ----------------------------
// 026 VAR BLUR
// ----------------------------
static float2 CL_V_BLUR(__private const float w, 
                        __private x128_state_t* state
                        )
{
    float tmpr, sr, cr, r;

    tmpr = rng_next_float(state) * M_TAU;
    sincos_fast(tmpr, &sr, &cr);
    r = w * rng_next_float(state);

    return r * (float2)(cr, sr);
}
// ----------------------------
// 027 VAR CURL
// ----------------------------
static float2 CL_V_CURL(__private const float2 in, 
                        __private const float w, 
                        __private const float2 c
                        )
{
    float re, im, r;

#if USE_FMA
    float x2 = in.x * in.x;
    float y2 = in.y * in.y;
    re = fma(c.y, (x2 - y2), fma(c.x, in.x, 1.0f));
    im = fma(2.0f * c.y, in.x * in.y, c.x * in.y);
#else
    re = 1.0f + c.x * in.x + c.y * ((in.x * in.x) - (in.y * in.y));
    im = c.x * in.y + (2.0f * c.y) *  in.x * in.y;
#endif
#if USE_FMA
    float value = fma(re, re, im * im);
#else
    float value = (re * re) + (im * im);
#endif
#if USE_NATIVE
    r = w * native_recip(Zeps(value));
#else
    r = w * 1.0f / Zeps(value);
#endif

    return r * (float2)(
        in.x * re + in.y * im, 
        in.y * re - in.x * im
    );
}
// ----------------------------
// 028 VAR NGON
// ----------------------------
static float2 CL_V_NGON(__private const float2 in, 
                        __private const float w, 
                        __private const float4 ngon, 
                        __private const float4 ngon_precalc // cpower csides csidesinv unusued(1.0)
                        )
{
    float r2, r_factor, theta, phi, amp;

    r2 = SUMSQ(in);
#if USE_NATIVE
    r_factor = (r2 == 0.0f) ? 0.0f : native_exp(ngon_precalc.x * native_log(r2));
#else
    r_factor = (r2 == 0.0f) ? 0.0f : exp(ngon_precalc.x * log(r2));
#endif

    theta = atan2(in.y, in.x);

    phi = theta - ngon_precalc.y * floor(theta * ngon_precalc.z);
    phi -= ngon_precalc.y * (phi > 0.5f * ngon_precalc.y);
#if USE_NATIVE
    amp = (ngon.z * (native_recip(native_cos(phi)) - 1.0f) + ngon.w) * w * r_factor;
#else
    amp = (ngon.z * (1.0f / cos(phi) - 1.0f) + ngon.w) * w * r_factor;
#endif

    return amp * in;
}
// ----------------------------
// 029 VAR PDG
// ----------------------------
static float2 CL_V_PDJ(__private const float2 in, 
                    __private const float w, 
                    __private const float4 pdj  // wA wB wC wD
                    )
{
    float ox, oy;

#if USE_NATIVE
    ox = native_sin(pdj.x * in.y) - native_cos(pdj.y * in.x);
    oy = native_sin(pdj.z * in.x) - native_cos(pdj.w * in.y);
#else
    ox = sin(pdj.x * in.y) - cos(pdj.y * in.x);
    oy = sin(pdj.z * in.x) - cos(pdj.w * in.y);
#endif

    return w * (float2)(ox, oy);
}
// ----------------------------
// 030 VAR BLOB
// ----------------------------
static float2 CL_V_BLOB(__private const float2 in, 
                        __private const float w, 
                        __private const float4 blob // low high wave unused
                        )
{
    float d, r, aa, bdiff;

    float _SQRT = SQRT(in);
    float2 precalc = in / _SQRT;

    aa = ATAN(in);
    bdiff = blob.y - blob.x;
#if USE_NATIVE
    r = _SQRT * (blob.x + bdiff * (0.5f + 0.5f * native_sin(blob.z * aa)));
#else
    r = _SQRT * (blob.x + bdiff * (0.5f + 0.5f * sin(blob.z * aa)));
#endif

    float wrr = w * r;

    return wrr * precalc;
}
// ----------------------------
// 031 VAR JULIAN
// ----------------------------
static float2 CL_V_JULIAN(__private const float2 in, 
                        __private const float w, 
                        x128_state_t* state, 
                        __private const float2 julian   // power distance
                        )
{
    int t_rnd;
    float inv_jx, julian_cn, r, tmpr, sa, ca;

#if USE_NATIVE
    inv_jx = native_recip(julian.x);
#else
    inv_jx = 1.0f / julian.x;
#endif
    julian_cn = julian.y * inv_jx * 0.5f;

    float r2 = SUMSQ(in);
    float a  = ATANYX(in);

    t_rnd = (int)(julian.x * rng_next_float(state));
    tmpr = (a + M_TAU * t_rnd) * inv_jx;
#if USE_NATIVE
    r = w * native_powr(r2, julian_cn);
#else
    r = w * powr(r2, julian_cn);
#endif

    sincos_fast(tmpr, &sa, &ca);

    return r * (float2)(ca, sa);
}
// ----------------------------
// 032 VAR JULIASCOPE
// ----------------------------
static float2 CL_V_JULIASCOPE(__private const float2 in, 
                            __private const float w, 
                            x128_state_t* state, 
                            __private const float2 juliascope   // power(julian_rN) distance
                            )
{
    int t_rnd;
    float _ATANYX, julian_rN, sign, julian_cn, tmpr, r, sa, ca;
    
#if USE_NATIVE
    float inv_jx = native_recip(juliascope.x);
#else
    float inv_jx = 1.0f / juliascope.x;
#endif

    _ATANYX = ATANYX(in);
    julian_cn = juliascope.y * inv_jx * 0.5f;

    t_rnd = (int)(juliascope.x * rng_next_float(state));

    sign = (t_rnd & 1) ? -1.0f : 1.0f;
    tmpr = (M_TAU * t_rnd + sign * _ATANYX) * inv_jx;

    sincos_fast(tmpr, &sa, &ca);
#if USE_NATIVE
    r = w * native_powr(SUMSQ(in), julian_cn);
#else
    r = w * powr(SUMSQ(in), julian_cn);
#endif

    return r * (float2)(ca, sa);
}
// ----------------------------
// 033 VAR GAUSSIAN BLUR
// ----------------------------
static float2 CL_V_GAUSSIAN_BLUR(__private const float w, 
                                __private x128_state_t* state
                                )
{
    float rnd1, rndA, rndG, sa, ca;

    rndA = rng_next_float(state) * M_TAU;
    rndG = w * (rng_next_float(state) + 
                rng_next_float(state) + 
                rng_next_float(state) + 
                rng_next_float(state) - 
                2.0f
                );
    sincos_fast(rndA, &sa, &ca);

    return rndG * (float2)(ca, sa);
}
// ----------------------------
// 034 VAR FAN2
// ----------------------------
static float2 CL_V_FAN2(__private const float2 in, 
                        __private const float w, 
                        __private const float2 fan2 // x y
                        )
{
    float dx, dx2, inv_dx, a, r, ady, t, sa, ca;

    dx  = M_PI_F * Zeps(fan2.x * fan2.x);
    dx2 = 0.5f * dx;
#if USE_NATIVE
    inv_dx = native_recip(dx);
#else
    inv_dx = 1.0f / dx;
#endif

    a = ATAN(in);
#if USE_NATIVE
    r = w * native_sqrt(SUMSQ(in));
#else
    r = w * sqrt(SUMSQ(in));
#endif

    ady = a + fan2.y;
    t = ady - dx * (int)(ady * inv_dx);
    a += dx2 * (1.0f - 2.0f * step(dx2, t));

    sincos_fast(a, &sa, &ca);

    return r * (float2)(sa, ca);
}
// ----------------------------
// 035 VAR RINGS2
// ----------------------------
static float2 CL_V_RINGS2(__private const float2 in, 
                        __private const float w, 
                        __private const float rings2val // value
                        )
{
    float _SQRT, r, dx;
    int nrand;

    _SQRT = SQRT(in);
    float2 precalc = in / _SQRT;
    r = _SQRT;
    dx = rings2val * rings2val;
    r += -2.0f * dx * (int)((r + dx)/(2.0f * dx)) + r * (1.0f - dx);

    float wr = w * r;

    return wr * precalc;
}
// ----------------------------
// 036 VAR RECTANGLES
// ----------------------------
static float2 CL_V_RECTANGLES(__private const float2 in, 
                            __private const float w, 
                            __private const float2 rectangles // x y
                            )
{
    float2 invr, t, m;
#if USE_NATIVE
    invr = native_recip(rectangles);
#else
    invr = 1.0f / rectangles;
#endif
#if USE_FMA
    t = floor(in * invr);
    m = fma(t, 2.0f * rectangles, rectangles) - in;
#else
    m = (2.0f * floor(in * invr) + 1.0f) * rectangles - in;
#endif

    return w * select(
        m, 
        in, 
        rectangles == 0.0f
    );
}
// ----------------------------
// 037 VAR RADIAL BLUR
// ----------------------------
static float2 CL_V_RADIALBLUR(__private const float2 in, 
                            __private const float w, 
                            __private x128_state_t* state, 
                            __private const float angle // angle
                            )
{
    float rndG, tmpa, ra, rz, sa, ca, m_spin, m_zoom;

    sincos_fast(angle * M_PI_2, &m_spin, &m_zoom);  // TO DO: compute in vex land
    
    rndG = w * (rng_next_float(state) +
                rng_next_float(state) +
                rng_next_float(state) +
                rng_next_float(state) - 
                2.0f
                );

    ra = SQRT(in);
#if USE_FMA
    tmpa = fma(m_spin, rndG, ATANYX(in));
    sincos_fast(tmpa, &sa, &ca);
    rz = fma(m_zoom, rndG, -1.0f);

    return fma(rz, in, ra * (float2)(ca, sa));
#else
    tmpa = ATANYX(in) + m_spin * rndG;
    sincos_fast(tmpa, &sa, &ca);
    rz = m_zoom * rndG - 1.0f;

    return ra * (float2)(ca, sa) + rz * in;
#endif
}
// ----------------------------
// 038 VAR PIE
// ----------------------------
static float2 CL_V_PIE(__private const float w, 
                    __private x128_state_t* state, 
                    __private const float4 pie  // slices thickness rotation
                    )
{
    float a, r, sa, ca, sl;

    sl = (int)(rng_next_float(state) * pie.x);
    a = pie.z + M_TAU * (sl + rng_next_float(state) * pie.y) / pie.x;
    r = w * rng_next_float(state);
    sincos_fast(a, &sa, &ca);

    return r * (float2)(ca, sa);
}
// ----------------------------
// 039 VAR ARCH
// ----------------------------
static float2 CL_V_ARCH(__private const float2 in, 
                        __private const float w, 
                        __private x128_state_t* state
                        )
{
    float a, sa, ca;

    a = rng_next_float(state) * w * M_PI;
    sincos_fast(a, &sa, &ca);
    float sa2 = sa * sa;

#if USE_NATIVE
    
    float inv_ca = native_recip(ca);
#else
    float inv_ca = 1.0f / ca;
#endif

    return w * (float2)(
        sa, 
        sa2 * inv_ca
    );
}
// ----------------------------
// 040 VAR TANGENT
// ----------------------------
static float2 CL_V_TANGENT(__private const float2 in, 
                        __private const float w
                        )
{
#if USE_NATIVE
    return w * (float2)(
        native_sin(in.x) / native_cos(in.y), 
        native_tan(in.y)
    );
#else
    return w * (float2)(
        sin(in.x) / cos(in.y), 
        tan(in.y)
    );
#endif
}
// ----------------------------
// 041 VAR SQUARE
// ----------------------------
static float2 CL_V_SQUARE(__private const float w, 
                        __private x128_state_t* state
                        )
{
    return w * (float2)(
        rng_next_float(state) - 0.5, 
        rng_next_float(state) - 0.5
    );
}
// ----------------------------
// 042 VAR RAYS
// ----------------------------
static float2 CL_V_RAYS(__private const float2 in, 
                        __private const float w, 
                        __private x128_state_t* state
                        )
{
    float ang, r, tanr;

    ang = w * rng_next_float(state) * M_PI;
#if USE_NATIVE
    r = w * native_recip(Zeps(SUMSQ(in)));
    tanr = w * native_tan(ang) * r;

    return tanr * (float2)(
        native_cos(in.x), 
        native_sin(in.y)
    );
#else
    r = w * (1.0f / Zeps(SUMSQ(in)));
    tanr = w * tan(ang) * r;

    return tanr * (float2)(
        cos(in.x), 
        sin(in.y)
    );
#endif
}
// ----------------------------
// 043 VAR BLADE
// ----------------------------
static float2 CL_V_BLADE(__private const float2 in, 
                        __private const float w, 
                        __private x128_state_t* state
                        )
{
    float r, sr, cr;

    r = w * rng_next_float(state) * SQRT(in);
    sincos_fast(r, &sr, &cr);

    float wx = w * in.x;

    return wx * (float2)(
        cr + sr, 
        cr - sr
    );
}
// ----------------------------
// 044 VAR SECANT2
// ----------------------------
static float2 CL_V_SECANT2(__private const float2 in, 
                        __private const float w
                        )
{
    float r, sr, cr, icr;

    r = w * SQRT(in);
    sincos_fast(r, &sr, &cr);
#if USE_NATIVE
    icr = native_recip(cr);
#else
    icr = 1.0f / cr;
#endif

    return w * (float2)(
        in.x, 
        select(icr - 1.0f, icr + 1.0f, cr < 0)
    );
}
// ----------------------------
// 045 VAR TWINTRIAN
// ----------------------------
static float2 CL_V_TWINTRIAN(__private const float2 in, 
                            __private const float w, 
                            __private x128_state_t* state
                            )
{
    float r, sr, ss, cr, diff;

    r = rng_next_float(state) * w * SQRT(in);
    sincos_fast(r, &sr, &cr);
    ss = sr * sr;
#if USE_NATIVE
    // diff = native_log10(ss) + cr;
    diff = native_log(ss) * 0.434294481903251827651f + cr;
#else
    diff = log10(ss) + cr;
#endif
    diff = select(diff, -30.0f, !isfinite(diff) | isnan(diff));

    float wx = w * in.x;

    return wx * (float2)(
        diff,
        diff - sr * M_PI
    );
}
// ----------------------------
// 046 VAR TWINTRIAN
// ----------------------------
static float2 CL_V_CROSS(__private const float2 in, 
                        __private const float w, 
                        __private const int F3C
                        )
{
    float r, inxy;

    inxy = (in.x - in.y) * (in.x + in.y);
    r = w / select(Zeps(inxy), Zeps(fabs(inxy)), F3C);

    return r * in;
}
// ----------------------------
// 047 VAR DISC2
// ----------------------------
static float2 CL_V_DISC2(__private const float2 in, 
                        __private const float w, 
                        __private const float2 disc2,   // rot twist
                        __private const float4 disc2_pc // (F3) disc2_timespi disc2_sinadd disc2_cosadd
                        )
{
    float r, t, sr, cr;

    t = disc2_pc.x * (in.x + in.y);
    sincos_fast(t, &sr, &cr);
    r = w * ATAN(in) / M_PI;

    return r * (float2)(
        sr + disc2_pc.z, 
        cr + disc2_pc.y
    );
}
// ----------------------------
// 048 VAR DISC2
// ----------------------------
static float2 CL_V_SUPERSHAPE(__private const float2 in, 
                            __private const float w, 
                            __private x128_state_t* state, 
                            __private const float4 supershape,  // (F3) m rnd holes
                            __private const float4 supershape_n // (F3) n1 n2 n3
                        )
{
    float _SQRT, theta, st, ct, t, r, ss_pm_4, ss_pneg1_n1;

    // TO DO: compute in vex land
    // I did but made no difference and I prefer to keep it here
    // so the wrangle core node in Houdini's land remain more performant.
    ss_pm_4 = supershape.x * 0.25f;
#if USE_NATIVE
    ss_pneg1_n1 = native_recip(supershape_n.x) * -1.0f;
#else
    ss_pneg1_n1 = -1.0f / supershape_n.x;
#endif
    float inv_sy = 1.0f - supershape.y;

    _SQRT = SQRT(in);
#if USE_NATIVE
    float inv_sqrt = native_recip(_SQRT);
#else
    float inv_sqrt = 1.0f / _SQRT;
#endif

    theta = ss_pm_4 * ATANYX(in) + M_PI_4;
    sincos_fast(theta, &st, &ct);
    float rnd = supershape.y * rng_next_float(state) + inv_sy * _SQRT - supershape.z;
#if USE_NATIVE
    t = native_powr(fabs(ct), supershape_n.y) + native_powr(fabs(st), supershape_n.z);
    r = w * rnd * native_powr(t, ss_pneg1_n1) * inv_sqrt;
#else
    t = powr(fabs(ct), supershape_n.y) + powr(fabs(st), supershape_n.z);
    r = w * rnd * powr(t, ss_pneg1_n1) * inv_sqrt;
#endif

    return r * in;
}
// ----------------------------
// 049 VAR FLOWER
// ----------------------------
static float2 CL_V_FLOWER(__private const float2 in, 
                        __private const float w, 
                        __private x128_state_t* state, 
                        __private const float2 flower   // petals holes
                        )
{
    float theta, r;

    theta = ATANYX(in);
#if USE_NATIVE
    float n_theta = native_cos(flower.x * theta);
    r = w * (rng_next_float(state) - flower.y) * n_theta * native_rsqrt(dot(in, in));
#else
    float n_theta = cos(flower.x * theta);
    r = w * (rng_next_float(state) - flower.y) * n_theta / SQRT(in);
#endif

    return r * in;
}
// ----------------------------
// 050 VAR CONIC
// ----------------------------
static float2 CL_V_CONIC(__private const float2 in, 
                        __private const float w, 
                        __private x128_state_t* state, 
                        __private const float2 conic    // eccentricity holes
                        )
{
    float ct, r;

    float rnd = rng_next_float(state) - conic.y;
    
#if USE_NATIVE
    float inv_len = native_rsqrt(dot(in, in));
    ct = in.x * inv_len;
#else
    float inv_len = rsqrt(dot(in, in));
    ct = in.x * inv_len;
#endif
    
    r = w * rnd * conic.x * inv_len / (1.0f + conic.x * ct);

    return r * in;
}
// ----------------------------
// 051 VAR PARABOLA
// ----------------------------
static float2 CL_V_PARABOLA(__private const float2 in, 
                            __private const float w, 
                            __private x128_state_t* state, 
                            __private const float2 parabola // height width
                            )
{
    float r, sr, cr;

    r = SQRT(in);
    sincos_fast(r, &sr, &cr);

    float sr2 = sr * sr;

    return w * (float2)(
        parabola.x * sr2 * rng_next_float(state), 
        parabola.y * cr  * rng_next_float(state)
    );
}
// ----------------------------
// 052 VAR BENT2
// ----------------------------
static float2 CL_V_BENT2(__private const float2 in, 
                        __private const float w, 
                        __private const float2 bent2    // x y
                        )
{
    float2 r = select(in, in * bent2, in < 0.0f);

return w * r;
}
// ----------------------------
// 053 VAR BIPOLAR - The most expensive so far
// ----------------------------
static float2 CL_V_BIPOLAR(__private const float2 in, 
                        __private const float w, 
                        __private const float shift // shift
                        )
{
    float x2y2, tt, x2, ps, y, lx;

    x2y2 = dot(in, in);
    tt = x2y2 + 1.0f;
    ps = -M_PI_2 * shift;

#if USE_FMA
    y = fma(0.5f, atan2(2.0f * in.y, x2y2 - 1.0f), ps);
#else
    y = 0.5f * atan2(2.0f * in.y, x2y2 - 1.0f) + ps;
#endif

    y = y - M_PI * floor((y + M_PI_2) * M_1_PI);
#if USE_NATIVE
    lx = native_log((tt + 2.0f * in.x) / (tt - 2.0f * in.x));
#else
    lx = log((tt + 2.0f * in.x) / (tt - 2.0f * in.x));
#endif

    return w * (float2)(
        M_1_2PI * lx,
        M_2_PI * y
    );
}
// ----------------------------
// 054 VAR BOARDERS
// ----------------------------
static float2 CL_V_BOARDERS(__private const float2 in, 
                            __private const float w, 
                            __private x128_state_t* state
                            )
{
    float roundX, roundY, offsetX, offsetY, halfX, halfY, signX, signY;

    roundX = rint(in.x);
    roundY = rint(in.y);
    offsetX = in.x - roundX;
    offsetY = in.y - roundY;

    halfX = offsetX * 0.5f;
    halfY = offsetY * 0.5f;
    signX = copysign(0.25f, offsetX);
    signY = copysign(0.25f, offsetY);

    float rnd = rng_next_float(state);

    if (rnd >= 0.75f)
        return (float2)(halfX + roundX, halfY + roundY);
    else {
        if (fabs(offsetX) >= fabs(offsetY)) {
            // Horizontal
            if (offsetX >= 0.0f) {
                return w * (float2)(
                    halfX + roundX + signX,
                    halfY + roundY + 0.25f * offsetY * native_recip(offsetX)
                );
            } else {
                return w * (float2)(
                    halfX + roundX - 0.25f,
                    halfY + roundY - 0.25f * offsetY * native_recip(offsetX)
                );
            }
        } else {
            // Vertical
            if (offsetY >= 0.0f) {
                return w * (float2)(
                    halfX + roundX + 0.25f * offsetX * native_recip(offsetY),
                    halfY + roundY + 0.25f
                );
            } else {
                return w * (float2)(
                    halfX + roundX - 0.25f * offsetX * native_recip(offsetY),
                    halfY + roundY - 0.25f
                );
            }
        }
    }
}
// ----------------------------
// 055 VAR BUTTERFLY
// ----------------------------
static float2 CL_V_BUTTERFLY(__private const float2 in, 
                            __private const float w
                            )
{
    float wx, y2, r;

    wx = w * 1.3029400317411197908970256609023f;
    y2 = 2.0f * in.y;
#if USE_NATIVE
    r = wx * native_sqrt(fabs(in.y * in.x) / (Zeps(in.x * in.x + y2 * y2)));
#else
    r = wx * sqrt(fabs(in.y * in.x) / (Zeps(in.x * in.x + y2 * y2)));
#endif

    return r * (float2)(in.x, y2);
}
// ----------------------------
// 056 VAR CELL
// ----------------------------
static float2 CL_V_CELL(__private const float2 in, 
                        __private const float w, 
                        __private const float size  // size
                        )
{
    float inv_cell_size, xs, ys, x, y, dx, dy;

#if USE_NATIVE
    inv_cell_size = native_recip(size);
#else
    inv_cell_size = 1.0f / size;
#endif

    x = floor(in.x * inv_cell_size);
    y = floor(in.y * inv_cell_size);
    xs = x * size;
    ys = y * size;
    dx = in.x - xs;
    dy = in.y - ys;

    if (y >= 0.0f) {
        y *= 2.0f;
        if (x >= 0.0f)
            x *= 2.0f;
        else
            x = -(2.0f * x + 1.0f);
    }
    else {
        y = -(2.0f * y + 1.0f);
        if (x >= 0.0f)
            x *= 2.0f;
        else
            x = -(2.0f * x + 1.0f);
    }

    return (float2)(
        w  * (dx + x * size), 
        -w * (dy + y * size)
    );
}
// ----------------------------
// 057 VAR CPOW
// ----------------------------
static float2 CL_V_CPOW(__private const float2 in, 
                        __private const float w, 
                        __private x128_state_t* state, 
                        __private const float4 cpow // power, r, i
                        )
{
    float aa, lnr, va, vc, vd, ang, sa, ca, mm;

    aa = ATANYX(in);
#if USE_NATIVE
    lnr = 0.5f * native_log(SUMSQ(in));
#else
    lnr = 0.5f * log(SUMSQ(in));
#endif
    va = M_TAU  / cpow.x;
    vc = cpow.y / cpow.x;
    vd = cpow.z / cpow.x;
    ang = vc * aa + vd * lnr + va * floor(cpow.x * rng_next_float(state));
#if USE_NATIVE
    mm = w * native_exp(vc * lnr - vd * aa);
#else
    mm = w * exp(vc * lnr - vd * aa);
#endif
    sincos_fast(ang, &sa, &ca);

    return mm * (float2)(ca, sa);
}
// ----------------------------
// 058 VAR EDISC
// ----------------------------
static float2 CL_V_EDISC(__private const float2 in, 
                        __private const float w
                        )
{
    float tmp, tmp2, r1, r2, xmax, aa1, aa2, ww, snv, csv, snhu, cshu;

    tmp  = SUMSQ(in) + 1.0f;
    tmp2 = 2.0f * in.x;
#if USE_NATIVE
    r1 = native_sqrt(tmp + tmp2);
    r2 = native_sqrt(tmp - tmp2);
#else
    r1 = sqrt(tmp + tmp2);
    r2 = sqrt(tmp - tmp2);
#endif
    xmax = Zeps((r1 + r2) * 0.5f);
#if USE_NATIVE
    float t = native_sqrt(xmax - 1.0f);
    aa1 = native_log(xmax + t);
#else
    float t = sqrt(xmax - 1.0f);
    aa1 = log(xmax + t);
#endif
    aa2 = -acos(in.x / xmax);
    ww = w * 0.086424247393025485907f;  // precomputed 1/11.57034632

    sincos_fast(aa1, &snv, &csv);

#if USE_NATIVE
    float e = native_exp(aa2);
    float ei = native_recip(e);
#else
    float e = exp(aa2);
    float ei = 1.0f / e;
#endif
    snhu = 0.5f * (e - ei);
    cshu = 0.5f * (e + ei);

    snv = (in.y > 0.0f) ? -snv : snv;

    return ww * (float2)(
        cshu * csv, 
        snhu * snv
    );
}
// ----------------------------
// 059 VAR EDISC
// ----------------------------
static float2 CL_V_ELLIPTIC(__private const float2 in, 
                            __private const float w
                            )
{
    float x2, sq, u, v, xmaxm1, a, ssx, weightDivPiDiv2;

    x2 = 2.0f * in.x;
    sq = SUMSQ(in);
    u = sq + x2;
    v = sq - x2;

    xmaxm1 = 0.5f * (Sqrt1pm1(u) + Sqrt1pm1(v));
    a = in.x / (1.0f + xmaxm1);
#if USE_NATIVE
    ssx = xmaxm1 > 0.0f ? native_sqrt(xmaxm1) : 0.0f;
#else
    ssx = xmaxm1 > 0.0f ? sqrt(xmaxm1) : 0.0f;
#endif

    float wscale = w * (2.0f / M_PI);
    float logterm = log1p(xmaxm1 + ssx);
    float y = copysign(wscale * logterm, in.y);

    return (float2)(
        wscale * asin(clamp(a, -1.0f, 1.0f)),
        y
    );
}
// ----------------------------
// 060 VAR NOISE
// ----------------------------
static float2 CL_V_NOISE(__private const float2 in, 
                        __private const float w, 
                        __private x128_state_t* state
                        )
{
    float tmpr, sr, cr, r;

    tmpr = rng_next_float(state) * M_TAU;
    sincos_fast(tmpr, &sr, &cr);
    r = w * rng_next_float(state);

    return r * in * (float2)(cr, sr);
}
// ----------------------------
// 061 VAR ESCHER
// ----------------------------
static float2 CL_V_ESCHER(__private const float2 in, 
                        __private const float w, 
                        __private const float beta  // beta
                        )
{
    float aa, lnr, seb, ceb, vc, vd, mm, nn, sn, cn;
    
    aa = ATANYX(in);
#if USE_NATIVE
    lnr = 0.5f * native_log(SUMSQ(in));
#else
    lnr = 0.5f * log(SUMSQ(in));
#endif
    sincos_fast(beta, &seb, &ceb);
    vc = 0.5f * (1.0f + ceb);
    vd = 0.5f * seb;
#if USE_FMA
    float exp_arg = fma(vc, lnr, -vd * aa);
#else
    float exp_arg = vc * lnr - vd * aa
#endif
#if USE_NATIVE
    mm = w * native_exp(exp_arg);
#else
    mm = w * exp(exp_arg);
#endif
#if USE_FMA
    nn = fma(vc, aa, vd * lnr);
#else
    nn = vc * aa + vd * lnr;
#endif
    sincos_fast(nn, &sn, &cn);

    return mm * (float2)(cn, sn);
}
// ----------------------------
// 062 VAR FOCI
// ----------------------------
static float2 CL_V_FOCI(__private const float2 in, 
                        __private const float w
                        )
{
    float expx, expnx, sn, cn, tmp;

#if USE_NATIVE
    expx = 0.5f * native_exp(in.x);
    expnx = 0.25f * native_recip(Zeps(expx));
#else
    expx = 0.5f * exp(in.x);
    expnx = 0.25f * (1.0f / Zeps(expx));
#endif
    sincos_fast(in.y, &sn, &cn);
#if USE_NATIVE
    tmp = w * native_recip(Zeps(expx + expnx - cn));
#else
    tmp = w * (1.0f / Zeps(expx + expnx - cn));
#endif

    return tmp * (float2)(
        expx - expnx, 
        sn
    );

}
// ----------------------------
// 063 VAR LAZYSUSAN
// ----------------------------
static float2 CL_V_LAZYSUSAN(__private const float2 in, 
                            __private const float w, 
                            __private const float4 lazysusan,   // spin, twist, space
                            __private const float2 lazy         // x, y
                        )
{
    float xx, yy, r, sa, ca, a;

    xx = in.x - lazy.x;
    yy = in.y + lazy.y;
    r = SQRT((float2)(xx, yy));
    if(r < w){
        a = ATANYX((float2)(xx, yy)) + lazysusan.x + lazysusan.y * (w - r);
        sincos_fast(a, &sa, &ca);
        r = w * r;

        return r * (float2)(
            ca + lazy.x, 
            sa - lazy.y
        );
    }
    else{
        r = w * (1.0 + lazysusan.z / r);

        return r * (float2)(
            xx + lazy.x, 
            yy - lazy.y
        );
    }
}
// ----------------------------
// 064 VAR LOONIE
// ----------------------------
static float2 CL_V_LOONIE( __private const float2 in, 
                        __private const float w
                        )
{
    float r, r2, w2;

    r2 = SUMSQ(in);
    w2 = w * w;
    if(r2 < w2){
#if USE_NATIVE
        r = w * native_sqrt(w2 / r2 - 1.0f);
#else
        r = w * sqrt(w2 / r2 - 1.0f);
#endif
        return r * in;
    }
    else{
        return w * in;
    }
}
// ----------------------------
// 065 VAR PREBLUR
// Not dispached but hard coded inside the Chaos Game instead
// ----------------------------
static float2 CL_V_PREBLUR(__private const float w, 
                        __private x128_state_t* state
                        )
{
    float rnd1, rndA, rndG, sa, ca;
    
    rndA = rng_next_float(state) * M_TAU;
    rndG = w * (rng_next_float(state) + 
                rng_next_float(state) + 
                rng_next_float(state) + 
                rng_next_float(state) - 
                2.0f
                );
    sincos_fast(rndA, &sa, &ca);

    return rndG * (float2)(ca, sa);
}
// ----------------------------
// 066 VAR MODULUS
// ----------------------------
static float2 CL_V_MODULUS(__private const float2 in, 
                        __private const float w, 
                        __private const float2 modulus  // x, y
                        )
{
    float2 period, r;

    period = 2.0f * modulus;
    r = in + modulus;
    r -= period * floor(r / period);

    return w * (r - modulus);
}
// ----------------------------
// 067 VAR OSCOPE
// ----------------------------
static float2 CL_V_OSCOPE( __private const float2 in, 
                        __private const float w, 
                        __private const float4 oscope   // frequency, amplitude, damping, separation
                        )
{
    float tpf, absx, cosval, decay, t, cond;

    tpf = M_TAU * oscope.x;
    absx = fabs(in.x);
#if USE_NATIVE
    cosval = native_cos(tpf * in.x);
    decay = (oscope.z == 0.0f) ? 1.0f : native_exp(-absx * oscope.z);
#else
    cosval = cos(tpf * in.x);
    decay = (oscope.z == 0.0f) ? 1.0f : exp(-absx * oscope.z);
#endif
    t = oscope.y * decay * cosval + oscope.w;

    float2 flipped = w * (float2)(in.x, -in.y);
    float2 normal  = w * in;

    cond = (fabs(in.y) <= t) ? 1.0f : 0.0f; 
    return normal * (1.0f - cond) + flipped * cond;
}
// ----------------------------
// 068 VAR POLAR2
// ----------------------------
static float2 CL_V_POLAR2(__private const float2 in, 
                        __private const float w
                        )
{
    float p2v = w / M_PI;
#if USE_NATIVE
    return (float2)(
        p2v * ATAN(in), 
        (0.5f * p2v) * native_log(SUMSQ(in))
    );
#else
    return (float2)(
        p2v * ATAN(in), 
        (0.5f * p2v) * log(SUMSQ(in))
    );
#endif
}
// ----------------------------
// 069 VAR POPCORN2
// ----------------------------
static float2 CL_V_POPCORN2(__private const float2 in, 
                            __private const float w, 
                            __private const float pop2c,    // c
                            __private const float2 pop2     // x, y
                            )
{
#if USE_NATIVE
    return w * (in + pop2 * (float2)(
        native_sin(SafeTan(in.y * pop2c)), 
        native_sin(SafeTan(in.x * pop2c))
        )
    );
#else
    return w * (in + pop2 * (float2)(
        sin(SafeTan(in.y * pop2c)), 
        sin(SafeTan(in.x * pop2c))
        )
    );
#endif
}
// ----------------------------
// 070 VAR SCRY
// ----------------------------
static float2 CL_V_SCRY(__private const float2 in, 
                        __private const float w
                        )
{
    float t, r;

    t = SUMSQ(in);
#if USE_NATIVE
    float val = (SQRT(in) * (t + native_recip(Zeps(w))));
    r = native_recip(val);
#else
    float val = (SQRT(in) * (t + 1.0f / Zeps(w)));
    r = 1.0f / val;
#endif

    return r * in;
}
// ----------------------------
// 071 VAR SEPARATION
// ----------------------------
static float2 CL_V_SEPARATION(__private const float2 in, 
                            __private const float w, 
                            __private const float2 sep, // x, y 
                            __private const float2 ins  // inside_x, inside_y
                            )
{
    float sx2, sy2, x, y;

    sx2 = sep.x * sep.x;
    sy2 = sep.y * sep.y;
#if USE_NATIVE
    float sqrt_sx2 = native_sqrt(in.x * in.x + sx2);
    float sqrt_sy2 = native_sqrt(in.y * in.y + sy2);
#else
    float sqrt_sx2 = sqrt(in.x * in.x + sx2);
    float sqrt_sy2 = sqrt(in.y * in.y + sy2);
#endif
    float insx = in.x * ins.x;
    float insy = in.y * ins.y;
    if(in.x > 0.0f) x = w * (sqrt_sx2 - insx);
    else x = w * -(sqrt_sx2 + insx);
    if(in.y > 0.0f) y = w * (sqrt_sy2 - insy);
    else y = w * -(sqrt_sy2 + insy);

    return (float2)(x, y);
}
// ----------------------------
// 072 VAR SPLIT
// ----------------------------
static float2 CL_V_SPLIT(__private const float2 in, 
                        __private const float w, 
                        __private const float2 split    // x, y
                        )
{
#if USE_NATIVE
    float2 scaled, t, t2, cos_approx, eps, mask;

    scaled = in * split * 3.141592653589793238462f;
    t = fmod(scaled, 2.0f * 3.141592653589793238462f);
    t2 = t * t;
    cos_approx = 1.0f + 
                t2 * (-0.5f + 
                t2 * (0.0416666667f + 
                t2 * (-0.0013888889f + 
                t2 * (0.0000248016f + 
                t2 * (-2.7557319e-7f + 
                t2 * 2.0876757e-9f)))));

    eps = (float2)(0.0005f, 0.0005f); 
    mask = sign(cos_approx + eps);

    return w * in * mask.yx;
#else
    float x, y;

    if(cos(in.x * split.x * M_PI) >= 0) y = w * in.y;
    else y = w * -in.y;
    if(cos(in.y * split.y * M_PI) >= 0) x = w * in.x;
    else x = w * -in.x;

    return (float2)(x, y);
#endif
}
// ----------------------------
// 073 VAR SPLITS
// ----------------------------
static float2 CL_V_SPLITS(__private const float2 in, 
                        __private const float w, 
                        __private const float2 splits   // x, y
                        )
{
    float2 s = 2.0f * step(0.0f, in) - 1.0f;
    return w * (in + s * splits);
}
// ----------------------------
// 074 VAR STRIPES
// ----------------------------
static float2 CL_V_STRIPES(__private const float2 in, 
                        __private const float w, 
                        __private const float2 stripes  // space, warp
                        )
{
    float roundx, offsetx;

    roundx = floor(in.x + 0.5f);
    offsetx = in.x - roundx;
#if USE_FMA
    return w * (float2)(
        fma(offsetx, (1.0f - stripes.x), roundx), 
        fma(offsetx, offsetx * stripes.y, in.y)
    );
#else
    return w * (float2)(
        (offsetx * (1.0f - stripes.x) + roundx), 
        (in.y + offsetx * offsetx * stripes.y)
    );
#endif
}
// ----------------------------
// 075 VAR WEDGE
// ----------------------------
static float2 CL_V_WEDGE(__private const float2 in, 
                        __private const float w, 
                        __private const float4 wedge    // swirl, angle, hole, count
                        )
{
    float r, a, c, m_CompFac;

    m_CompFac = 1 - wedge.y * wedge.w * M_1_2PI;
    r = SQRT(in);
    a = ATANYX(in) + wedge.x * r;
    float tmp = (wedge.w * a + M_PI) * M_1_2PI;
    c = (float)((int)(tmp - (tmp < 0.0f ? 1.0f : 0.0f)));
    a = a * m_CompFac + c * wedge.y;
    r = w * (r + wedge.z);
#if USE_NATIVE
    return r * (float2)(
        native_cos(a), 
        native_sin(a)
    );
#else
    return r * (float2)(
        cos(a), 
        sin(a)
    );
#endif
}
// ----------------------------
// 076 VAR WEDGEJULIA
// ----------------------------
static float2 CL_V_WEDGEJULIA(__private const float2 in, 
                            __private const float w, 
                            __private x128_state_t* state, 
                            __private const float4 wedgejulia   // power, angle, dist, count
                            )
{
    float wedgeJulia_cf, wedgeJulia_rN, wedgeJulia_cn, rr, t_rnd, a, cc, sa, ca;

    // TO DO: compute in vex land
    // I did but made no difference and I prefer to keep it here
    // so the wrangle core node in Houdini's land remain more performant.
    wedgeJulia_cf = 1.0 - wedgejulia.y * wedgejulia.w * M_1_2PI;
    wedgeJulia_rN = fabs(wedgejulia.x);
    wedgeJulia_cn = wedgejulia.z / wedgejulia.x / 2.0;
    
#if USE_NATIVE
    rr = w * native_powr(SUMSQ(in), wedgeJulia_cn);
#else
    rr = w * powr(SUMSQ(in), wedgeJulia_cn);
#endif
    t_rnd = (int)((wedgeJulia_rN) * rng_next_float(state));
    a = (ATANYX(in) + M_TAU * t_rnd) / wedgejulia.x;
#if USE_FMA
    float tmp = fma(wedgejulia.w, a, (float)M_PI) * M_1_2PI;
    cc = (float)((int)(tmp - (tmp < 0.0f ? 1.0f : 0.0f)));
#else
    cc = floor( (wedgejulia.w * aa + M_PI) * M_1_2PI );
#endif
    a = a * wedgeJulia_cf + cc * wedgejulia.y;
    sincos_fast(a, &sa, &ca);

    return rr * (float2)(ca, sa);
}
// ----------------------------
// 077 VAR WEDGESPH
// ----------------------------
static float2 CL_V_WEDGESPH(__private const float2 in, 
                            __private const float w, 
                            __private const float4 wedgesph // swirl, angle, hole, count
                            )
{
    float r, a, cc, comp_fac, sa, ca;

#if USE_NATIVE
    r = native_recip(Zeps(SQRT(in)));
#else
    r = 1.0f / Zeps(SQRT(in));
#endif
    a = ATANYX(in) + wedgesph.x * r;
#if USE_FMA
    float tmp = fma(wedgesph.w, a, (float)M_PI) * M_1_2PI;
    cc = (float)((int)(tmp - (tmp < 0.0f ? 1.0f : 0.0f)));
#else
    cc = floor( (wedgesph.w * a + M_PI) * M_1_2PI );
#endif
    comp_fac = 1.0f - wedgesph.y * wedgesph.w * M_1_2PI;
#if USE_FMA
    a = fma(a, comp_fac, cc * wedgesph.y);
#else
    a = a * comp_fac + cc * wedgesph.y;
#endif
    sincos_fast(a, &sa, &ca);
    r = w * (r + wedgesph.z);

    return r * (float2)(ca, sa);
}
// ----------------------------
// 078 VAR WHORL
// ----------------------------
static float2 CL_V_WHORL(__private const float2 in, 
                        __private const float w, 
                        __private const float2 whorl    // inside, outside
                        )
{
    float r, a, sa, ca;

    r = SQRT(in);
    float2 Owmr = whorl / (w - r);
    float base = ATANYX(in);
    a = base + select(Owmr.y, Owmr.x, r < w);
    sincos_fast(a, &sa, &ca);
    
    return w * r * (float2)(ca, sa);
}
// ----------------------------
// 079 VAR WAVES2
// ----------------------------
static float2 CL_V_WAVES2(__private const float2 in, 
                        __private const float w, 
                        __private const float2 scl,     // scale x, scale y
                        __private const float2 freq     // frequency x, frequency y
                        )
{
#if USE_NATIVE
    return w * (in + scl * native_sin(in.yx * freq));
#else
    return w * (in + scl * sin(in.yx * freq));
#endif
}
// ----------------------------
// 080 VAR EXP
// ----------------------------
static float2 CL_V_EXP(__private const float2 in, 
                    __private const float w
                    )
{
    float expe, sy, cy;

#if USE_NATIVE
    expe = w * native_exp(in.x);
#else
    expe = w * exp(in.x);
#endif
    sincos_fast(in.y, &sy, &cy);

    return expe * (float2)(cy, sy);
}
// ----------------------------
// 081 VAR LOG
// ----------------------------
static float2 CL_V_LOG(__private const float2 in, 
                    __private const float w
                    )
{
#if USE_NATIVE
    return w * (float2)(
        0.5 * native_log(SUMSQ(in)), 
        ATANYX(in)
    );
#else
    return w * (float2)(
        0.5 * log(SUMSQ(in)), 
        ATANYX(in)
    );
#endif
}
// ----------------------------
// 082 VAR SIN
// ----------------------------
static float2 CL_V_SIN(__private const float2 in, 
                    __private const float w, 
                    __private const int F3C
                    )
{
    float2 xy = in * (F3C ? 1.0f : (float)M_PI_2);

    #if USE_NATIVE
    return w * (float2)(
        native_sin(xy.x) * cosh(xy.y),
        native_cos(xy.x) * sinh(xy.y)
    );
    #else
    return w * (float2)(
        sin(xy.x) * cosh(xy.y),
        cos(xy.x) * sinh(xy.y)
    );
    #endif
}
// ----------------------------
// 083 VAR COS
// ----------------------------
static float2 CL_V_COS(__private const float2 in, 
                    __private const float w, 
                    __private const int F3C
                    )
{
    float2 xy = in * (F3C ? 1.0f : (float)M_PI_2);

    #if USE_NATIVE
    return w * (float2)(
        native_cos(xy.x)  * cosh(xy.y),
        -native_sin(xy.x) * sinh(xy.y)
    );
    #else
    return w * (float2)(
        cos(xy.x)  * cosh(xy.y),
        -sin(xy.x) * sinh(xy.y)
    );
    #endif
}
// ----------------------------
// 084 VAR TAN
// ----------------------------
static float2 CL_V_TAN(__private const float2 in, 
                    __private const float w, 
                    __private const int F3C
                    )
{
    float tansin, tancos, tansinh, tancosh, den;

    if(F3C){
        sincos_fast(2.0f * in.x, &tansin, &tancos);
        float iny2 = 2.0f * in.y;
        tansinh = sinh(iny2);
        tancosh = cosh(iny2);
    #if USE_NATIVE
        den = w * native_recip(Zeps(tancos + tancosh));
    #else
        den = w / Zeps(tancos + tancosh);
    #endif
        return den * (float2)(tansin, tansinh);
    }
    else{
        float2 xy = in * (float)M_PI_2;

    #if USE_NATIVE
        den = w / Zeps(native_cos(xy.x) + cosh(xy.y));
        return den * (float2)(
            native_sin(xy.x), 
            sinh(xy.y)
        );
    #else
        den = w / Zeps(cos(xy.x) + cosh(xy.y));
        return den * (float2)(
            sin(xy.x), 
            sinh(xy.y)
        );
    #endif
    }
}
// ----------------------------
// 085 VAR SEC
// ----------------------------
static float2 CL_V_SEC(__private const float2 in, 
                    __private const float w, 
                    __private const int F3C
                    )
{
    float secsin, seccos, secsinh, seccosh, den;

    float2 xy = in * (F3C ? 1.0f : (float)M_PI);

    sincos_fast(xy.x, &secsin, &seccos);
    secsinh = sinh(xy.y);
    seccosh = cosh(xy.y);
    float2 xy2 = xy * 2.0f;
#if USE_NATIVE
    den = w * (2.0f / Zeps(native_cos(xy2.x) + cosh(xy2.y)));
#else
    den = w * (2.0f / Zeps(cos(xy2.x) + cosh(xy2.y)));
#endif

    return den * (float2)(
        seccos * seccosh, 
        secsin * secsinh
    );
}
// ----------------------------
// 086 VAR CSC
// ----------------------------
static float2 CL_V_CSC(__private const float2 in, 
                    __private const float w, 
                    __private const int F3C
                    )
{
    float cscsin, csccos, cscsinh, csccosh, den;

    float2 xy = in * (F3C ? 1.0f : (float)M_PI_2);

    sincos_fast(xy.x, &cscsin, &csccos);
    cscsinh = sinh(xy.y);
    csccosh = cosh(xy.y);
    float2 xy2 = xy * 2.0f;
#if USE_NATIVE
    den = w * 2.0f / Zeps(cosh(xy2.y) - native_cos(xy2.x));
#else
    den = w * 2.0f / Zeps(cosh(xy2.y) - cos(xy2.x));
#endif

    float y_sign = F3C ? -1.0f : 1.0f;

    return den * (float2)(
        cscsin * csccosh, 
        y_sign * csccos * cscsinh
    );
}
// ----------------------------
// 087 VAR COT
// ----------------------------
static float2 CL_V_COT(__private const float2 in, 
                    __private const float w, 
                    __private const int F3C
                    )
{
    float cotsin, cotcos, cotsinh, cotcosh, den;

    float2 xy = in * (F3C ? 2.0f : (float)M_PI_2);

    sincos_fast(xy.x, &cotsin, &cotcos);
    cotsinh = sinh(xy.y);
    cotcosh = cosh(xy.y);
    den = w / (cotcosh - cotcos);

    float y_sign = F3C ? -1.0f : 1.0f;

    return den * (float2)(
        cotsin, 
        y_sign * cotsinh);
}
// ----------------------------
// 088 VAR SINH
// ----------------------------
static float2 CL_V_SINH(__private const float2 in, 
                    __private const float w, 
                    __private const int F3C
                    )
{
    float sinhsin, sinhcos, sinhsinh, sinhcosh;

    float2 xy = in * (F3C ? 1.0f : (float)M_PI_4);

    sincos_fast(xy.y, &sinhsin, &sinhcos);
    sinhsinh = sinh(xy.x);
    sinhcosh = cosh(xy.x);

    return w * (float2)(
        sinhsinh * sinhcos, 
        sinhcosh * sinhsin
    );
}
// ----------------------------
// 089 VAR COSH
// ----------------------------
static float2 CL_V_COSH(__private const float2 in, 
                    __private const float w, 
                    __private const int F3C
                    )
{
    float coshsin, coshcos, coshsinh, coshcosh;

    float2 xy = in * (F3C ? 1.0f : (float)M_PI_2);

    sincos_fast(xy.y, &coshsin, &coshcos);
    coshsinh = sinh(xy.x);
    coshcosh = cosh(xy.x);

    return w * (float2)(
        coshcosh * coshcos, 
        coshsinh * coshsin
    );
}
// ----------------------------
// 090 VAR TANH
// ----------------------------
static float2 CL_V_TANH(__private const float2 in, 
                    __private const float w, 
                    __private const int F3C
                    )
{
    float tanhsin, tanhcos, tanhsinh, tanhcosh, den;

    float2 xy = in * (F3C ? 2.0f : (float)M_PI_2);

    sincos_fast(xy.y, &tanhsin, &tanhcos);
    tanhsinh = sinh(xy.x);
    tanhcosh = cosh(xy.x);
#if USE_NATIVE
    den = native_recip(Zeps(tanhcos + tanhcosh));
#else
    den = 1.0f / Zeps(tanhcos + tanhcosh);
#endif

    return w * den * (float2)(tanhsinh, tanhsin);
}
// ----------------------------
// 091 VAR TANH
// ----------------------------
static float2 CL_V_SECH(__private const float2 in, 
                    __private const float w, 
                    __private const int F3C
                    )
{
    float sechsin, sechcos, sechsinh, sechcosh, den;

    float2 xy = in * (F3C ? 1.0f : (float)M_PI_4);

    sincos_fast(xy.y, &sechsin, &sechcos);
    sechsinh = sinh(xy.x);
    sechcosh = cosh(xy.x);

    den = w * 2.0f / Zeps(cos(2.0f * xy.y) + cosh(2.0f * xy.x));

    float y_sign = F3C ? -1.0f : 1.0f;

    return den * (float2)(
        sechcos * sechcosh, 
        y_sign * sechsin * sechsinh
    );
}
// ----------------------------
// 092 VAR CSCH
// ----------------------------
static float2 CL_V_CSCH(__private const float2 in, 
                    __private const float w, 
                    __private const int F3C
                    )
{
    float cschsin, cschcos, cschsinh, cschcosh, den;

    float2 xy = in * (F3C ? 1.0f : (float)M_PI_4);

    float2 in2 = 2.0f * xy;
    sincos_fast(xy.y, &cschsin, &cschcos);
    cschsinh = sinh(xy.x);
    cschcosh = cosh(xy.x);
#if USE_NATIVE
    den = w * 2.0f / Zeps(cosh(in2.x) - native_cos(in2.y));
#else
    den = w * 2.0f / Zeps(cosh(in2.x) - cos(in2.y));
#endif

    float y_sign = F3C ? -1.0f : 1.0f;

    return den * (float2)(
        cschsinh * cschcos, 
        y_sign * cschcosh * cschsin
    );
}
// ----------------------------
// 093 VAR COTH
// ----------------------------
static float2 CL_V_COTH(__private const float2 in, 
                    __private const float w, 
                    __private const int F3C
                    )
{
    float cothsin, cothcos, cothsinh, cothcosh, den;

    float2 xy = in * (F3C ? 2.0f : (float)M_PI_2);

    sincos_fast(xy.y, &cothsin, &cothcos);
    cothsinh = sinh(xy.x);
    cothcosh = cosh(xy.x);
    den = w / Zeps(cothcosh - cothcos);

    return den * (float2)(cothsinh, cothsin);
}
// ----------------------------
// 094 VAR AUGER
// ----------------------------
static float2 CL_V_AUGER(__private const float2 in, 
                    __private const float w, 
                    __private const float4 auger    // frequency, scale, symmetry, weight
                    )
{
    float s, t, dy, dx;

    float m_HalfScale = auger.y / 2.0f;
    float2 sta = auger.x * in;
#if USE_NATIVE
    s = native_sin(sta.x);
    t = native_sin(sta.y);
#else
    s = sin(sta.x);
    t = sin(sta.y);
#endif
    dx = in.x + auger.w * (m_HalfScale * t + fabs(in.x) * t);
    dy = in.y + auger.w * (m_HalfScale * s + fabs(in.y) * s);

    return w * (float2)((
        in.x + auger.z * (dx - in.x)), 
        dy
    );
}
// ----------------------------
// 095 VAR FLUX
// ----------------------------
static float2 CL_V_FLUX(__private const float2 in, 
                        __private const float w, 
                        __private const float spread    // spread
                        )
{
    float r1, r2, xpw, xmw, avgr, avga, sa, ca;

    xpw = in.x + w;
    xmw = in.x - w;

    float iny2 = in.y * in.y;
    r1 = iny2 + xpw * xpw;
    r2 = iny2 + xmw * xmw;

#if USE_NATIVE
    avgr = w * (2.0f + spread) * native_sqrt(native_sqrt(r1)) * native_rsqrt(native_sqrt(r2));
#else
    avgr = w * (2.0f + spread) * sqrt(sqrt(r1)) * rsqrt(sqrt(r2));
#endif
    avga = 0.5f * (atan2(in.y, xmw) - atan2(in.y, xpw));

    sincos_fast(avga, &sa, &ca);

    return avgr * (float2)(ca, sa);
}
// ----------------------------
// 096 VAR MOBIUS
// ----------------------------
static float2 CL_V_MOBIUS(__private const float2 in, 
                        __private const float w, 
                        __private const float4 re,  // reA, reB, reC, reD -> real
                        __private const float4 im   // imA, imB, imC, imD -> imaginary
                        )
{
    float reu, imu, rev, imv, inv;

    reu = re.x * in.x - im.x * in.y + re.y;
    imu = re.x * in.y + im.x * in.x + im.y;

    rev = re.z * in.x - im.z * in.y + re.w;
    imv = re.z * in.y + im.z * in.x + im.w;

#if USE_NATIVE
    inv = native_rsqrt(rev*rev + imv*imv);
#else
    inv = rsqrt(rev*rev + imv*imv);
#endif
    inv *= inv;
    inv *= w;

    return inv * (float2)(
        reu * rev + imu * imv,
        imu * rev - reu * imv
    );
}
// ----------------------------
// 097 VAR CURVE
// ----------------------------
static float2 CL_V_CURVE(__private const float2 in, 
                        __private const float w, 
                        __private const int F3C,  
                        __private const float2 lenght,      // lenght_x, lenght_y
                        __private const float2 amplitude    // amplitude_x, amplitude_y
                        )
{
    float lx, ly;

    if(F3C){
    #if USE_NATIVE
        lx = native_recip(fmax((lenght.x * lenght.x), 1e-20f));
        ly = native_recip(fmax((lenght.y * lenght.y), 1e-20f));
        return w * (float2)(
            in.x + amplitude.x * native_exp(-in.y * in.y * lx), 
            in.y + amplitude.y * native_exp(-in.x * in.x * ly)
        );
    #else
        lx = 1.0f / fmax((lenght.x * lenght.x), 1e-20f);
        ly = 1.0f / fmax((lenght.y * lenght.y), 1e-20f);
        return w * (float2)(
            in.x + amplitude.x * exp(-in.y * in.y * lx), 
            in.y + amplitude.y * exp(-in.x * in.x * ly)
        );
    #endif
    }
    else{
    #if USE_NATIVE
        return w * (float2)(
            in.x + amplitude.x * native_exp(-in.y * in.y / Zeps(lenght.x)),
            in.y + amplitude.y * native_exp(-in.x * in.x / Zeps(lenght.y))
        );
    #else
        return w * (float2)(
            in.x + amplitude.x * exp(-in.y * in.y / Zeps(lenght.x)),
            in.y + amplitude.y * exp(-in.x * in.x / Zeps(lenght.y))
        );
    #endif
    }
}
// ----------------------------
// 098 VAR PERSPECTIVE
// ----------------------------
static float2 CL_V_PERSPECTIVE(__private const float2 in, 
                            __private const float w, 
                            __private const float2 presp    // angle, distance
                            )
{
    float t, ang, vsin, vfcos;

    ang = presp.x * M_PI_2;
#if USE_NATIVE
    vsin = native_sin(ang);
    vfcos = presp.y * native_cos(ang);
#else
    vsin = sin(ang);
    vfcos = presp.y * cos(ang);
#endif
    t = w / (presp.y - in.y * vsin);

    return t * (float2)(
        presp.y * in.x, 
        vfcos * in.y
    );
}
// ----------------------------
// 099 VAR BWRAPS
// ----------------------------
static float2 CL_V_BWRAPS(__private const float2 in, 
                        __private const float w, 
                        __private const float4 bwraps,  // size, space, gain
                        __private const float2 twist    // in_twist, out_twist
                        )
{
    float g2, r2, rfactor, max_bubble, vx, vy, cx, cy, lx, ly, r, theta, sa, ca;

    // precalc
    float radius = 0.5f * (bwraps.x / (1.0f + bwraps.y * bwraps.y));

#if USE_NATIVE
    g2 = native_sqrt(fabs(bwraps.z)) / bwraps.x + 1e-6f;
#else
    g2 = sqrt(fabs(bwraps.z)) / bwraps.x + 1e-6f;
#endif

    max_bubble = g2 * radius;

#if USE_NATIVE
    float den = 0.25f * max_bubble * max_bubble + 1.0f;
    max_bubble = (max_bubble > 2.0f) ? 1.0f : max_bubble * native_recip(den);
#else
    max_bubble = (max_bubble > 2.0f) ? 1.0f : max_bubble * 1.0f / ((max_bubble * max_bubble) / 4.0f + 1.0f);
#endif

    r2 = radius * radius;
    rfactor = radius / max_bubble;

    if (bwraps.x == 0.0f)
    {
        return w * in;
    }
    else
    {
        vx = in.x;
        vy = in.y;

        cx = (floor(vx / bwraps.x) + 0.5f) * bwraps.x;
        cy = (floor(vy / bwraps.x) + 0.5f) * bwraps.x;

        lx = vx - cx;
        ly = vy - cy;

        float l2 = lx * lx + ly * ly;

        if (l2 > r2)
        {
            return w * in;
        }
        else
        {
            lx *= g2;
            ly *= g2;
            l2 = lx * lx + ly * ly;

            r = rfactor / Zeps(l2 / 4.0f + 1.0f);

            lx *= r;
            ly *= r;
            l2 = lx * lx + ly * ly;

            r = l2 / r2;

        #if USE_FMA
            theta = fma(twist.x, (1.0f - r), twist.y * r);
        #else
            theta = twist.x * (1.0f - r) + twist.y * r;
        #endif

            sincos_fast(theta, &sa, &ca);

        #if USE_FMA
            vx = fma(sa, ly, fma(ca, lx, cx));
            vy = fma(-sa, lx, fma(ca, ly, cy));
        #else
            vx = cx + ca * lx + sa * ly;
            vy = cy - sa * lx + ca * ly;
        #endif

            return w * (float2)(vx, vy);
        }
    }
}
// ----------------------------
// 100 VAR HEMISPHERE
// ----------------------------
static float2 CL_V_HEMISPHERE(__private const float2 in, 
                            __private const float w 
                            )
{
#if USE_NATIVE
    float t = w * native_rsqrt(SUMSQ(in) + 1.0f);
#else
    float t = w * rsqrt(SUMSQ(in) + 1.0f);
#endif

    return t * in;
}
// ----------------------------
// 101 VAR POLYNOMIAL
// ----------------------------
static float2 CL_V_POLYNOMIAL(__private const float2 in, 
                            __private const float w, 
                            __private const float2 powr,    // pow_x, pow_y
                            __private const float2 lc,      // lc_x, lc_y
                            __private const float2 sc       // sc_x, sc_y
                            )
{
    float xp, yp;

    float abs_w = fabs(w);
    float2 in_abs_w = abs_w * fabs(in);

#if USE_NATIVE
    xp = native_powr(abs_w * in_abs_w.x, powr.x);
    yp = native_powr(abs_w * in_abs_w.y, powr.y);
#else
    xp = pow(abs_w * in_abs_w.x, powr.x);
    yp = pow(abs_w * in_abs_w.y, powr.y);
#endif
#if USE_FMA
    return (float2)(
        fma(xp, sgn(in.x), fma(lc.x, in.x, sc.x)), 
        fma(yp, sgn(in.y), fma(lc.y, in.y, sc.y))
    );
#else
    return (float2)(
        xp * sgn(in.x) + lc.x * in.x + sc.x, 
        yp * sgn(in.y) + lc.y * in.y + sc.y
    );
#endif
}
// ----------------------------
// 102 VAR CROP
// ----------------------------
static float2 CL_V_CROP(__private const float2 in, 
                        __private const float w, 
                        __private x128_state_t* state, 
                        __private const float4 ltrb,    // left, top, right, bottom
                        __private const float2 az       // area, zero
                        )
{
    float x0, x1, y0, y1, rx, ry, w2, h2;
    int left, right, top, bottom;

    float2 p = in;

    x0 = fmin(ltrb.x, ltrb.z);
    x1 = fmax(ltrb.x, ltrb.z);
    y0 = fmin(ltrb.y, ltrb.w);
    y1 = fmax(ltrb.y, ltrb.w);

    w2 = (x1 - x0) * (0.5f * az.x);
    h2 = (y1 - y0) * (0.5f * az.x);

    rx = rng_next_float(state);
    ry = rng_next_float(state);

    // conditions
    left   = p.x < x0;
    right  = p.x > x1;
    top    = p.y > y1;
    bottom = p.y < y0;

    // replacements
    float xL = x0 + rx * w2;
    float xR = x1 - rx * w2;
    float yB = y0 + ry * h2;
    float yT = y1 - ry * h2;

    
    p.x = left   ? xL : p.x;
    p.x = right  ? xR : p.x;
    p.y = bottom ? yB : p.y;
    p.y = top    ? yT : p.y;

    int outside = left | right | bottom | top;

    if (outside && az.y != 0.0f)
        p = (float2)(0.0f);

    return w * p;
}
// ----------------------------
// 103 VAR UNPOLAR
// ----------------------------
static float2 CL_V_UNPOLAR(__private const float2 in, 
                        __private const float w 
                        )
{
    float m_Vvar2, r, sa, ca;

    m_Vvar2 = (w / M_PI) * 0.5;
#if USE_NATIVE
    r = native_exp(in.y);
#else
    r = exp(in.y);
#endif
    sincos_fast(in.x, &sa, &ca);

    return m_Vvar2 * r * (float2)(sa, ca);
}
// ----------------------------
// 104 VAR GLYNNIA
// ----------------------------
static float2 CL_V_GLYNNIA(__private const float2 in, 
                        __private const float w, 
                        __private x128_state_t* state
                        )
{
    float r, m_V2, d, y2;

    r = SQRT(in);
    m_V2 = w * 0.7071067811865475f;

    d = r + in.x;
    y2 = in.y * in.y;

    if (r > 1.0f)
    {
        if (rng_next_float(state) > 0.5f)
        {
        #if USE_NATIVE
            float s = native_sqrt(d);
        #else
            float s = sqrt(d);
        #endif

            return (float2)(
                m_V2 * s,
                -(m_V2 / s) * in.y
            );
        }
        else
        {
        #if USE_NATIVE
            float inv = w / native_sqrt(r * (y2 + d*d));
        #else
            float inv = w / sqrt(r * (y2 + d*d));
        #endif
            return inv * (float2)(d, in.y);
        }
    }
    else
    {
        if (rng_next_float(state) > 0.5f)
        {
        #if USE_NATIVE
            float s = Zeps(native_sqrt(d));
        #else
            float s = Zeps(sqrt(d));
        #endif

            return (float2)(
                -(m_V2 * s),
                -(m_V2 / s) * in.y
            );
        }
        else
        {
        #if USE_NATIVE
            float inv = w / Zeps(native_sqrt(r * (y2 + d*d)));
        #else
            float inv = w / Zeps(sqrt(r * (y2 + d*d)));
        #endif

            return (float2)(
                -(inv * d),
                inv * in.y
            );
        }
    }
}
// ----------------------------
// 105 VAR POINT SYMMETRY
// ----------------------------
static float2 CL_V_POINT_SYMMETRY(__private const float2 in, 
                                __private const float w, 
                                __private x128_state_t* state, 
                                __private const float4 ptsym    // order, center_x, center_y
                                )
{
    float order, twoPiDivOrder, angle, dx, dy, sa, ca, x, y;

    order = Zeps(ptsym.x);
    twoPiDivOrder = M_TAU / order;
    int k = (int)(rng_next_float(state) * order);
    angle = k * twoPiDivOrder;

    float cx = ptsym.y;
    float cy = ptsym.z;
    dx = (in.x - cx) * w;
    dy = (in.y - cy) * w;
    sincos_fast(angle, &sa, &ca);
#if USE_FMA
    x = fma(dx, ca, dy * sa);
    y = fma(dy, ca, -dx * sa);
#else
    x = dx * ca + dy * sa;
    y = dy * ca - dx * sa;
#endif

    return (float2)(
        cx + x, 
        cy + y
    );
}




// ----------------------------
// CL FLAM3 variations dispatch
//
// Each iterations of the chaos game will select one variation to be applied to the incoming point/sample.
// The dispatch will take care of finding the one and execute it.
// ----------------------------

static float2 CL_V_DISPATCH(
    __private const int     type, 
    __private const float2  in, 
    __private const float   w, 
    __private const float2  y,
    __private const float2  o, 
    __private const int     F3C, 
    __private x128_state_t* state, 
    __local const float*    PRM_F, 
    __local const float2*   PRM_F2, 
    __local const float4*   PRM_F3,   // Casted as float4 instead of float3 array so it map correctly
    __local const float4*   PRM_F4 
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
        case 26:    return CL_V_BLUR(w, state);
        case 27:    return CL_V_CURL(in, w, PRM_F2[PRM_F2_IDX_CURL]);
        case 28:    return CL_V_NGON(in, w, PRM_F4[PRM_F4_IDX_NGON], PRM_F4[PRM_F4_IDX_NGON_PRECALC]);
        case 29:    return CL_V_PDJ(in, w, PRM_F4[PRM_F4_IDX_PDJW]);
        case 30:    return CL_V_BLOB(in, w, PRM_F3[PRM_F3_IDX_BLOB]);
        case 31:    return CL_V_JULIAN(in, w, state, PRM_F2[PRM_F2_IDX_JULIAN]);
        case 32:    return CL_V_JULIASCOPE(in, w, state, PRM_F2[PRM_F2_IDX_JULIASCOPE]);
        case 33:    return CL_V_GAUSSIAN_BLUR(w, state);
        case 34:    return CL_V_FAN2(in, w, PRM_F2[PRM_F2_IDX_FAN2]);
        case 35:    return CL_V_RINGS2(in, w, PRM_F[PRM_F_IDX_RINGS2VAL]);
        case 36:    return CL_V_RECTANGLES(in, w, PRM_F2[PRM_F2_IDX_RECTANGLES]);
        case 37:    return CL_V_RADIALBLUR(in, w, state, PRM_F[PRM_F_IDX_RADIALBLUR]);
        case 38:    return CL_V_PIE(w, state, PRM_F3[PRM_F3_IDX_PIE]);
        case 39:    return CL_V_ARCH(in, w, state);
        case 40:    return CL_V_TANGENT(in, w);
        case 41:    return CL_V_SQUARE(w, state);
        case 42:    return CL_V_RAYS(in, w, state);
        case 43:    return CL_V_BLADE(in, w, state);
        case 44:    return CL_V_SECANT2(in, w);
        case 45:    return CL_V_TWINTRIAN(in, w, state);
        case 46:    return CL_V_CROSS(in, w, F3C);
        case 47:    return CL_V_DISC2(in, w, PRM_F2[PRM_F2_IDX_DISC2], PRM_F3[PRM_F3_IDX_DISC2_PRECALC]);
        case 48:    return CL_V_SUPERSHAPE(in, w, state, PRM_F3[PRM_F3_IDX_SUPERSHAPE], PRM_F3[PRM_F3_IDX_SUPERSHAPEN]);
        case 49:    return CL_V_FLOWER(in, w, state, PRM_F2[PRM_F2_IDX_FLOWER]);
        case 50:    return CL_V_CONIC(in, w, state, PRM_F2[PRM_F2_IDX_CONIC]);
        case 51:    return CL_V_PARABOLA(in, w, state, PRM_F2[PRM_F2_IDX_PARABOLA]);
        case 52:    return CL_V_BENT2(in, w, PRM_F2[PRM_F2_IDX_BENT2]);
        case 53:    return CL_V_BIPOLAR(in, w, PRM_F[PRM_F_IDX_BIPOLARSHIFT]);
        case 54:    return CL_V_BOARDERS(in, w, state);
        case 55:    return CL_V_BUTTERFLY(in, w);
        case 56:    return CL_V_CELL(in, w, PRM_F[PRM_F_IDX_CELLSIZE]);
        case 57:    return CL_V_CPOW(in, w, state, PRM_F3[PRM_F3_IDX_CPOW]);
        case 58:    return CL_V_EDISC(in, w);
        case 59:    return CL_V_ELLIPTIC(in, w);
        case 60:    return CL_V_NOISE(in, w, state);
        case 61:    return CL_V_ESCHER(in, w, PRM_F[PRM_F_IDX_ESCHERBETA]);
        case 62:    return CL_V_FOCI(in, w);
        case 63:    return CL_V_LAZYSUSAN(in, w, PRM_F3[PRM_F3_IDX_LAZYSUSANSTS], PRM_F2[PRM_F2_IDX_LAZYSUSAN]);
        case 64:    return CL_V_LOONIE(in, w);
        //   65:    return CL_V_PREBLUR(w, state) -> Not dispached but hard coded inside the Chaos Game instead
        case 66:    return CL_V_MODULUS(in, w, PRM_F2[PRM_F2_IDX_MODULUS]);
        case 67:    return CL_V_OSCOPE(in, w, PRM_F4[PRM_F4_IDX_OSCOPE]);
        case 68:    return CL_V_POLAR2(in, w);
        case 69:    return CL_V_POPCORN2(in, w, PRM_F[PRM_F_IDX_POPCORN2C], PRM_F2[PRM_F2_IDX_POPCORN2]);
        case 70:    return CL_V_SCRY(in, w);
        case 71:    return CL_V_SEPARATION(in, w, PRM_F2[PRM_F2_IDX_SEPARATION], PRM_F2[PRM_F2_IDX_SEPARATIONIN]);
        case 72:    return CL_V_SPLIT(in, w, PRM_F2[PRM_F2_IDX_SPLIT]);
        case 73:    return CL_V_SPLITS(in, w, PRM_F2[PRM_F2_IDX_SPLITS]);
        case 74:    return CL_V_STRIPES(in, w, PRM_F2[PRM_F2_IDX_STRIPES]);
        case 75:    return CL_V_WEDGE(in, w, PRM_F4[PRM_F4_IDX_WEDGE]);
        case 76:    return CL_V_WEDGEJULIA(in, w, state, PRM_F4[PRM_F4_IDX_WEDGEJULIA]);
        case 77:    return CL_V_WEDGESPH(in, w, PRM_F4[PRM_F4_IDX_WEDGESPH]);
        case 78:    return CL_V_WHORL(in, w, PRM_F2[PRM_F2_IDX_WHORL]);
        case 79:    return CL_V_WAVES2(in, w, PRM_F2[PRM_F2_IDX_WAVES2SCALE], PRM_F2[PRM_F2_IDX_WAVES2FREQ]);
        case 80:    return CL_V_EXP(in, w);
        case 81:    return CL_V_LOG(in, w);
        case 82:    return CL_V_SIN(in, w, F3C);
        case 83:    return CL_V_COS(in, w, F3C);
        case 84:    return CL_V_TAN(in, w, F3C);
        case 85:    return CL_V_SEC(in, w, F3C);
        case 86:    return CL_V_CSC(in, w, F3C);
        case 87:    return CL_V_COT(in, w, F3C);
        case 88:    return CL_V_SINH(in, w, F3C);
        case 89:    return CL_V_COSH(in, w, F3C);
        case 90:    return CL_V_TANH(in, w, F3C);
        case 91:    return CL_V_SECH(in, w, F3C);
        case 92:    return CL_V_CSCH(in, w, F3C);
        case 93:    return CL_V_COTH(in, w, F3C);
        case 94:    return CL_V_AUGER(in, w, PRM_F4[PRM_F4_IDX_AUGER]);
        case 95:    return CL_V_FLUX(in, w, PRM_F[PRM_F_IDX_FLUXSPREAD]);
        case 96:    return CL_V_MOBIUS(in, w, PRM_F4[PRM_F4_IDX_MOBIUSRE], PRM_F4[PRM_F4_IDX_MOBIUSIM]);
        case 97:    return CL_V_CURVE(in, w, F3C, PRM_F2[PRM_F2_IDX_CURVELENGTH], PRM_F2[PRM_F2_IDX_CURVEAMP]);
        case 98:    return CL_V_PERSPECTIVE(in, w, PRM_F2[PRM_F2_IDX_PERSP]);
        case 99:    return CL_V_BWRAPS(in, w, PRM_F3[PRM_F3_IDX_BWRAPS], PRM_F2[PRM_F2_IDX_BWRAPTWIST]);
        case 100:   return CL_V_HEMISPHERE(in, w);
        case 101:   return CL_V_POLYNOMIAL(in, w, PRM_F2[PRM_F2_IDX_POLYNOMIALPOW], PRM_F2[PRM_F2_IDX_POLYNOMIALLC], PRM_F2[PRM_F2_IDX_POLYNOMIALSC]);
        case 102:   return CL_V_CROP(in, w, state, PRM_F4[PRM_F4_IDX_CROPLTRB], PRM_F2[PRM_F2_IDX_CROP]);
        case 103:   return CL_V_UNPOLAR(in, w);
        case 104:   return CL_V_GLYNNIA(in, w, state);
        case 105:   return CL_V_POINT_SYMMETRY(in, w, state, PRM_F3[PRM_F3_IDX_PTSYM]);

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


static float2 CL_V_DISPATCH_COMPILER(
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
// CL FLAM3 kernel (xforms/iterators)
//
// The main FLAM3 Kernel function.
// This will be called from the Houdini OpenCL node.
// ----------------------------

__kernel void cl_flam3( 
    int F3C,
    int OPID,
    int ITER,
    int P_length,
    __global float * restrict P,
    int COLOR_length,
    __global float * restrict COLOR,
    int ALPHA_length,
    __global float * restrict ALPHA,
    int PSCALE_length,
    __global float * restrict PSCALE,
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
    int PPVT_length,
    int PPVT_tuplesize,
    __global int * restrict PPVT_index,
    __global float4 * restrict PPVT,
    int PPVW_length,
    int PPVW_tuplesize,
    __global int * restrict PPVW_index,
    __global float4 * restrict PPVW,
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
    __global float4 * restrict PRM_F3,   // Casted as float4 instead of float3 array so it map correctly
    int PRM_F4_length,
    int PRM_F4_tuplesize,
    __global int * restrict PRM_F4_index,
    __global float4 * restrict PRM_F4
)
{        
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

    // PRE/POST variations
    __local int4 local_PPVT[MAX_XFORMS];
    __local float4 local_PPVW[MAX_XFORMS];
    // VAR variations
    __local int4 local_VT[MAX_XFORMS];
    __local float4 local_VW[MAX_XFORMS];

    // PRE, VAR and POST parameterics
    __local float local_PRM_F[PRM_NUM_F_SIZE];
    __local float2 local_PRM_F2[PRM_NUM_F2_SIZE];
    __local float4 local_PRM_F3[PRM_NUM_F3_SIZE];   // Marked as F3 becasue it was meant to be a vector array from vex
    __local float4 local_PRM_F4[PRM_NUM_F4_SIZE];

    // copy cooperatively
    for(int i = lid; i < RES; i += lsize){
        // CDF
        local_IW[i] = IW[i];
        
        // pre affine
        local_PRE_AFFINE[i].xy = (float4)(X[i], Y[i]);
        local_PRE_AFFINE[i].o = (float4)(O[i], 0.0f, 0.0f);
        // post affine
        local_POST_AFFINE[i].xy = (float4)(PX[i], PY[i]);
        local_POST_AFFINE[i].o = (float4)(PO[i], 0.0f, 0.0f);
        // post affine toggles
        local_POST[i] = POST[i];

        // PRE/POST variations
        local_PPVT[i] = convert_int4(PPVT[i]);
        local_PPVW[i] = PPVW[i];

        // VAR variations
        local_VT[i] = convert_int4(VT[i]);
        local_VW[i] = VW[i];
    }

    // Copy arrays of floats in chunks of float4s
    // and handle the remainders if any.
    
    // Float arrays
    int total_SHD       = RES * SHD_NUM_SIZE;
    int total_XAOS      = RES * RES;
    int total_PRM_F     = RES * PRM_NUM_F;
    // Float2 array
    int total_PRM_F2    = RES * PRM_NUM_F2;
    // Float4 arrays
    int total_PRM_F3    = RES * PRM_NUM_F3; // Marked as F3 becasue it was meant to be a vector array from vex
    int total_PRM_F4    = RES * PRM_NUM_F4;

    // SHD
    int num_f4_SHD = total_SHD >> 2;
    for(int i = lid; i < num_f4_SHD; i += lsize)
        ((__local float4*)local_SHD)[i] = ((__global float4*)SHD)[i];
    for(int i = (num_f4_SHD << 2) + lid; i < total_SHD; i += lsize)
        local_SHD[i] = SHD[i];
    // PRM_F
    int num_f4_PRM_F = total_PRM_F >> 2;
    for(int i = lid; i < num_f4_PRM_F; i += lsize)
        ((__local float4*)local_PRM_F)[i] = ((__global float4*)PRM_F)[i];
    for(int i = (num_f4_PRM_F << 2) + lid; i < total_PRM_F; i += lsize)
        local_PRM_F[i] = PRM_F[i];
    // PRM_F2
    for(int i = lid; i < total_PRM_F2; i += lsize)
        local_PRM_F2[i] = PRM_F2[i];
    // PRM_F3
    for(int i = lid; i < total_PRM_F3; i += lsize)
        local_PRM_F3[i] = PRM_F3[i];
    // PRM_F4
    for(int i = lid; i < total_PRM_F4; i += lsize)
        local_PRM_F4[i] = PRM_F4[i];

    if(XS){
        // XST
        int num_f4 = total_XAOS >> 2;
        for(int i = lid; i < num_f4; i += lsize)
            ((__local float4*)local_XST)[i] = ((__global float4*)XST)[i];
        for(int i = (num_f4 << 2) + lid; i < total_XAOS; i += lsize)
            local_XST[i] = XST[i];
    }
    barrier(CLK_LOCAL_MEM_FENCE);   // Wait for the copy to complete

    int gid = get_global_id(0);
    if (gid >= P_length)
        return;
    
    // init
    int idx;
    int4 _vt, _ppvt;
    float clr = 0.0f;
    float _prev_clr = 0.0f;
    float2 mem, _tmp;
    float4 _vw, _ppvw;
    
    // RNG init
    float r;
    x128_state_t rng;
    rng_init(&rng, gid + OPID);  // unique per thread, per node
    
    // build starting sample (Biunit)
    mem = (float2)(rng_next_neg1pos1(&rng), rng_next_neg1pos1(&rng));
    
    // if XAOS, pick a starting xform from distribution
    if(XS) idx = sample_cdf_binary(local_IW, RES, rng_next_float(&rng));

    for (int i = 0; i < ITER; ++i){
        
        // xform selection
        r = rng_next_float(&rng);
        idx = XS ? sample_cdf_binary(&local_XST[idx * RES], RES, r) : sample_cdf_binary(local_IW, RES, r);

        // pre affine 
        affine_t pa = local_PRE_AFFINE[idx];
        mem = affine(mem, pa);

        // PRE/POST data
        _ppvt = local_PPVT[idx];
        _ppvw = local_PPVW[idx];
        // PRE
        if (_ppvw.x > 0.0f) mem += CL_V_PREBLUR(_ppvw.x, &rng);
        if (_ppvw.y > 0.0f) mem  = CL_V_DISPATCH(_ppvt.y, mem, _ppvw.y, pa.xy.zw, pa.o.xy, F3C, &rng, &local_PRM_F[idx * PRM_NUM_F], &local_PRM_F2[idx * PRM_NUM_F2], &local_PRM_F3[idx * PRM_NUM_F3], &local_PRM_F4[idx * PRM_NUM_F4]);
        if (_ppvw.z > 0.0f) mem  = CL_V_DISPATCH(_ppvt.z, mem, _ppvw.z, pa.xy.zw, pa.o.xy, F3C, &rng, &local_PRM_F[idx * PRM_NUM_F], &local_PRM_F2[idx * PRM_NUM_F2], &local_PRM_F3[idx * PRM_NUM_F3], &local_PRM_F4[idx * PRM_NUM_F4]);
        
        // VAR data
        _vt = local_VT[idx];
        _vw = local_VW[idx];
        // VAR
        _tmp = (float2)(0.0f, 0.0f);
        if (_vw.x != 0.0f) _tmp += CL_V_DISPATCH(_vt.x, mem, _vw.x, pa.xy.zw, pa.o.xy, F3C, &rng, &local_PRM_F[idx * PRM_NUM_F], &local_PRM_F2[idx * PRM_NUM_F2], &local_PRM_F3[idx * PRM_NUM_F3], &local_PRM_F4[idx * PRM_NUM_F4]);
        if (_vw.y != 0.0f) _tmp += CL_V_DISPATCH(_vt.y, mem, _vw.y, pa.xy.zw, pa.o.xy, F3C, &rng, &local_PRM_F[idx * PRM_NUM_F], &local_PRM_F2[idx * PRM_NUM_F2], &local_PRM_F3[idx * PRM_NUM_F3], &local_PRM_F4[idx * PRM_NUM_F4]);
        if (_vw.z != 0.0f) _tmp += CL_V_DISPATCH(_vt.z, mem, _vw.z, pa.xy.zw, pa.o.xy, F3C, &rng, &local_PRM_F[idx * PRM_NUM_F], &local_PRM_F2[idx * PRM_NUM_F2], &local_PRM_F3[idx * PRM_NUM_F3], &local_PRM_F4[idx * PRM_NUM_F4]);
        if (_vw.w != 0.0f) _tmp += CL_V_DISPATCH(_vt.w, mem, _vw.w, pa.xy.zw, pa.o.xy, F3C, &rng, &local_PRM_F[idx * PRM_NUM_F], &local_PRM_F2[idx * PRM_NUM_F2], &local_PRM_F3[idx * PRM_NUM_F3], &local_PRM_F4[idx * PRM_NUM_F4]);

        // POST
        if (_ppvw.w > 0.0f) _tmp = CL_V_DISPATCH(_ppvt.w, _tmp, _ppvw.w, pa.xy.zw, pa.o.xy, F3C, &rng, &local_PRM_F[idx * PRM_NUM_F], &local_PRM_F2[idx * PRM_NUM_F2], &local_PRM_F3[idx * PRM_NUM_F3], &local_PRM_F4[idx * PRM_NUM_F4]);

        // post affine    
        if(local_POST[idx]) _tmp = affine(_tmp, local_POST_AFFINE[idx]);


        // color
        _prev_clr = clr = local_SHD[idx] + local_SHD[idx + RES] * _prev_clr;
        
        // update
        mem = _tmp;
    }
    
    // Alpha value
    float a = local_SHD[(RES << 1) + idx];
    
    // OUT
    vstore3((float3)(mem, 0.0f), gid, P);
    ALPHA[gid]   = a;
    COLOR[gid]   = clr;
    PSCALE[gid]  = PSCL * a;
}





// ----------------------------
// CL FLAM3 FF kernel (finalXform)
//
// The FF(finalXform) Kernel function.
// This will be called from the Houdini OpenCL node.
// ----------------------------

__kernel void cl_flam3_ff( 
    int F3C,
    int OPID,
    int P_length,
    __global float * restrict P,
    int FF_X_length,
    int FF_X_tuplesize,
    global int * restrict FF_X_index,
    global float2 * restrict FF_X,
    int FF_Y_length,
    int FF_Y_tuplesize,
    global int * restrict FF_Y_index,
    global float2 * restrict FF_Y,
    int FF_O_length,
    int FF_O_tuplesize,
    global int * restrict FF_O_index,
    global float2 * restrict FF_O,
    int    FF_POST,     // ON(1) or OFF(0)
    float4 FF_PRE_VT,   // PREV1T, unused(0), unused(0), unused(0) -> Just in case I need more in the future
    float4 FF_PRE_VW,   // PREV1W, unused(0), unused(0), unused(0) -> Just in case I need more in the future
    float4 FF_VPP_VT,   // V1T, V2T, POSTV1T, POSTV2T
    float4 FF_VPP_VW,   // V1W, V2W, POSTV1W, POSTV2W
    int FF_PRM_F_length,
    int FF_PRM_F_tuplesize,
    __global int * restrict FF_PRM_F_index,
    __global float * restrict FF_PRM_F,
    int FF_PRM_F2_length,
    int FF_PRM_F2_tuplesize,
    __global int * restrict FF_PRM_F2_index,
    __global float2 * restrict FF_PRM_F2,
    int FF_PRM_F3_length,
    int FF_PRM_F3_tuplesize,
    __global int * restrict FF_PRM_F3_index,
    __global float4 * restrict FF_PRM_F3,   // Casted as float4 instead of float3 array so it map correctly
    int FF_PRM_F4_length,
    int FF_PRM_F4_tuplesize,
    __global int * restrict FF_PRM_F4_index,
    __global float4 * restrict FF_PRM_F4

)
{
    // copy data to local memory
    int lid = get_local_id(0);
    int lsize = get_local_size(0);

    // pre and post affine
    __local affine_t local_FF_AFFINE[FF_RES_PRM];

    // // PRE, VAR and POST parameterics
    __local float local_FF_PRM_F[FF_PRM_NUM_F_SIZE];
    __local float2 local_FF_PRM_F2[FF_PRM_NUM_F2_SIZE];
    __local float4 local_FF_PRM_F3[FF_PRM_NUM_F3_SIZE];   // Marked as F3 becasue it was meant to be a vector array from vex
    __local float4 local_FF_PRM_F4[FF_PRM_NUM_F4_SIZE];

    // copy cooperatively
    for(int i = lid; i < FF_RES_PRM; i += lsize){
        
        // pre and post affine
        local_FF_AFFINE[i].xy = (float4)(FF_X[i], FF_Y[i]);
        local_FF_AFFINE[i].o = (float4)(FF_O[i], 0.0f, 0.0f);
    }

    // Copy arrays of floats in chunks of float4s
    // and handle the remainders if any.
    
    // Float arrays
    int ff_total_PRM_F     = FF_RES_PRM * PRM_NUM_F;
    // Float2 array
    int ff_total_PRM_F2    = FF_RES_PRM * PRM_NUM_F2;
    // Float4 arrays
    int ff_total_PRM_F3    = FF_RES_PRM * PRM_NUM_F3; // Marked as F3 becasue it was meant to be a vector array from vex
    int ff_total_PRM_F4    = FF_RES_PRM * PRM_NUM_F4;

    // PRM_F
    int num_f4_PRM_F = ff_total_PRM_F >> 2;
    for(int i = lid; i < num_f4_PRM_F; i += lsize)
        ((__local float4*)local_FF_PRM_F)[i] = ((__global float4*)FF_PRM_F)[i];
    for(int i = (num_f4_PRM_F << 2) + lid; i < ff_total_PRM_F; i += lsize)
        local_FF_PRM_F[i] = FF_PRM_F[i];
    // PRM_F2
    for(int i = lid; i < ff_total_PRM_F2; i += lsize)
        local_FF_PRM_F2[i] = FF_PRM_F2[i];
    // PRM_F3
    for(int i = lid; i < ff_total_PRM_F3; i += lsize)
        local_FF_PRM_F3[i] = FF_PRM_F3[i];
    // PRM_F4
    for(int i = lid; i < ff_total_PRM_F4; i += lsize)
        local_FF_PRM_F4[i] = FF_PRM_F4[i];

    barrier(CLK_LOCAL_MEM_FENCE);   // Wait for the copy to complete

    int gid = get_global_id(0);
    if (gid >= P_length)
        return;
    
    // init
    int4 _vt, _ppvt;
    float2 mem, _tmp;
    float4 _vw, _ppvw;
    
    // RNG init
    float r;
    x128_state_t rng;
    rng_init(&rng, gid + OPID);  // unique per thread, per node
    
    // get sample
    mem = vload3(gid, P).xy;
    
    // pre affine 
    affine_t pa = local_FF_AFFINE[0];
    mem = affine(mem, pa);

    // PRE
    if (FF_PRE_VW.x > 0.0f) mem = CL_V_DISPATCH(FF_PRE_VT.x, mem, FF_PRE_VW.x, pa.xy.zw, pa.o.xy, F3C, &rng, &local_FF_PRM_F[PRM_NUM_F], &local_FF_PRM_F2[PRM_NUM_F2], &local_FF_PRM_F3[PRM_NUM_F3], &local_FF_PRM_F4[PRM_NUM_F4]);
    
    // VAR
    _tmp = (float2)(0.0f, 0.0f);
    if (FF_VPP_VW.x != 0.0f) _tmp += CL_V_DISPATCH(FF_VPP_VT.x, mem, FF_VPP_VW.x, pa.xy.zw, pa.o.xy, F3C, &rng, &local_FF_PRM_F[0], &local_FF_PRM_F2[0], &local_FF_PRM_F3[0], &local_FF_PRM_F4[0]);
    if (FF_VPP_VW.y != 0.0f) _tmp += CL_V_DISPATCH(FF_VPP_VT.y, mem, FF_VPP_VW.y, pa.xy.zw, pa.o.xy, F3C, &rng, &local_FF_PRM_F[0], &local_FF_PRM_F2[0], &local_FF_PRM_F3[0], &local_FF_PRM_F4[0]);

    // // POST
    if (FF_VPP_VW.z > 0.0f) _tmp = CL_V_DISPATCH(FF_VPP_VT.z, _tmp, FF_VPP_VW.z, pa.xy.zw, pa.o.xy, F3C, &rng, &local_FF_PRM_F[PRM_NUM_F], &local_FF_PRM_F2[PRM_NUM_F2], &local_FF_PRM_F3[PRM_NUM_F3], &local_FF_PRM_F4[PRM_NUM_F4]);
    if (FF_VPP_VW.w > 0.0f) _tmp = CL_V_DISPATCH(FF_VPP_VT.w, _tmp, FF_VPP_VW.w, pa.xy.zw, pa.o.xy, F3C, &rng, &local_FF_PRM_F[PRM_NUM_F], &local_FF_PRM_F2[PRM_NUM_F2], &local_FF_PRM_F3[PRM_NUM_F3], &local_FF_PRM_F4[PRM_NUM_F4]);

    // post affine    
    if(FF_POST) _tmp = affine(_tmp, local_FF_AFFINE[1]);

    
    // update
    mem = _tmp;
    
    // OUT
    vstore3((float3)(mem, 0.0f), gid, P);
}
