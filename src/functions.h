#ifndef __functions_h__
#define __functions_h__

/*  
 /  Title:      SideFX Houdini FLAM3: 2D
 /  Author:     Alessandro Nardini
 /  date:       October 2020, Last revised May 2022
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
 /  Name:       FLAME GENOME   "CVEX"
 /
 /  Comment:    GENOME entities and properties.
*/


#include <math.h>



#define EPS     1e-10
#define LIMIT   1000
#define M_1_PI  0.318309886183790671538
#define M_2_PI  0.636619772367581343076

float ATAN(const vector2 p){ return atan2(p[0], p[1]); }

float ATANYX(const vector2 p){ return atan2(p[1], p[0]); }

float SUMSQ(const vector2 p){ return (p[0]*p[0] + p[1]*p[1]); }

float SQRT(const vector2 p){ return sqrt(SUMSQ(p)); }

float sgn(const float n){ return (n < 0) ? -1 : (n > 0) ? 1 : 0; }

float fmod(const float a, b){ return (a-floor(a/b)*b); }

void sincos(const float a; float sa, ca){ sa=sin(a); ca=cos(a); }

void precalc_V_DISC2(vector disc2_precalc; const float rot, twist){
    // PRECALC
    // disc2_precalc[idx][0] = timespi
    // disc2_precalc[idx][1] = sinadd
    // disc2_precalc[idx][2] = cosadd
    float k;
    disc2_precalc[0] = rot * M_PI;
    sincos(twist, disc2_precalc[1], disc2_precalc[2]);
    disc2_precalc[2] -= 1;
    if(twist > ( 2*M_PI)){ k = (1 + twist - 2*M_PI); disc2_precalc[2]*=k; disc2_precalc[1]*=k; }
    if(twist < (-2*M_PI)){ k = (1 + twist + 2*M_PI); disc2_precalc[2]*=k; disc2_precalc[1]*=k; }
}

void precalc_V_SUPERSHAPE(vector2 supershape_precalc; const float ss_m, ss_n_0){
    // PRECALC
    // supershape_precalc[idx][0] = ss_pm_4
    // supershape_precalc[idx][1] = ss_pneg1_n1
    supershape_precalc[0] = ss_m / 4.0;
    supershape_precalc[1] = -1.0 / ss_n_0;
}

void precalc_V_WEDGEJULIA(vector wedgejulia_precalc; const float power, angle, dist, count){
    // PRECALC
    // wedgejulia_precalc[idx][0] = wedgeJulia_cf
    // wedgejulia_precalc[idx][1] = wedgeJulia_rN
    // wedgejulia_precalc[idx][2] = wedgeJulia_cn
    wedgejulia_precalc[0] = 1.0 - angle * count * M_1_PI * 0.5;
    wedgejulia_precalc[1] = abs(power);
    wedgejulia_precalc[2] = dist / power / 2.0;
}

void precalc_V_PERSP(vector2 persp_precalc; const float angle, dist){
    // PRECALC
    // persp_precalc[idx][0] = vsin
    // persp_precalc[idx][1] = vfsin
    float ang = angle * M_PI / 2.0;
    persp_precalc[0] = sin(ang);
    persp_precalc[1] = dist * cos(ang);
}

void precalc_V_BWRAPS(vector bwraps_precalc; const float cellsize, space, gain){
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
    if(ACTIVE){ if( !isfinite(vec[0]) || !isfinite(vec[1]) || isnan(vec[0]) || isnan(vec[1]) || length(vec)>LIMIT || alpha==0 ) return 1; }
    return 0;
}

void V_SYM(vector2 p; const int num){
    float ang = 0;
    // 3-way
    if(!num){
        if(nrandom('twister')>(1.0/3.0)){
            ang = 120;
            if(nrandom('twister')>0.5) ang = 240;
        }
    }
    // 5-way
    else if(num){
        if(nrandom('twister')>=0.2){
            float sym = nrandom('twister');
            if(0.2 < sym <= 0.4)        ang =  72;
            else if(0.4 < sym <= 0.6)   ang = 144;
            else if(0.6 < sym <= 0.8)   ang = 216;
            else if(0.8 < sym <= 1.0)   ang = 288;
        }
    }
    p *= (matrix2)maketransform(0, set(0, 0, ang));
}

void affine(vector2 p; const vector2 x, y, o){
    p = set( x[0]*p[0] + y[0]*p[1] + o[0],
             x[1]*p[0] + y[1]*p[1] + o[1]);
}

void affineRot(matrix2 m2; const vector2 x, y; const float ang){
    m2 = set(x, y);
    rotate(m2, ang);
}

void XAOS_transpose(const float XAOS[]; float T[]; const int size){
    for(int i=0; i<size; i++){
        for(int j=0; j<size; j++){
            int idx = j*size+i;
            append(T, XAOS[idx]);
        }
    }
}


#endif