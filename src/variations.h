#ifndef __variations_h__
#define __variations_h__

/*  
 /  Title:      SideFX Houdini FRACTAL FLAME generator: 2D
 /  Author:     Alessandro Nardini
 /  date:       October 2020, Last revised November 2021
 /
 /  info:       Based on the original: "The Fractal Flame Algorithm"
 /  Authors:    Scott Draves, Erik Reckase
 /  Weblink:    https://flam3.com/flame_draves.pdf
 /  Date:       September 2003, Last revised November 2008
 /
 /  Name:       FLAME variations    "VEX"
 /
 /  Comment:    FLAM3 variations and functions
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

// The following precal functions are not used yet but here just for reference.
// For the time being those are hard coded inside each variation function.
////////////////////////////////////////////////////////////////////////////////////////////////
void precalc_V_DISC2(vector disc2_precalc; const float rot, twist){
    float k;
    disc2_precalc[0] = rot * M_PI;
    sincos(twist, disc2_precalc[1], disc2_precalc[2]);
    disc2_precalc[2] -= 1;
    if(twist > ( 2*M_PI)){ k = (1 + twist - 2*M_PI); disc2_precalc[2]*=k; disc2_precalc[1]*=k; }
    if(twist < (-2*M_PI)){ k = (1 + twist + 2*M_PI); disc2_precalc[2]*=k; disc2_precalc[1]*=k; }
}

void precalc_V_SUPERSHAPE(vector2 supershape_precalc; const float ss_m, ss_n_0){
    supershape_precalc[0] = ss_m / 4.0;
    supershape_precalc[1] = -1.0 / ss_n_0;
}

void precalc_V_WEDGEJULIA(vector wedgejulia_precalc; const float power, angle, dist, count){
    wedgejulia_precalc[0] = 1.0 - angle * count * M_1_PI * 0.5;
    wedgejulia_precalc[1] = abs(power);
    wedgejulia_precalc[2] = dist / power / 2.0;
}

void precalc_V_PERSP(vector2 persp_precalc; const float angle, dist){
    float ang = angle * M_PI / 2.0;
    persp_precalc[0] = sin(ang);
    persp_precalc[1] = dist * cos(ang);
}

void precalc_V_BWRAPS(vector bwraps_precalc; const float cellsize, space, gain){
    float radius = 0.5 * (cellsize / (1.0 + space*space ));
    bwraps_precalc[0] = sqrt(gain) / cellsize + 1e-6;
    float max_bubble = bwraps_precalc[0] * radius;
    max_bubble = (max_bubble>2.0) ? 1.0 : max_bubble*1.0/( (max_bubble*max_bubble)/4.0+1.0);
    bwraps_precalc[1] = radius*radius;
    bwraps_precalc[2] = radius/max_bubble;
}
// End precalc functions
////////////////////////////////////////////////////////////////////////////////////////////////

vector2 biunit(){ return set(fit01(nrandom('twister'), -1, 1), fit01(nrandom('twister'), -1, 1)); }

int chkNAN_v(const int ACTIVE; const vector2 vec){
    if(ACTIVE){ if(!isfinite(vec[0]) || !isfinite(vec[1]) || isnan(vec[0]) || isnan(vec[1]) || length(vec)>LIMIT) return 1; }
    return 0;
}

void V_SYM(vector2 p; const vector2 pivot; const int num){
    float ang = 0;
    // 3-way
    if(!num){
        if(nrandom('twister')>(1.0/3.0)){
            ang = 120;
            if(nrandom('twister')>0.5) ang = 240;
            p *= (matrix2)maketransform(0, 0, 0, set(0, 0, ang), 1, (vector)pivot);
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
        p *= (matrix2)maketransform(0, 0, 0, set(0, 0, ang), 1, (vector)pivot);
    }
}

void affine(vector2 p; const vector2 x, y, o){
    p = set( x[0]*p[0] + y[0]*p[1] + o[0],
             x[1]*p[0] + y[1]*p[1] + o[1]);
}

void affineRot(matrix2 m2; const vector2 x, y; const float ang){
    m2 = set(x, y);
    rotate(m2, ang);
}



// VARIATIONS
//
//  p = out position
// _p = incoming position
//
// VARs with precalc _p: 9, 10, 11, 19, 21, 30, 35
//
// VARs with PRECALC: 47, 48, 76, 98, 99
//
// 01
void V_SINUSOIDAL(vector2 p; const vector2 _p; const float w){
    p[0] = w * sin(_p[0]);
    p[1] = w * sin(_p[1]);
}
// 02
void V_SPHERICAL(vector2 p; const vector2 _p; const float w){
    float r2 = w / ( SUMSQ(_p) + EPS );
    p[0] = r2 * _p[0];
    p[1] = r2 * _p[1];
}
// 03
void V_SWIRL(vector2 p; const vector2 _p; const float w){
    float rr = SUMSQ(_p);
    float c1, c2, nx, ny;
    c1 = sin(rr);
    c2 = cos(rr);
    nx = c1 * _p[0] - c2 * _p[1];
    ny = c2 * _p[0] + c1 * _p[1];
    p[0] = w * nx;
    p[1] = w * ny;
}
// 04
void V_HORSESHOE(vector2 p; const vector2 _p; const float w){
    float rr = w / (SQRT(_p) + EPS);
    p[0] = (_p[0] - _p[1]) * (_p[0] + _p[1]) * rr;
    p[1] = 2.0 * _p[0] * _p[1] * rr;
}
// 05
void V_POLAR(vector2 p; const vector2 _p; const float w){
    float nx, ny;
    nx = ATAN(_p) * M_1_PI;
    ny = SQRT(_p) - 1.0;
    p[0] = w * nx;
    p[1] = w * ny;
}
// 06
void V_HANDKERCHIEF(vector2 p; const vector2 _p; const float w){
    float aa = ATAN(_p);
    p[0] = w * SQRT(_p) * sin(aa+SQRT(_p));
    p[1] = w * SQRT(_p) * cos(aa-SQRT(_p));
}
// 07
void V_HEART(vector2 p; const vector2 _p; const float w){
    float aa, ca, sa, rr;
    aa = SQRT(_p) * ATAN(_p);
    sa = sin(aa);
    ca = cos(aa);
    rr = w * SQRT(_p) * sa;
    p[0] = rr * sa;
    p[1] = (-rr) * ca;
}
// 08
void V_DISC(vector2 p; const vector2 _p; const float w){
    float aa, rr, sr, cr;
    aa = ATAN(_p) * (1.0/M_PI);
    rr = M_PI * SQRT(_p);
    sincos(rr, sr,cr);
    p[0] = w * sr * aa;
    p[1] = w * cr * aa;
}
// 09 (precalc _p)
void V_SPIRAL(vector2 p; const vector2 _p; const float w){
    vector2 precalc = (vector2)_p / SQRT(_p);
    float r, r1, sr, cr;
    r = SQRT(_p) + EPS;
    r1 = w/r;
    sincos(r, sr, cr);
    p[0] = r1 * (precalc[1] + sr);
    p[1] = r1 * (precalc[0] - cr);
}
// 10 (precalc _p)
void V_HIPERBOLIC(vector2 p; const vector2 _p; const float w){
    vector2 precalc = (vector2)_p / SQRT(_p);
    float rr = SQRT(_p) + EPS;
    p[0] = w * precalc[0] / rr;
    p[1] = w * precalc[1] * rr;
}
// 11 (precalc _p)
void V_DIAMOND(vector2 p; const vector2 _p; const float w){
    vector2 precalc = (vector2)_p / SQRT(_p);
    float rr, sr, cr;
    rr = SQRT(_p);
    sincos(rr, sr, cr);
    p[0] = w * (precalc[0] * cr);
    p[1] = w * (precalc[1] * sr);
}
// 12
void V_EX(vector2 p; const vector2 _p; const float w){
    float aa, rr, n0, n1, m0, m1;
    aa = ATAN(_p);
    rr = SQRT(_p);
    n0 = sin(aa+rr);
    n1 = cos(aa-rr);
    m0 = n0*n0*n0*rr;
    m1 = n1*n1*n1*rr;
    p[0] = w * (m0 + m1);
    p[1] = w * (m0 - m1);
}
// 13
void V_JULIA(vector2 p; const vector2 _p; const float w){
    float rr, aa, sa, ca;
    aa = 0.5 * ATAN(_p);
    if(nrandom('twister')<0.5)
        aa += M_PI;
    rr = w * sqrt(SQRT(_p));
    sincos(aa, sa, ca);
    p[0] = rr * ca;
    p[1] = rr * sa;
}
// 14
void V_BENT(vector2 p; const vector2 _p; const float w){
    float nx, ny;
    nx = _p[0];
    ny = _p[1];
    if(nx < 0.0) nx = nx * 2.0;
    if(ny < 0.0) ny = ny / 2.0;
    p[0] = w * nx;
    p[1] = w * ny;
}
// 15
void V_WAVES(vector2 p; const vector2 _p; const float w, d, e, f, h){
    float dx2, dy2, nx, ny;
    // precalc
    dx2 = 1.0/(f*f + EPS);
    dy2 = 1.0/(h*h + EPS);

    nx = _p[0] + d * sin(_p[1] * dx2);
    ny = _p[1] + e * sin(_p[0] * dy2);
    p[0] = w * nx;
    p[1] = w * ny;
}
// 16
void V_FISHEYE(vector2 p; const vector2 _p; const float w){
    float rr = SQRT(_p);
    rr = 2 * w / (rr+1);
    p[0] = rr * _p[1];
    p[1] = rr * _p[0];
}
// 17
void V_POPCORN(vector2 p; const vector2 _p; const float w, d, h){
    float dx, dy, nx, ny;
    dx = tan(3*_p[1]);
    dy = tan(3*_p[0]);
    nx = _p[0] + d * sin(dx);
    ny = _p[1] + h * sin(dy);
    p[0] = w * nx;
    p[1] = w * ny;
}
// 18
void V_EXPONENTIAL(vector2 p; const vector2 _p; const float w){
    float dx, dy, sdy, cdy;
    dx = w * exp(_p[0]-1.0);
    dy = M_PI * _p[1];
    sincos(dy, sdy, cdy);
    p[0] = dx * cdy;
    p[1] = dx * sdy;
}
// 19 (precalc _p)
void V_POWER(vector2 p; const vector2 _p; const float w){
    vector2 precalc = (vector2)_p / SQRT(_p);
    float rr = w * pow(SQRT(_p), precalc[0]);
    p[0] = rr * precalc[1];
    p[1] = rr * precalc[0];
}
// 20
void V_COSINE(vector2 p; const vector2 _p; const float w){
    float aa, sa, ca, nx, ny;
    aa = _p[0] * M_PI;
    sincos(aa, sa, ca);
    nx = ca * cosh(_p[1]);
    ny = -sa * sinh(_p[1]);
    p[0] = w * nx;
    p[1] = w * ny;
}
// 21 (precalc _p)
void V_RINGS(vector2 p; const vector2 _p; const float w, d){
    vector2 precalc = (vector2)_p / SQRT(_p);
    float dx, rr;
    dx = d*d + EPS;
    rr = SQRT(_p);
    rr = w * (fmod(rr+dx, 2*dx) - dx + rr * (1 - dx));
    p[0] = rr * precalc[1];
    p[1] = rr * precalc[0];
}
// 22
void V_FAN(vector2 p; const vector2 _p; const float w, d){
    float dx, dx2, dy, aa, rr, sa, ca;
    dx = M_PI * (d*d + EPS);
    dy = d;
    dx2 = 0.5 * dx;
    aa = ATAN(_p);
    rr = w * SQRT(_p);
    aa += (fmod(aa+dy,dx) > dx2) ? -dx2 : dx2;
    sincos(aa, sa, ca);
    p[0] = rr * ca;
    p[1] = rr * sa;
}
// 23
void V_BUBBLE(vector2 p; const vector2 _p; const float w){
    float rr = w / (0.25 * SUMSQ(_p) + 1);
    p[0] = rr * _p[0];
    p[1] = rr * _p[1];
}
// 24
void V_CYLINDER(vector2 p; const vector2 _p; const float w){
    p[0] = w * sin(_p[0]);
    p[1] = w * _p[1];
}
// 25
void V_EYEFISH(vector2 p; const vector2 _p; const float w){
    float rr =  (w * 2.0) / (1.0 + SQRT(_p));
    p[0] =  rr*_p[0];
    p[1] =  rr*_p[1];
}
// 26
void V_BLUR(vector2 p; const float w){
    float tmpr, sinr, cosr, rr;
    tmpr = nrandom("twister") * 2 * M_PI;
    sincos(tmpr, sinr, cosr);
    rr = w * nrandom("twister");
    p[0] = rr * cosr;
    p[1] = rr * sinr;
}
// 27 ( parametric )
void V_CURL(vector2 p; const vector2 _p; const float w, c1, c2){
    float re, im, rr;
    if(c1==0){
        if(c2==0){
            p[0] = w * _p[0];
            p[1] = w * _p[1];
        }
        else{
            re = 1.0 + c2*(sqrt(_p[0]) - sqrt(_p[1]));
            im = c2*2.0*_p[0]*_p[1];
            rr = w / (re*re + im*im);
            p[0] = (_p[0] * re + _p[1] * im) * rr;
            p[1] = (_p[1] * re - _p[0] * im) * rr;
        }
    }
    else{
        if(c2==0){
            re = 1.0 + c1*_p[0];
            im = c1*_p[1];
            rr = w / (re*re + im*im);
            p[0] = (_p[0] * re + _p[1] * im) * rr;
            p[1] = (_p[1] * re - _p[0] * im) * rr;
        }
        else{
            re = 1.0 + c1*_p[0] + c2*(sqrt(_p[0]) - sqrt(_p[1]));
            im = c1*_p[1] + c2*2.0*_p[0]*_p[1];
            rr = w / (re*re + im*im);
            p[0] = (_p[0]*re + _p[1]*im)*rr;
            p[1] = (_p[1]*re - _p[0]*im)*rr;
        }
    }
}
// 28 ( parametric )
void V_NGON(vector2 p; const vector2 _p; const float w, pow, sides, corners, circle){
    float cpower, csides, csidesinv, r_factor, theta, phi, amp;
    cpower = -0.5*pow; csides = 2.0*PI/sides; csidesinv = 1.0/csides;
    r_factor = (_p[0]==0 && _p[1]==0) ? 0 : pow(SUMSQ(_p), cpower);
    theta = ATANYX(_p);
    phi = theta - csides * floor(theta*csidesinv);
    if(phi>0.5*csides) phi -= csides;
    amp = (corners * (1.0/cos(phi) - 1.0) + circle) * w * r_factor;
    p[0] = amp * _p[0];
    p[1] = amp * _p[1];
}
// 29 ( parametric )
void V_PDJ(vector2 p; const vector2 _p; const float w; const vector4 pp){
    float  nx1, nx2, ny1, ny2;
    nx1 = cos(pp[1] * _p[0]);
    nx2 = sin(pp[2] * _p[0]);
    ny1 = sin(pp[0] * _p[1]);
    ny2 = cos(pp[3] * _p[1]);
    p[0] = w * (ny1 - nx1);
    p[1] = w * (nx2 - ny2);
}
// 30 ( parametric ) (precalc _p)
void V_BLOB(vector2 p; const vector2 _p; const float w, pp1, pp2, pp3){
    vector2 precalc = (vector2)_p / SQRT(_p);
    float  blob_coeff, rr, aa, bdiff;
    float SQRT = SQRT(_p);
    rr = SQRT;
    aa = ATAN(_p);
    bdiff = pp1 - pp2;
    rr = rr * (pp2 + bdiff * (0.5 + 0.5 * sin(pp3 * aa)));
    p[0] = w * precalc[0] * rr;
    p[1] = w * precalc[1] * rr;
}
// 31 ( parametric )
void V_JULIAN(vector2 p; const vector2 _p; const float w, power, jdist){
    int t_rnd;
    float julian_rN, julian_cn, tmpr, rr, sina, cosa;
    julian_rN = power;
    julian_cn = jdist / power / 2.0;
    t_rnd = (int)trunc(julian_rN * nrandom('twister'));
    tmpr = ( ATANYX(_p) + 2 * M_PI * t_rnd ) / power;
    rr = w * pow( SUMSQ(_p), julian_cn );
    sincos(tmpr, sina, cosa);
    p[0] = rr * cosa;
    p[1] = rr * sina;
}
// 32 ( parametric )
void V_JULIASCOPE(vector2 p; const vector2 _p; const float w, power, jdist){
    int t_rnd;
    float julian_rN, julian_cn, tmpr, rr, sina, cosa;
    julian_rN = power;
    julian_cn = jdist / power / 2.0;
    t_rnd = (int)trunc(julian_rN * nrandom('twister'));
    tmpr = ((t_rnd & 1) == 0) ? (2.0*M_PI*t_rnd+ATANYX(_p))/power : (2.0*M_PI*t_rnd-ATANYX(_p))/power;
    sincos(tmpr, sina, cosa);
    rr = w * pow( SUMSQ(_p), julian_cn );
    p[0] = rr * cosa;
    p[1] = rr * sina;
}
// 33
void V_GAUSSIAN(vector2 p; const float w){
    float ang, rr, sina, cosa;
    ang = nrandom('twister') * 2.0 * M_PI;
    rr = w * (nrandom('twister')+nrandom('twister')+nrandom('twister')+nrandom('twister') - 2.0);
    p[0] = rr * cos(ang);
    p[1] = rr * sin(ang);
}
// 34 ( parametric )
void V_FAN2(vector2 p; const vector2 _p; const float w; const vector2 fan2){
    float dx, dx2, dy, aa, sa,ca,rr, tt;
    dy = fan2[1];
    dx = M_PI * (fan2[0]*fan2[0] + EPS);
    dx2 = 0.5*dx;
    aa = ATAN(_p);
    rr = w * SQRT(_p);
    tt = aa + dy - dx * (int)((aa + dy)/dx);
    aa = (tt>dx2) ? aa-dx2 : aa+dx2;
    sincos(aa, sa, ca);
    p[0] = rr * sa;
    p[1] = rr * ca;
}
// 35 ( parametric ) (precalc _p)
void V_RINGS2(vector2 p; const vector2 _p; const float w, rings2val){
    vector2 precalc = (vector2)_p / SQRT(_p);
    float rr, dx;
    int nrand;
    rr = SQRT(_p);
    dx = rings2val*rings2val;
    rr += -2.0*dx*(int)((rr+dx)/(2.0*dx)) + rr * (1.0-dx);
    p[0] = w * precalc[0] * rr;
    p[1] = w * precalc[1] * rr;
}
// 36 ( parametric )
void V_RECTANGLES(vector2 p; const vector2 _p; const float w; const vector2 rect){
    if(rect[0]==0) p[0] = w * _p[0];
    else p[0] = w * ((2 * floor(_p[0] / rect[0]) + 1) * rect[0] - _p[0]);
    if(rect[1]==0) p[1] = w * _p[1];
    else p[1] = w * ((2 * floor(_p[1] / rect[1]) + 1) * rect[1] - _p[1]);
}
// 37 ( parametric )
void V_RADIALBLUR(vector2 p; const vector2 _p; const float w, spin, zoom){
    float rndG, tmpa, ra, rz, sa, ca;
    rndG = w * (nrandom('twister')+nrandom('twister')+nrandom('twister')+nrandom('twister') - 2.0);
    ra = SQRT(_p);
    tmpa = ATANYX(_p) + spin*rndG;
    sincos(tmpa, sa, ca);
    rz = zoom * rndG - 1;
    p[0] = ra * ca + rz * _p[0];
    p[1] = ra * sa + rz * _p[1];
}
// 38 ( parametric )
void V_PIE(vector2 p; const float w, slices, thickness, rotation){
    float aa, rr, sa, ca, sl;
    sl = (int)(nrandom('twister')*slices);
    aa = rotation + 2.0 * M_PI * (sl + nrandom("twister") * thickness) / slices;
    rr = w * nrandom('twister');
    sincos(aa, sa, ca);
    p[0] = rr * ca;
    p[1] = rr * sa;
}
// 39
void V_ARCH(vector2 p; const vector2 _p; const float w){
    float ang, sinr, cosr;
    ang = nrandom("twister") * w * M_PI;
    sincos(ang, sinr, cosr);
    p[0] = _p[0] + (w * sinr);
    p[1] = _p[1] + (w * (sinr*sinr)/cosr);
}
// 40
void V_TANGENT(vector2 p; const vector2 _p; const float w){
    p[0] = w * (sin(_p[0])/cos(_p[1]));
    p[1] = w * tan(_p[1]);
}
// 41
void V_SQUARE(vector2 p; const vector2 _p; const float w){
    p[0] = w * (nrandom("twister") - 0.5);
    p[0] = w * (nrandom("twister") - 0.5);
}
// 42
void V_RAYS(vector2 p; const vector2 _p; const float w){
    float ang, rr, tanrr;
    ang = w * nrandom("twister") * M_PI;
    rr = w / (SUMSQ(_p) + EPS);
    tanrr = w * tan(ang) * rr;
    p[0] = tanrr * cos(_p[0]);
    p[1] = tanrr * sin(_p[1]);
}
// 43
void V_BLADE(vector2 p; const vector2 _p; const float w){
    float rr, sinr, cosr;
    rr = nrandom("twister") * w * SQRT(_p);
    sincos(rr, sinr, cosr);
    p[0] = w * _p[0] * (cosr + sinr);
    p[1] = w * _p[0] * (cosr - sinr);
}
// 44
void V_SECANT2(vector2 p; const vector2 _p; const float w){
    float rr, cr, sr, icr, isr;
    rr = w * SQRT(_p);
    cr = cos(rr);
    sr = sin(rr);
    icr = 1.0/cr;
    p[0] = w * _p[0];
    p[1] = (cr<0) ? w*(icr+1) : w*(icr-1);
}
// 45
void V_TWINTRIAN(vector2 p; const vector2 _p; const float w){
    float rr, sinr, cosr, diff;
    rr = nrandom("twister") * w * SQRT(_p);
    sincos(rr, sinr, cosr);
    diff = log10(sinr*sinr)+cosr;
    if(!isfinite(diff) || isnan(diff))
        diff = -30.0;
    p[0] = w * _p[0] * diff;
    p[1] = w * _p[0] * (diff - sinr*M_PI);
}
// 46
void V_CROSS(vector2 p; const vector2 _p; const float w){
    float ss, rr;
    ss = _p[0]*_p[0] - _p[1]*_p[1];
    rr = w * sqrt(1.0 / (ss*ss+EPS));
    p[0] = _p[0]*rr;
    p[1] = _p[1]*rr;
}
// 47 ( parametric )
void V_DISC2(vector2 p; const vector2 _p; const float w, rot, twist){
    float rr, tt, sinr, cosr, disc2_sinadd, disc2_cosadd, disc2_timespi;
    // precalc
    float k;
    disc2_timespi = rot * M_PI;
    sincos(twist, disc2_sinadd, disc2_cosadd);
    disc2_cosadd -= 1;
    if(twist > ( 2*M_PI)){ k = (1 + twist - 2*M_PI); disc2_cosadd*=k; disc2_sinadd*=k; }
    if(twist < (-2*M_PI)){ k = (1 + twist + 2*M_PI); disc2_cosadd*=k; disc2_sinadd*=k; }

    tt = disc2_timespi * (_p[0] + _p[1]);
    sincos(tt, sinr, cosr);
    rr = w * ATAN(_p) / M_PI;
    p[0] = (sinr + disc2_cosadd) * rr;
    p[1] = (cosr + disc2_sinadd) * rr;
}
// 48 ( parametric )
void V_SUPERSHAPE(vector2 p; const vector2 _p; const float w, ss_rnd, ss_m, ss_holes; const vector ss_n){
    float theta, st, ct, tt1, tt2, rr, ss_pm_4, ss_pneg1_n1;
    // precalc
    ss_pm_4 = ss_m / 4.0;
    ss_pneg1_n1 = -1.0 / ss_n[0];

    theta = ss_pm_4 * ATANYX(_p) + M_PI_4;
    sincos(theta, st, ct);
    tt1 = abs(ct);  tt1 = pow(tt1, ss_n[1]);
    tt2 = abs(st);  tt2 = pow(tt2, ss_n[2]);
    float SQRT = SQRT(_p);
    rr = w * ((ss_rnd*nrandom('twister') + (1.0-ss_rnd)*SQRT) - ss_holes) * pow(tt1+tt2, ss_pneg1_n1) / SQRT;
    p[0] = rr * _p[0];
    p[1] = rr * _p[1];
}
// 49 ( parametric )
void V_FLOWER(vector2 p; const vector2 _p; const float w, petals, holes){
    float theta, rr;
    theta = ATANYX(_p);
    rr = w * (nrandom("twister") - holes) * cos(petals*theta) / SQRT(_p);
    p[0] = rr * _p[0];
    p[1] = rr * _p[1];
}
// 50
void V_CONIC(vector2 p; const vector2 _p; const float w, eccentricity, holes){
    float ct, rr;
    float SQRT = SQRT(_p);
    ct = _p[0] / SQRT;
    rr = w * (nrandom("twister") - holes) 
                * eccentricity / (1 + eccentricity*ct) / SQRT;
    p[0] = rr * _p[0];
    p[1] = rr * _p[1];
}
// 51 ( parametric )
void V_PARABOLA(vector2 p; const vector2 _p; const float w, height, width){
    float rr, sr, cr;
    rr = SQRT(_p);
    sincos(rr, sr, cr);
    p[0] = height * w * sr*sr * nrandom("twister");
    p[1] = width  * w * cr * nrandom("twister");
}
// 52 ( parametric )
void V_BENT2(vector2 p; const vector2 _p; const float w; const vector2 bent2){
    float nx, ny;
    nx = _p[0]; ny = _p[1];
    if(nx < 0.0)
        nx = nx * bent2[0];
    if(ny < 0.0)
        ny = ny * bent2[1];
    p[0] = w * nx;
    p[1] = w * ny;
}
// 53 ( parametric )
void V_BIPOLAR(vector2 p; const vector2 _p; const float w, shift){
    float x2y2, tt, x2, ps, y;
    x2y2 = SUMSQ(_p);
    tt = x2y2+1;
    x2 = 2*_p[0];
    ps = -M_PI_2 * shift;
    y = 0.5 * atan2(2.0 * _p[1], x2y2 - 1.0) + ps;
    if(y > M_PI_2) y = -M_PI_2 + fmod(y + M_PI_2, M_PI);
    else if (y < -M_PI_2) y = M_PI_2 - fmod(M_PI_2 - y, M_PI);
    p[0] = w * 0.25 * M_2_PI * log((tt+x2) / (tt-x2));
    p[1] = w * M_2_PI * y;
}
// 54
void V_BOARDERS(vector2 p; const vector2 _p; const float w){
    float roundX, roundY, offsetX, offsetY;
    roundX = rint(_p[0]);
    roundY = rint(_p[1]);
    offsetX = _p[0] - roundX;
    offsetY = _p[1] - roundY;
    if(nrandom("twister")>=0.75){
        p[0] = (offsetX*0.5 + roundX);
        p[1] = (offsetY*0.5 + roundY);
    }
    else{
        if (abs(offsetX) >= abs(offsetY)) {
            if (offsetX >= 0.0){
                p[0] = w*(offsetX*0.5 + roundX + 0.25);
                p[1] = w*(offsetY*0.5 + roundY + 0.25 * offsetY / offsetX);
            } 
            else{
                p[0] = w*(offsetX*0.5 + roundX - 0.25);
                p[1] = w*(offsetY*0.5 + roundY - 0.25 * offsetY / offsetX); 
            }
        }
            else{
                if (offsetY >= 0.0){
                    p[1] = w*(offsetY*0.5 + roundY + 0.25);
                    p[0] = w*(offsetX*0.5 + roundX + offsetX/offsetY*0.25);
                } 
                else{
                    p[1] = w*(offsetY*0.5 + roundY - 0.25);
                    p[0] = w*(offsetX*0.5 + roundX - offsetX/offsetY*0.25);
                }
            }
    }
}
// 55
void V_BUTTERFLY(vector2 p; const vector2 _p; const float w){
    float wx, y2, rr;
    wx = w*1.3029400317411197908970256609023;
    y2 = _p[1]*2.0;
    rr = wx*sqrt(abs(_p[1]*_p[0])/(EPS + _p[0]*_p[0] + y2*y2));
    p[0] = rr * _p[0];
    p[1] = rr * y2;
}
// 56 ( parametric )
void V_CELL(vector2 p; const vector2 _p; const float w, size){
    float inv_cell_size, x, y, dx, dy;
    inv_cell_size = 1.0/size;
    x = floor(_p[0]*inv_cell_size);
    y = floor(_p[1]*inv_cell_size);
    dx = _p[0] - x*size;
    dy = _p[1] - y*size;
    if(y>=0){
        if(x>=0){
            y *= 2;
            x *= 2;
        }
        else{
            y *= 2;
            x = -(2*x+1);
        }
    }
    else{
        if(x>=0){
            y = -(2*y+1);
            x *= 2;
        }
        else{
            y = -(2*y+1);
            x = -(2*x+1);
        }
    }
    p[0] = (dx + x*size);
    p[1] = -(dy + y*size);
}
// 57 ( parametric )
void V_CPOW(vector2 p; const vector2 _p; const float w, power, pow_r, pow_i){
    float aa, lnr, va, vc, vd, ang, sa, ca, mm;
    aa = ATANYX(_p);
    lnr = 0.5 * log(SUMSQ(_p));
    va = 2.0 * M_PI / power;
    vc = pow_r / power;
    vd = pow_i / power;
    ang = vc*aa + vd*lnr + va*floor(power * nrandom("twister"));
    mm = w * exp(vc * lnr - vd * aa);
    sincos(ang, sa, ca);
    p[0] = mm * ca;
    p[1] = mm * sa;
}
// 58
void V_EDISC(vector2 p; const vector2 _p; const float w){
    float tmp, tmp2, rr1, rr2, xmax, aa1, aa2, ww, snv, csv, snhu, cshu;
    tmp =SUMSQ(_p);
    tmp2 = 2.0 * _p[0];
    rr1 = sqrt(tmp+tmp2);
    rr2 = sqrt(tmp-tmp2);
    xmax = (rr1+rr2) * 0.5;
    aa1 = log(xmax + (sqrt(xmax - 1.0)));
    aa2 = -acos(_p[0]/xmax);
    ww = w / 11.57034632;;
    sincos(aa1, snv, csv);
    snhu = sinh(aa2);
    cshu = cosh(aa2);
    if(_p[1] > 0.0) snv = -snv;
    p[0] = ww * cshu * csv;
    p[1] = ww * snhu * snv;
}
// 59
void V_ELLIPTIC(vector2 p; const vector2 _p; const float w){
    float tmp, x2, xmax, aa, bb, ssx, ww;
    tmp = SUMSQ(_p) + 1.0;
    x2 = 2.0 * _p[0];
    xmax = 0.5 * (sqrt(tmp+x2) + sqrt(tmp-x2));
    aa = _p[0] / xmax;
    bb = 1.0 - aa*aa;
    ssx = xmax - 1.0;
    ww = w / M_PI_2;
    bb = (bb<0) ? 0 : sqrt(bb);
    ssx = (ssx<0) ? 0 : sqrt(ssx);
    p[0] = ww * atan2(aa,bb);
    p[1] = (_p[1] > 0) ? ww*log(xmax+ssx) : ww * -log(xmax+ssx);
}

// 60
void V_NOISE(vector2 p; const vector2 _p; const float w){
    float tmpr, sinr, cosr, rr;
    tmpr = nrandom("twister") * 2 * M_PI;
    sincos(tmpr, sinr, cosr);
    rr = w * nrandom("twister");
    p[0] = _p[0] * rr * cosr;
    p[1] = _p[1] * rr * sinr;
}
// 61 ( parametric )
void V_ESCHER(vector2 p; const vector2 _p; const float w, beta){
    float aa, lnr, seb, ceb, vc, vd, mm, nn, sn, cn;
    aa = ATANYX(_p);
    lnr = 0.5 * log(SUMSQ(_p));
    sincos(beta, seb, ceb);
    vc = 0.5 * (1.0 + ceb);
    vd = 0.5 * seb;
    mm = w * exp(vc*lnr - vd*aa);
    nn = vc*aa + vd*lnr;
    sincos(nn, sn, cn);
    p[0] = mm * cn;
    p[1] = mm * sn;
}
// 62
void V_FOCI(vector2 p; const vector2 _p; const float w){
    float expx, expnx, sn, cn, tmp, tmpz;
    expx = exp(_p[0]) * 0.5;
    expnx = 0.25 / expx;
    sincos(_p[1], sn, cn);
    tmp = w/(expx + expnx - cn);
    p[0] = tmp * (expx - expnx);
    p[1] = tmp * sn;
}
// 63 ( parametric )
void V_LAZYSUSAN(vector2 p; const vector2 _p; const float w, spin, twist, space; const vector2 lazy){
    float xx, yy, rr, sina, cosa, aa;
    xx = _p[0] - lazy[0];
    yy = _p[1] - lazy[1];
    rr = SQRT(set(xx,yy));
    if(rr<w){
        aa = ATANYX(set(xx,yy)) + spin + twist * (w - rr);
        sincos(aa, sina, cosa);
        rr = w * rr;
        p[0] = rr*cosa + lazy[0];
        p[1] = rr*sina + lazy[1];
    }
    else{
        rr = w * (1.0 + space / rr);
        p[0] = rr*xx + lazy[0];
        p[1] = rr*yy + lazy[1];
    }
}
// 64
void V_LOONIE(vector2 p; const vector2 _p; const float w){
    float rr, rr2, w2;
    rr2 = SUMSQ(_p);
    w2 = w * w;
    if(rr2 < w2){
        rr = w * sqrt(w2/rr2 - 1.0);
        p[0] = rr * _p[0];
        p[1] = rr * _p[1];
    }
    else{
        p[0] = w * _p[0];
        p[1] = w * _p[1];
    }
}
// 65
void V_PREBLUR(vector2 p; const float w){
    float rndG, rndA, sinA, cosA;
    rndG = w * (nrandom("twister") + nrandom("twister") + nrandom("twister") + nrandom("twister") - 2.0);
    rndA = nrandom("twister") * 2.0 * M_PI;
    sincos(rndA, sinA, cosA);
    p[0] += rndG * cosA;
    p[1] += rndG * sinA;
}
// 66 ( parametric )
void V_MODULUS(vector2 p; const vector2 _p; const float w; const vector2 m){
    float xr, yr;
    xr = 2*m[0]; yr = 2*m[1];
    if(_p[0] > m[0])
        p[0] = w * (m[0] + fmod(_p[0] + m[0], xr));
    else if(p[0] < m[0]) p[0] = w * (m[0] - fmod(m[0] + _p[0], xr));
    else p[0] = w * _p[0];
    if(_p[1] > m[1]) p[1] = w * (m[1] + fmod(_p[1] + m[1], yr));
    else if(p[0] < m[0]) p[1] = w * (m[1] - fmod(m[1] + _p[1], yr));
    else p[1] = w * _p[1];
}
// 67 ( parametric )
void V_OSCOPE(vector2 p; const vector2 _p; const float w, freq, amp, damp, sep){
    float tpf, tt;
    tpf = 2 * M_PI * freq;
    if(damp == 0.0) tt = amp * cos(tpf*_p[0]) + sep;
    else tt = amp * exp(-abs(_p[0])* damp) * cos(tpf*_p[0]) + sep;
    if(abs(_p[1]) <= tt){
        p[0] = w * _p[0];
        p[1] = w * -_p[1];
    }
    else{
        p[0] = w * _p[0];
        p[1] = w * _p[1];
    }
}
// 68
void V_POLAR2(vector2 p; const vector2 _p; const float w){
    float p2v = w / M_PI;
    p[0] = p2v * ATAN(_p);
    p[1] = p2v/2.0 * log(SUMSQ(_p));
    }
// 69 ( parametric )
void V_POPCORN2(vector2 p; const vector2 _p; const float w, pop2c; const vector2 pop2){
    p[0] = w * (_p[0] + pop2[0] * sin(tan(_p[1]*pop2c)));
    p[1] = w * (_p[1] + pop2[1] * sin(tan(_p[0]*pop2c)));
    }
// 70 ( parametric )
void V_SCRY(vector2 p; const vector2 _p; const float w){
    float tt, rr;
    tt = SUMSQ(_p);
    rr = 1.0 / (SQRT(_p) * (tt + 1.0/(w+EPS)));
    p[0] = _p[0] * rr;
    p[1] = _p[1] * rr;
}
// 71 ( parametric )
void V_SEPARATION(vector2 p; const vector2 _p; const float w; const vector2 sep, ins){
    float sx2, sy2;
    sx2 = sep[0]*sep[0];
    sy2 = sep[1]*sep[1];
    if(_p[0] > 0.0) p[0] = w * (sqrt(_p[0]*_p[0] + sx2) - _p[0]*ins[0]);
    else p[0] = w * -(sqrt(_p[0]*_p[0] + sx2) + _p[0]*ins[0]);
    if(_p[1] > 0.0) p[1] = w * (sqrt(_p[1]*_p[1] + sy2) - _p[1]*ins[1]);
    else p[1] = w * -(sqrt(_p[1]*_p[1] + sy2) + _p[1]*ins[1]);
}
// 72 ( parametric )
void V_SPLIT(vector2 p; const vector2 _p; const float w; const vector2 split){
    if(cos(_p[0]*split[0]*M_PI) >= 0) p[1] = w * _p[1];
    else p[1] = w * -_p[1];
    if(cos(_p[1]*split[1]*M_PI) >= 0) p[0] = w * _p[0];
    else p[0] = w * -_p[0];
}
// 73 ( parametric )
void V_SPLITS(vector2 p; const vector2 _p; const float w; const vector2 splits){
    if(_p[0] >= 0) p[0] = w * (_p[0] + splits[0]);
    else p[0] = w * (_p[0] - splits[0]);
    if(_p[1] >= 0) p[1] = w * (_p[1] + splits[1]);
    else p[1] = w * (_p[1] - splits[1]);
}
// 74 ( parametric )
void V_STRIPES(vector2 p; const vector2 _p; const float w, space, warp){
    float roundx, offsetx;
    roundx = floor(_p[0] + 0.5);
    offsetx = _p[0] - roundx;
    p[0] = w * (offsetx * (1.0 - space) + roundx);
    p[1] = w * (_p[1] + offsetx*offsetx*warp);
}
// 75 ( parametric )
void V_WEDGE(vector2 p; const vector2 _p; const float w, swirl, angle, hole, count){
    float rr, aa, cc, comp_fac, sa, ca;
    rr = SQRT(_p);
    aa = ATANYX(_p) + swirl * rr;
    cc = floor( (count * aa + M_PI) * M_1_PI*0.5 );
    comp_fac = 1 - angle*count*M_1_PI*0.5;
    aa = aa * comp_fac + cc * angle;
    sincos(aa, sa, ca);
    rr = w * (rr + hole);
    p[0] = rr*ca;
    p[1] = rr*sa;
}
// 76 ( parametric )
void V_WEDGEJULIA(vector2 p; const vector2 _p; const float w, power, angle, dist, count){
    float wedgeJulia_cf, wedgeJulia_rN, wedgeJulia_cn, rr, t_rnd, aa, cc, sa, ca;
    // precalc
    wedgeJulia_cf = 1.0 - angle * count * M_1_PI * 0.5;
    wedgeJulia_rN = abs(power);
    wedgeJulia_cn = dist / power / 2.0;

    rr = w * pow(SUMSQ(_p), wedgeJulia_cn);
    t_rnd = (int)((wedgeJulia_rN)*nrandom("twister"));
    aa = (ATANYX(_p) + 2 * M_PI * t_rnd) / power;
    cc = floor( (count * aa + M_PI)*M_1_PI*0.5 );
    aa = aa * wedgeJulia_cf + cc * angle;
    sincos(aa, sa, ca);
    p[0] = rr * ca;
    p[1] = rr * sa;
}
// 77 ( parametric )
void V_WEDGESPH(vector2 p; const vector2 _p; const float w, swirl, angle, hole, count){
    float rr, aa, cc, comp_fac, sa, ca;
    rr = 1.0/(SQRT(_p) + EPS);
    aa = ATANYX(_p) + swirl * rr;
    cc = floor( (count * aa + M_PI)*M_1_PI*0.5 );
    comp_fac = 1 - angle*count*M_1_PI*0.5;
    aa = aa * comp_fac + cc * angle;
    sincos(aa, sa, ca);
    rr = w * (rr + hole);
    p[0] = rr * ca;
    p[1] = rr * sa;
}
// 78 ( parametric )
void V_WHORL(vector2 p; const vector2 _p; const float w, inside, outside){
    float rr, aa, sa, ca;
    rr = SQRT(_p);
    if(rr<w) aa = ATANYX(_p) + inside/(w-rr);
    else aa = ATANYX(_p) + outside/(w-rr);
    sincos(aa, sa, ca);
    p[0] = w*rr*ca;
    p[1] = w*rr*sa;
}
// 79 ( parametric )
void V_WAVES2(vector2 p; const vector2 _p; const float w; const vector2 scl, freq){
    p[0] = w*(_p[0] + scl[0]*sin(_p[1]*freq[0]));
    p[1] = w*(_p[1] + scl[1]*sin(_p[0]*freq[1]));
}
// 80
void V_COTHEEXP(vector2 p; const vector2 _p; const float w){
    float expe, expz, expsin, expcos;
    expe = exp(_p[0]);
    sincos(p[1], expsin, expcos);
    p[0] = w * expe * expcos;
    p[1] = w * expe * expsin;
}
// 81
void V_COTHELOG(vector2 p; const vector2 _p; const float w){
    p[0] = w * 0.5 * log(SUMSQ(_p));
    p[1] = w * ATANYX(_p);
}
// 82
void V_COTHESIN(vector2 p; const vector2 _p; const float w){
    float sinsin, sinacos, sinsinh, sincosh;
    sincos(_p[0], sinsin, sinacos);
    sinsinh = sinh(_p[1]);
    sincosh = cosh(_p[1]);
    p[0] = w * sinsin * sincosh;
    p[1] = w * sinacos * sinsinh;
}
// 83
void V_COTHECOS(vector2 p; const vector2 _p; const float w){
    float cossin, coscos, cossinh, coscosh;
    sincos(_p[0], cossin, coscos);
    cossinh = sinh(_p[1]);
    coscosh = cosh(_p[1]);
    p[0] = w * coscos * coscosh;
    p[1] = w * cossin * cossinh;
}
// 84
void V_COTHETAN(vector2 p; const vector2 _p; const float w){
    float tansin, tancos, tansinh, tancosh, tanden;
    sincos(2*_p[0], tansin, tancos);
    tansinh = sinh(2.0*_p[1]);
    tancosh = cosh(2.0*_p[1]);
    tanden = 1.0/(tancos + tancosh);
    p[0] = w * tanden * tansinh;
    p[1] = w * tanden * tancosh;
}
// 85
void V_COTHESEC(vector2 p; const vector2 _p; const float w){
    float secsin, seccos, secsinh, seccosh, secden;
    sincos(_p[0], secsin, seccos);
    secsinh = sinh(_p[1]);
    seccosh = cosh(_p[1]);
    secden = 2.0/(cos(2.0*_p[0]) + cosh(2.0*_p[1]));
    p[0] = w * secden * seccos * seccosh;
    p[1] = w * secden * secsin * secsinh;
}
// 86
void V_COTHECSC(vector2 p; const vector2 _p; const float w){
    float cscsin, csccos, cscsinh, csccosh, cscden;
    sincos(p[0], cscsin, csccos);
    cscsinh = sinh(_p[1]);
    csccosh = cosh(_p[1]);
    cscden = 2.0/(cosh(2.0*_p[1]) - cos(2.0*_p[0]));
    p[0] = w * cscden * cscsin * csccosh;
    p[1] = w * cscden * csccos * cscsinh;
}
// 87
void V_COTHECOT(vector2 p; const vector2 _p; const float w){
    float cotsin, cotcos, cotsinh, cotcosh, cotden;
    sincos(2.0*_p[0], cotsin, cotcos);
    cotsinh = sinh(2.0*_p[1]);
    cotcosh = cosh(2.0*_p[1]);
    cotden = 1.0/(cotcosh - cotcos);
    p[0] = w * cotden * cotsin;
    p[1] = w * cotden * -1 * cotsinh;
}
// 88
void V_COTHESINH(vector2 p; const vector2 _p; const float w){
    float sinhsin, sinhcos, sinhsinh, sinhcosh;
    sincos(_p[1], sinhsin, sinhcos);
    sinhsinh = sinh(_p[0]);
    sinhcosh = cosh(_p[0]);
    p[0] = w * sinhsinh * sinhcos;
    p[1] = w * sinhcosh * sinhsin;
}
// 89
void V_COTHECOSH(vector2 p; const vector2 _p; const float w){
    float coshsin, coshcos, coshsinh, coshcosh;
    sincos(_p[1], coshsin, coshcos);
    coshsinh = sinh(_p[0]);
    coshcosh = cosh(_p[0]);
    p[0] = w * coshcosh * coshcos;
    p[1] = w * coshsinh * coshsin;
}
// 90
void V_COTHETANH(vector2 p; const vector2 _p; const float w){
    float tanhsin, tanhcos, tanhsinh, tanhcosh, tanhden;
    sincos(2.0*_p[1], tanhsin, tanhcos);
    tanhsinh = sinh(_p[0]);
    tanhcosh = cosh(_p[0]);
    tanhden = 1.0/(tanhcos + tanhcosh);
    p[0] = w * tanhden * tanhsinh;
    p[1] = w * tanhden * tanhsin;
}
// 91
void V_COTHESECH(vector2 p; const vector2 _p; const float w){
    float sechsin, sechcos, sechsinh, sechcosh, sechden;
    sincos(_p[1], sechsin, sechcos);
    sechsinh = sinh(_p[0]);
    sechcosh = cosh(_p[0]);
    sechden = 2.0/(cos(2.0*_p[1]) + cosh(2.0*_p[0]));
    p[0] = w * sechden * sechcos * sechcosh;
    p[1] = w * sechden * sechsin * sechsinh;
}
// 92
void V_COTHECSCH(vector2 p; const vector2 _p; const float w){
    float cschsin, cschcos, cschsinh, cschcosh, cschden;
    sincos(_p[1], cschsin, cschcos);
    cschsinh = sinh(_p[0]);
    cschcosh = cosh(_p[0]);
    cschden = 2.0/(cosh(2.0*_p[0]) - cos(2.0*_p[1]));
    p[0] = w * cschden * cschsinh * cschcos;
    p[1] = w * cschden * cschcosh * cschsin;
}
// 93
void V_COTHECOTH(vector2 p; const vector2 _p; const float w){
    float cothsin, cothcos, cothsinh, cothcosh, cothden;
    sincos(2.0*_p[1], cothsin, cothcos);
    cothsinh = sinh(2.0*_p[0]);
    cothcosh = cosh(2.0*_p[0]);
    cothden = 1.0/(cothcosh - cothcos);
    p[0] = w * cothden * cothsinh;
    p[1] = w * cothden * cothsin;
}
// 94 ( parametric )
void V_AUGER(vector2 p; const vector2 _p; const float w, freq, scale, sym, ww){
    float  ss, tt, uu, dy, dx;
    ss = sin(freq * _p[0]);
    tt = sin(freq * _p[1]);
    dx = _p[1] + ww*(scale*ss/2.0 + abs(_p[1])*ss);
    dy = _p[0] + ww*(scale*tt/2.0 + abs(_p[0])*tt);
    p[0] = w * (_p[0] + sym*(dx*_p[0]));
    p[1] = w * dy;
}
// 95 ( parametric )
void V_FLUX(vector2 p; const vector2 _p; const float w, spread){
    float xpw, xmw, avgr, avga;
    xpw = _p[0] + w;
    xmw = _p[0] - w;
    avgr = w * (2 + spread) * sqrt(sqrt(_p[1]*_p[1]+xpw*xpw) / sqrt(_p[1]*_p[1] + xmw*xmw));
    avga = ( atan2(_p[1], xmw) - atan2(_p[1], xpw)) * 0.5;
    p[0] = avgr * cos(avga);
    p[1] = avgr * sin(avga);
}
// 96 ( parametric )
void V_MOBIUS(vector2 p; const vector2 _p; const float w; const vector4 re, im){
    float reu, imu, rev, imv, radv;
    reu = re[0] * _p[0] - im[0] * _p[1] + re[1];
    imu = re[0] * _p[1] + im[0] * _p[0] + im[1];
    rev = re[2] * _p[0] - im[2] * _p[1] + re[3];
    imv = re[2] * _p[1] + im[2] * _p[0] + im[3];
    radv = w / (rev*rev + imv*imv);
    p[0] = radv * (reu*rev + imu*imv);
    p[1] = radv * (imu*rev - reu*imv);
}
// 97 ( parametric )
void V_CURVE(vector2 p; const vector2 _p; const float w; const vector2 l, a){
    float pc_xlen, pc_ylen;
    pc_xlen = l[0]*l[0];
    pc_ylen = l[1]*l[1];
    if (pc_xlen<1E-20) pc_xlen = 1E-20;
    if (pc_ylen<1E-20) pc_ylen = 1E-20;
    p[0] = w * (_p[0] + a[0] * exp(_p[1]*_p[1]/l[0]));
    p[1] = w * (_p[1] + a[1] * exp(_p[0]*_p[0]/l[1]));
}
// 98 ( parametric )
void V_PERSPECTIVE(vector2 p; const vector2 _p; const float w, angle, dist){
    float tt, vsin, vfcos;
    // precalc
    float ang = angle * M_PI / 2.0;
    vsin = sin(ang);
    vfcos = dist * cos(ang);

    tt = 1.0 / (dist - _p[1] * vsin);
    p[0] = w * dist * _p[0] * tt;
    p[1] = w * vfcos * _p[1] * tt;
}
// 99 ( parametric )
void V_BWRAPS(vector2 p; const vector2 _p; const float w, cellsize, space, gain, innertwist, outertwist){
    float g2, r2, rfactor, max_bubble, Vx, Vy, Cx, Cy, Lx, Ly, rr, theta, ss, cc;
    // precalc
    float radius = 0.5 * (cellsize / (1.0 + space*space ));
    g2 = sqrt(gain) / cellsize + 1e-6;
    max_bubble = g2 * radius;
    max_bubble = (max_bubble>2.0) ? 1.0 : max_bubble*1.0/( (max_bubble*max_bubble)/4.0+1.0);
    r2 = radius*radius;
    rfactor = radius/max_bubble;

    Vx = _p[0];
    Vy = _p[1];
    if(cellsize == 0.0){
        p[0] = w * Vx;
        p[1] = w * Vy;
    }
    else{
        Cx = (floor(Vx / cellsize) + 0.5) * cellsize;
        Cy = (floor(Vy / cellsize) + 0.5) * cellsize;
        Lx = Vx - Cx;
        Ly = Vy - Cy;
        if((Lx*Lx + Ly*Ly) > r2){
            p[0] = w * Vx;
            p[1] = w * Vy;
        }
        else{
            Lx *= g2;
            Ly *= g2;
            rr = rfactor / ((Lx*Lx + Ly*Ly) / 4.0 + 1);
            Lx *= rr;
            Ly *= rr;
            rr = (Lx*Lx + Ly*Ly) / r2;
            theta = innertwist * (1.0 - rr) + outertwist * rr;
            sincos(theta, ss, cc);
            Vx = Cx + cc * Lx + ss * Ly;
            Vy = Cy - ss * Lx + cc * Ly;
            p[0] = w * Vx;
            p[1] = w * Vy;
        }
    }
}
// 100
void V_HEMISPHERE(vector2 p; const vector2 _p; const float w){
    float tt;
    tt = w / sqrt(SUMSQ(_p) + 1);
    p[0] = _p[0] * tt;
    p[1] = _p[1] * tt;
}
// 101 ( parametric )
void V_POLYNOMIAL(vector2 p; const vector2 _p; const float w; const vector2 pow, lc, sc){
    float xp, yp;
    xp = pow(w * abs(_p[0]), pow[0]);
    yp = pow(w * abs(_p[1]), pow[1]);
    p[0] = xp * sgn(_p[0]) + lc[0] * _p[0] * sc[0];
    p[1] = yp * sgn(_p[1]) + lc[1] * _p[1] * sc[1];
}

#endif
