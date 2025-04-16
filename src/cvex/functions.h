#ifndef __functions_h__
#define __functions_h__

/*  
 /  Tested on:  Houdini 19.x
 /              Houdini 19.5
 /              Houdini 20.x
 /              Houdini 20.5
 /
 /  Title:      FLAM3H. SideFX Houdini FLAM3: 2D
 /  Author:     Alessandro Nardini
 /  date:       October 2020, Last revised April 2025
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
 /  Name:       FUNCTIONS "CVEX"
 /
 /  Comment:    FLAM3 functions.
*/


#include <math.h>



#define LIMIT   1000.0f
#define EPS     2.220446049250313e-016
#define M_PI2   6.28318530717958647692
#define M_1_PI  0.318309886183790671538
#define M_2_PI  0.636619772367581343076
#define FLOAT_MAX_TAN 8388607.0f
#define FLOAT_MIN_TAN -FLOAT_MAX_TAN

float res_weight(const float x, y, w){ return ( x * 1+(y*w) ) / ( 1920 * 1+(1080*w) ); }

float ATAN(const vector2 p){ return atan2(p[0], p[1]); }

float ATANYX(const vector2 p){ return atan2(p[1], p[0]); }

float SUMSQ(const vector2 p){ return (p[0]*p[0] + p[1]*p[1]); }

float SQRT(const vector2 p){ return sqrt(SUMSQ(p)); }

float SafeTan(const float x){ return tan(clamp(x, FLOAT_MIN_TAN, FLOAT_MAX_TAN)); }

float Zeps(const float x){ return (x==0) ? EPS : x; }

float sgn(const float n){ return (n < 0) ? -1 : (n > 0) ? 1 : 0; }

float fmod(const float a, b){ return (a-floor(a/b)*b); }

void sincos(const float a; float sa, ca){ sa=sin(a); ca=cos(a); }

// An improved Elliptic version which helps with rounding errors.
// Even at 32bit is already much much better than the original FLAM3 version, so I keep this one.
// Source: https://mathr.co.uk/blog/2017-11-01_a_more_accurate_elliptic_variation.html
//
float log1p(float x){
    float xp1 = 1+x;
    return (xp1==1) ? x : x * log(xp1) / (xp1-1);
}
float Sqrt1pm1(float x){
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

    return sqrt(1 + x) - 1;
}

void precalc_V_DISC2(vector disc2_precalc; const float rot, twist){
    // This is the only one to benefit from the precalc

    // PRECALC
    // disc2_precalc[idx][0] = timespi  (d0)
    // disc2_precalc[idx][1] = sinadd   (d1)
    // disc2_precalc[idx][2] = cosadd   (d2)
    float k, d0, d1, d2;
    
    d0 = rot * M_PI;
    sincos(twist, d1, d2);
    d2 -= 1;
    if(twist > ( 2*M_PI)){ k = (1 + twist - 2*M_PI); d2*=k; d1*=k; }
    if(twist < (-2*M_PI)){ k = (1 + twist + 2*M_PI); d2*=k; d1*=k; }
    disc2_precalc = set(d0, d1, d2);
}

void precalc_V_SUPERSHAPE(vector2 supershape_precalc; const float ss_m, ss_n_0){
    // NOT USED as the precalc made it slower for some reasons

    // PRECALC
    // supershape_precalc[idx][0] = ss_pm_4
    // supershape_precalc[idx][1] = ss_pneg1_n1
    supershape_precalc[0] = ss_m / 4.0;
    supershape_precalc[1] = -1.0 / ss_n_0;
}

void precalc_V_WEDGEJULIA(vector wedgejulia_precalc; const float power, angle, dist, count){
    // NOT USED as the precalc made it slower for some reasons

    // PRECALC
    // wedgejulia_precalc[idx][0] = wedgeJulia_cf
    // wedgejulia_precalc[idx][1] = wedgeJulia_rN
    // wedgejulia_precalc[idx][2] = wedgeJulia_cn
    wedgejulia_precalc[0] = 1.0 - angle * count * M_1_PI * 0.5;
    wedgejulia_precalc[1] = abs(power);
    wedgejulia_precalc[2] = dist / power / 2.0;
}

void precalc_V_PERSP(vector2 persp_precalc; const float angle, dist){
    // NOT USED as the precalc made it slower for some reasons

    // PRECALC
    // persp_precalc[idx][0] = vsin
    // persp_precalc[idx][1] = vfsin
    float ang = angle * M_PI / 2.0;
    persp_precalc[0] = sin(ang);
    persp_precalc[1] = dist * cos(ang);
}

void precalc_V_BWRAPS(vector bwraps_precalc; const float cellsize, space, gain){
    // NOT USED as the precalc made it slower for some reasons

    // PRECALC
    // bwraps_precalc[idx][0] = g2
    // bwraps_precalc[idx][1] = r2
    // bwraps_precalc[idx][2] = rfactor
    float radius = 0.5 * (cellsize / (1.0 + space*space ));
    bwraps_precalc[0] = sqrt(gain) / cellsize + 1e-6;
    float max_bubble = bwraps_precalc[0] * radius;
    max_bubble = (max_bubble>2.0) ? 1.0 : max_bubble*1.0/( (max_bubble*max_bubble)/4.0+1.0);
    bwraps_precalc[1] = radius*radius;
    bwraps_precalc[2] = radius/max_bubble;
}

vector2 biunit(){ return set(2*nrandom('twister')-1, 2*nrandom('twister')-1); }

int chkPT(const int ACTIVE; const vector2 vec; const float alpha){
    if(ACTIVE){ float val=vec[0]+vec[1]; if( !isfinite(val) || isnan(val) || length(vec)>LIMIT || alpha==0 ) return 1; }
    return 0;
}

void affine(vector2 p; const vector2 x, y, o){
    p = set( /*A*/x[0]*p[0] + /*B*/y[0]*p[1] + /*C*/o[0],
             /*D*/x[1]*p[0] + /*E*/y[1]*p[1] + /*F*/o[1]);
}

void affineRot(matrix2 m2; const vector2 x, y; const float ang){
    m2 = set(x, y);
    rotate(m2, ang);
}

void XAOS_transpose_s(const string XAOS[]; string T[]; const int size){
    for(int i=0; i<size; i++){
        for(int j=0; j<size; j++){
            int idx = j*size+i;
            append(T, XAOS[idx]);
        }
    }
}


#endif