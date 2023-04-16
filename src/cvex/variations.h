#ifndef __variations_h__
#define __variations_h__

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
 /  Name:       VARIATIONS "CVEX"
 /
 /  Comment:    FLAM3 variations.
*/


#include <functions.h>


/*
    VARIATIONS
    p = out position
    _p = incoming position
    VARs with precalc _p: 9, 10, 11, 19, 21, 30, 35
    VARs with PRECALC: 47, 48, 76, 98, 99

    00 LINEAR
    hardcoded inside "flame.h", "flamepp.h", "flameff.h" header files.
*/

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
    float rr, c1, c2, nx, ny;
    rr = SUMSQ(_p);
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
    float a = ATAN(_p);
    p[0] = w * SQRT(_p) * sin(a+SQRT(_p));
    p[1] = w * SQRT(_p) * cos(a-SQRT(_p));
}
// 07
void V_HEART(vector2 p; const vector2 _p; const float w){
    float a, r;
    a = SUMSQ(_p) * ATAN(_p);
    r = w * SUMSQ(_p);
    p[0] = r * sin(a);
    p[1] = (-r) * cos(a);
}
// 08
void V_DISC(vector2 p; const vector2 _p; const float w){
    float a, r, sr, cr;
    a = ATAN(_p) * (1.0/M_PI);
    r = M_PI * SQRT(_p);
    sincos(r, sr,cr);
    p[0] = w * sr * a;
    p[1] = w * cr * a;
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
    vector2 precalc = _p / SQRT(_p);
    float rr = Zeps(SQRT(_p));
    p[0] = w * precalc[0] / rr;
    p[1] = w * precalc[1] * rr;
}
// 11 (precalc _p)
void V_DIAMOND(vector2 p; const vector2 _p; const float w){
    float a = atan2(_p[0], _p[1]);
    float r = sqrt(_p[0]*_p[0] + _p[1]*_p[1]);
    p[0] = w * sin(a) * cos(r);
    p[1] = w * cos(a) * sin(r);
}
// 12
void V_EX(vector2 p; const vector2 _p; const float w){
    float a, r, n0, n1, m0, m1;
    a = ATAN(_p);
    r = SQRT(_p);
    n0 = sin(a+r);
    n1 = cos(a-r);
    m0 = n0*n0*n0*r;
    m1 = n1*n1*n1*r;
    p[0] = w * (m0 + m1);
    p[1] = w * (m0 - m1);
}
// 13
void V_JULIA(vector2 p; const vector2 _p; const float w){
    float r, a, sa, ca;
    a = 0.5 * ATAN(_p);
    if(nrandom('twister')<0.5)
        a += M_PI;
    r = w * sqrt(SQRT(_p));
    sincos(a, sa, ca);
    p[0] = r * ca;
    p[1] = r * sa;
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
void V_WAVES(vector2 p; const vector2 _p; const float w, b, c, e, f){
    float dx, dy, m_Dx2, m_Dy2, c10, c11, nx, ny;
    dx = c;
    dy = f;
    m_Dx2 = 1 / Zeps(dx * dx);
    m_Dy2 = 1 / Zeps(dy * dy);
    
    c10 = b;
    c11 = e;
    nx = _p[0] + c10 * sin(_p[1] * m_Dx2);
    ny = _p[1] + c11 * sin(_p[0] * m_Dy2);
    p[0] = w * nx;
    p[1] = w * ny;
}
// 16
void V_FISHEYE(vector2 p; const vector2 _p; const float w){
    float r = SQRT(_p);
    r = 2 * w / (r+1);
    p[0] = r * _p[1];
    p[1] = r * _p[0];
}
// 17
void V_POPCORN(vector2 p; const vector2 _p; const float w, c, f){
    float dx, dy, nx, ny;
    dx = tan(3*_p[1]);
    dy = tan(3*_p[0]);
    nx = _p[0] + c * sin(dx);
    ny = _p[1] + f * sin(dy);
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
    float r = w * pow(SQRT(_p), precalc[0]);
    p[0] = r * precalc[1];
    p[1] = r * precalc[0];
}
// 20
void V_COSINE(vector2 p; const vector2 _p; const float w){
    float a, sa, ca, nx, ny;
    a = _p[0] * M_PI;
    sincos(a, sa, ca);
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
void V_FAN(vector2 p; const vector2 _p; const float w, c, f){
    float dx, dx2, dy, a, r, sa, ca;
    dx = M_PI * (c*c + EPS);
    dy = f;
    dx2 = 0.5 * dx;
    a = ATAN(_p);
    r = w * SQRT(_p);
    a += (fmod(a+dy,dx) > dx2) ? -dx2 : dx2;
    sincos(a, sa, ca);
    p[0] = r * ca;
    p[1] = r * sa;
}
// 23
void V_BUBBLE(vector2 p; const vector2 _p; const float w){
    float r = w / (0.25 * SUMSQ(_p) + 1);
    p[0] = r * _p[0];
    p[1] = r * _p[1];
}
// 24
void V_CYLINDER(vector2 p; const vector2 _p; const float w){
    p[0] = w * sin(_p[0]);
    p[1] = w * _p[1];
}
// 25
void V_EYEFISH(vector2 p; const vector2 _p; const float w){
    float r =  (w * 2.0) / (1.0 + SQRT(_p));
    p[0] =  r*_p[0];
    p[1] =  r*_p[1];
}
// 26
void V_BLUR(vector2 p; const float w){
    float tmpr, sinr, cosr, r;
    tmpr = nrandom("twister") * 2 * M_PI;
    sincos(tmpr, sinr, cosr);
    r = w * nrandom("twister");
    p[0] = r * cosr;
    p[1] = r * sinr;
}
// 27 ( parametric )
void V_CURL(vector2 p; const vector2 _p; const float w, c1, c2){
    // From APOPHYSIS
    float re, im, r;
    if(c1==0){
        if(c2==0){
            p[0] = w * _p[0];
            p[1] = w * _p[1];
        }
        else{
            re = 1.0 + c2*(sqrt(_p[0]) - sqrt(_p[1]));
            im = c2*2.0*_p[0]*_p[1];
            r = w / (re*re + im*im);
            p[0] = (_p[0] * re + _p[1] * im) * r;
            p[1] = (_p[1] * re - _p[0] * im) * r;
        }
    }
    else{
        if(c2==0){
            re = 1.0 + c1*_p[0];
            im = c1*_p[1];
            r = w / (re*re + im*im);
            p[0] = (_p[0] * re + _p[1] * im) * r;
            p[1] = (_p[1] * re - _p[0] * im) * r;
        }
        else{
            re = 1.0 + c1*_p[0] + c2*(sqrt(_p[0]) - sqrt(_p[1]));
            im = c1*_p[1] + c2*2.0*_p[0]*_p[1];
            r = w / (re*re + im*im);
            p[0] = (_p[0]*re + _p[1]*im)*r;
            p[1] = (_p[1]*re - _p[0]*im)*r;
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
void V_GAUSSIAN_BLUR(vector2 p; const float w){
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
    p[0] = w * sinr;
    p[1] = w * (sinr*sinr)/cosr;
}
// 40
void V_TANGENT(vector2 p; const vector2 _p; const float w){
    p[0] = w * (sin(_p[0])/cos(_p[1]));
    p[1] = w * tan(_p[1]);
}
// 41
void V_SQUARE(vector2 p; const vector2 _p; const float w){
    p[0] = w * (nrandom("twister") - 0.5);
    p[1] = w * (nrandom("twister") - 0.5);
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
void V_DISC2(vector2 p; const vector2 _p; const float w, rot, twist, disc2_timespi, disc2_sinadd, disc2_cosadd){
    float rr, tt, sinr, cosr;
    tt = disc2_timespi * (_p[0] + _p[1]);
    sincos(tt, sinr, cosr);
    rr = w * ATAN(_p) / M_PI;
    p[0] = (sinr + disc2_cosadd) * rr;
    p[1] = (cosr + disc2_sinadd) * rr;
}
// 47 L ( parametric )
void V_DISC2_L(vector2 p; const vector2 _p; const float w, rot, twist; const vector precalc){
    float disc2_sinadd, disc2_cosadd, disc2_timespi;
    // precalc
    disc2_timespi = precalc[0];
    disc2_sinadd  = precalc[1];
    disc2_cosadd  = precalc[2];

    V_DISC2(p, _p, w, rot, twist, disc2_timespi, disc2_sinadd, disc2_cosadd);
}
// 47 FF ( parametric )
void V_DISC2_FF(vector2 p; const vector2 _p; const float w, rot, twist;){
    float disc2_sinadd, disc2_cosadd, disc2_timespi;
    // precalc
    vector precalc;
    precalc_V_DISC2(precalc, rot, twist);
    disc2_timespi = precalc[0];
    disc2_sinadd  = precalc[1];
    disc2_cosadd  = precalc[2];

    V_DISC2(p, _p, w, rot, twist, disc2_timespi, disc2_sinadd, disc2_cosadd);
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
// 50 ( parametric )
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
    inv_cell_size = 1 / size;
    x = floor(_p[0] * inv_cell_size);
    y = floor(_p[1] * inv_cell_size);
    dx = _p[0] - x * size;
    dy = _p[1] - y * size;
    if(y >= 0){
        if(x >= 0){
            y *= 2;
            x *= 2;
        }
        else{
            y *= 2;
            x = -(2 * x + 1);
        }
    }
    else{
        if(x >= 0){
            y = -(2 * y + 1);
            x *= 2;
        }
        else{
            y = -(2 * y + 1);
            x = -(2 * x + 1);
        }
    }
    p[0] = w * (dx + x * size);
    p[1] = -(w * (dy + y * size));
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
    tmp =SUMSQ(_p) + 1;
    tmp2 = 2.0 * _p[0];
    rr1 = sqrt(tmp+tmp2);
    rr2 = sqrt(tmp-tmp2);
    xmax = Zeps((rr1+rr2) * 0.5);
    aa1 = log(xmax + (sqrt(xmax - 1.0)));
    aa2 = -acos(_p[0]/xmax);
    ww = w / 11.57034632;
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
    yy = _p[1] + lazy[1];
    rr = SQRT(set(xx,yy));
    if(rr<w){
        aa = ATANYX(set(xx,yy)) + spin + twist * (w - rr);
        sincos(aa, sina, cosa);
        rr = w * rr;
        p[0] = rr*cosa + lazy[0];
        p[1] = rr*sina - lazy[1];
    }
    else{
        rr = w * (1.0 + space / rr);
        p[0] = rr*xx + lazy[0];
        p[1] = rr*yy - lazy[1];
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
    float xr=2*m[0]; float yr=2*m[1];

    if(_p[0] > m[0])
        p[0] = w * (-m[0] + fmod(_p[0] + m[0], xr));
    else if(_p[0] < -m[0])
        p[0] = w * (m[0] - fmod(m[0] - _p[0], xr));
    else
        p[0] = w * _p[0];

    if(_p[1] > m[1])
        p[1] = w * (-m[1] + fmod(_p[1] + m[1], yr));
    else if(_p[1] < -m[1])
        p[1] = w * (m[1] - fmod(m[1] - _p[1], yr));
    else
        p[1] = w * _p[1];
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
    p[0] = w * (_p[0] + pop2[0] * sin(SafeTan(_p[1]*pop2c)));
    p[1] = w * (_p[1] + pop2[1] * sin(SafeTan(_p[0]*pop2c)));
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
    float r, a, c, m_CompFac;
    m_CompFac = 1 - angle * count *M_1_PI * 0.5;
    r = SUMSQ(_p);
    a = ATANYX(_p) + swirl * r;
    c = floor((count * a + M_PI) * M_1_PI * 0.5);
    a = a * m_CompFac + c * angle;
    r = w * (r + hole);
    p[0] = r * cos(a);
    p[1] = r * sin(a);
}
// 76 ( parametric ) // const vector precalc)
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
/*
// 76 ( parametric ) // const vector precalc)
void V_WEDGEJULIA(vector2 p; const vector2 _p; const float w, power, angle, dist, count, wedgeJulia_cf, wedgeJulia_rN, wedgeJulia_cn){ 
    float rr, t_rnd, aa, cc, sa, ca;

    rr = w * pow(SUMSQ(_p), wedgeJulia_cn);
    t_rnd = (int)((wedgeJulia_rN)*nrandom("twister"));
    aa = (ATANYX(_p) + 2 * M_PI * t_rnd) / power;
    cc = floor( (count * aa + M_PI)*M_1_PI*0.5 );
    aa = aa * wedgeJulia_cf + cc * angle;
    sincos(aa, sa, ca);
    p[0] = rr * ca;
    p[1] = rr * sa;
}
// 76 L ( parametric )
void V_WEDGEJULIA_L(vector2 p; const vector2 _p; const float w, power, angle, dist, count; const vector precalc){
    float wedgeJulia_cf, wedgeJulia_rN, wedgeJulia_cn, rr, t_rnd, aa, cc, sa, ca;
    // precalc
    wedgeJulia_cf = precalc[0];
    wedgeJulia_rN = precalc[1];
    wedgeJulia_cn = precalc[2];

    V_WEDGEJULIA(p, _p, w, power, angle, dist, count, wedgeJulia_cf, wedgeJulia_rN, wedgeJulia_cn);
}
// 76 FF ( parametric )
void V_WEDGEJULIA_FF(vector2 p; const vector2 _p; const float w, power, angle, dist, count){
    float wedgeJulia_cf, wedgeJulia_rN, wedgeJulia_cn, rr, t_rnd, aa, cc, sa, ca;
    // precalc
    vector precalc;
    precalc_V_WEDGEJULIA(precalc, power, angle, dist, count);
    wedgeJulia_cf = precalc[0];
    wedgeJulia_rN = precalc[1];
    wedgeJulia_cn = precalc[2];

    V_WEDGEJULIA(p, _p, w, power, angle, dist, count, wedgeJulia_cf, wedgeJulia_rN, wedgeJulia_cn);
}
*/
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
void V_EXP(vector2 p; const vector2 _p; const float w){
    float expe, expz, expsin, expcos;
    expe = w * exp(_p[0]);
    p[0] = expe * cos(_p[1]);
    p[1] = expe * sin(_p[1]);
}
// 81
void V_LOG(vector2 p; const vector2 _p; const float w){
    p[0] = w * 0.5 * log(SUMSQ(_p));
    p[1] = w * ATANYX(_p);
}
// 82
void V_SIN(const int f3c; vector2 p; const vector2 _p; const float w){
    if(f3c){
        p[0] = w * sin(_p[0]) * cosh(_p[1]);
        p[1] = w * cos(_p[0]) * sinh(_p[1]);  
    }
    else{
        float x, y;
        x = _p[0] * M_PI_2;
        y = _p[1] * M_PI_2;
        p[0] = w * sin(x) * cosh(y);
        p[1] = w * cos(x) * sinh(y);
    }
}
// 83
void V_COS(const int f3c; vector2 p; const vector2 _p; const float w){
    if(f3c){
        p[0] = w * cos(_p[0]) * cosh(_p[1]);
        p[1] = -(w * sin(_p[0]) * sinh(_p[1])); }
    else{
        float x, y;
        x = _p[0] * M_PI_2;
        y = _p[1] * M_PI_2;
        p[0] = w * cos(x) * cosh(y);
        p[1] = w * -sin(x) * sinh(y); }
}
// 84
void V_TAN(const int f3c; vector2 p; const vector2 _p; const float w){
    float tansin, tancos, tansinh, tancosh, tanden;
    if(f3c){
        sincos(2 * _p[0], tansin, tancos);
        tansinh = sinh(2 * _p[1]);
        tancosh = cosh(2 * _p[1]);
        tanden = 1 / Zeps(tancos + tancosh);
        p[0] = w * tanden * tansin;
        p[1] = w * tanden * tansinh;}
    else{
        float x, y, den;
        x = _p[0] * M_PI_2;
        y = _p[1] * M_PI_2;
        den = w / Zeps(cos(x) + cosh(y));
        p[0] = sin(x) * den;
        p[1] = sinh(y) * den;}
}
// 85
void V_SEC(const int f3c; vector2 p; const vector2 _p; const float w){
    float secsin, seccos, secsinh, seccosh, secden;
    if(f3c){
        sincos(_p[0], secsin, seccos);
        secsinh = sinh(_p[1]);
        seccosh = cosh(_p[1]);
        secden = 2.0/(cos(2.0*_p[0]) + cosh(2.0*_p[1]));
        p[0] = w * secden * seccos * seccosh;
        p[1] = w * secden * secsin * secsinh;}
    else{
        float x, y;
        x = _p[0] * M_PI;
        y = _p[1] * M_PI;
        sincos(x, secsin, seccos);
        secsinh = sinh(y);
        seccosh = cosh(y);
        secden = w * (2 / Zeps(cos(2 * x) + cosh(2 * y)));
        p[0] = secden * seccos * seccosh;
        p[1] = secden * secsin * secsinh;  
    }
}
// 86 This somehow do not work as expected...
void V_CSC(const int f3c; vector2 p; const vector2 _p; const float w){
    float cscsin, csccos, cscsinh, csccosh, cscden;
    if(f3c){
        sincos(_p[0], cscsin, csccos);
        cscsinh = sinh(_p[1]);
        csccosh = cosh(_p[1]);
        cscden = 2 / Zeps(cosh(2 * _p[1]) - cos(2 * _p[0]));
        p[0] = w * cscden * cscsin * csccosh;
        p[1] = -(w * cscden * csccos * cscsinh);
    }
    else{
        float x, y, d;
        x = _p[0] * M_PI_2;
        y = _p[1] * M_PI_2;
        sincos(x, cscsin, csccos);
        cscsinh = sinh(y);
        csccosh = cosh(y);
        d = 1 + 2 * cscsinh * cscsinh - cos(2 * x);
        cscden = 2 * w / d;
        p[0] = cscden * cscsin * csccosh;
        p[1] = cscden * csccos * cscsinh;}
}
// 87
void V_COT(const int f3c; vector2 p; const vector2 _p; const float w){
    float cotsin, cotcos, cotsinh, cotcosh, cotden;
    if(f3c){
        sincos(2.0*_p[0], cotsin, cotcos);
        cotsinh = sinh(2.0*_p[1]);
        cotcosh = cosh(2.0*_p[1]);
        cotden = 1.0/(cotcosh - cotcos);
        p[0] = w * cotden * cotsin;
        p[1] = w * cotden * -1 * cotsinh;}
    else{
        float x, y;
        x = _p[0] * M_PI_2;
        y = _p[1] * M_PI_2;
        sincos(x, cotsin, cotcos);
        cotsinh = sinh(y);
        cotcosh = cosh(y);
        cotden = w / Zeps(cotcosh - cotcos);
        p[0] = cotden * cotsin;
        p[1] = cotden * cotsinh;
    }
}
// 88
void V_SINH(const int f3c; vector2 p; const vector2 _p; const float w){
    float sinhsin, sinhcos, sinhsinh, sinhcosh;
    if(f3c){
        sincos(_p[1], sinhsin, sinhcos);
        sinhsinh = sinh(_p[0]);
        sinhcosh = cosh(_p[0]);
        p[0] = w * sinhsinh * sinhcos;
        p[1] = w * sinhcosh * sinhsin; }
    else{
        float x, y;
        x = _p[0] * M_PI_4;
        y = _p[1] * M_PI_4;
        sincos(y, sinhsin, sinhcos);
        sinhsinh = sinh(x);
        sinhcosh = cosh(x);
        p[0] = w * sinhsinh * sinhcos;
        p[1] = w * sinhcosh * sinhsin;
    }
}
// 89
void V_COSH(const int f3c; vector2 p; const vector2 _p; const float w){
    float coshsin, coshcos, coshsinh, coshcosh;
    if(f3c){
        sincos(_p[1], coshsin, coshcos);
        coshsinh = sinh(_p[0]);
        coshcosh = cosh(_p[0]);
        p[0] = w * coshcosh * coshcos;
        p[1] = w * coshsinh * coshsin; }
    else{
        float x, y;
        x = _p[0] * M_PI_2;
        y = _p[1] * M_PI_2;
        sincos(y, coshsin, coshcos);
        coshsinh = sinh(x);
        coshcosh = cosh(x);
        p[0] = w * coshcosh * coshcos;
        p[1] = w * coshsinh * coshsin;
    }
}
// 90
void V_TANH(const int f3c; vector2 p; const vector2 _p; const float w){
    float tanhsin, tanhcos, tanhsinh, tanhcosh, tanhden;
    if(f3c){
        sincos(2.0*_p[1], tanhsin, tanhcos);
        tanhsinh = sinh(2 * _p[0]);
        tanhcosh = cosh(2 * _p[0]);
        tanhden = 1 / Zeps(tanhcos + tanhcosh);
        p[0] = w * tanhden * tanhsinh;
        p[1] = w * tanhden * tanhsin;}
    else{
        float x, y;
        x = _p[0] * M_PI_2;
        y = _p[1] * M_PI_2;
        sincos(y, tanhsin, tanhcos);
        tanhsinh = sinh(x);
        tanhcosh = cosh(x);
        tanhden = w / Zeps(tanhcos + tanhcosh);
        p[0] = tanhden * tanhsinh;
        p[1] = tanhden * tanhsin;
    }
}
// 91
void V_SECH(const int f3c; vector2 p; const vector2 _p; const float w){
    float sechsin, sechcos, sechsinh, sechcosh, sechden;
    if(f3c){
        sincos(_p[1], sechsin, sechcos);
        sechsinh = sinh(_p[0]);
        sechcosh = cosh(_p[0]);
        sechden = 2 / Zeps(cos(2 * _p[1]) + cosh(2 * _p[0]));
        p[0] = w * sechden * sechcos * sechcosh;
        p[1] = -(w * sechden * sechsin * sechsinh); }
    else{
        float x, y;
        x = _p[0] * M_PI_4;
        y = _p[1] * M_PI_4;
        sincos(y, sechsin, sechcos);
        sechsinh = sinh(x);
        sechcosh = cosh(x);
        sechden = w * (2 / Zeps(cos(y * 2) + cosh(x * 2)));
        p[0] = sechden * sechcos * sechcosh;
        p[1] = sechden * sechsin * sechsinh;
    }
}
// 92
void V_CSCH(const int f3c; vector2 p; const vector2 _p; const float w){
    float cschsin, cschcos, cschsinh, cschcosh, cschden;
    if(f3c){
        sincos(_p[1], cschsin, cschcos);
        cschsinh = sinh(_p[0]);
        cschcosh = cosh(_p[0]);
        cschden = 2 / Zeps(cosh(2 * _p[0]) - cos(2 * _p[1]));
        p[0] = w * cschden * cschsinh * cschcos;
        p[1] = -(w * cschden * cschcosh * cschsin);
    }
    else{
        float x, y;
        x = _p[0] * M_PI_4;
        y = _p[1] * M_PI_4;
        sincos(y, cschsin, cschcos);
        cschsinh = sinh(x);
        cschcosh = cosh(x);
        cschden = w * (2 / Zeps(cosh(2 * x) - cos(2 * y)));
        p[0] = cschden * cschsinh * cschcos;
        p[1] = cschden * cschcosh * cschsin; }
}
// 93
void V_COTH(const int f3c; vector2 p; const vector2 _p; const float w){
    float cothsin, cothcos, cothsinh, cothcosh, cothden;
    if(f3c){
        sincos(2.0*_p[1], cothsin, cothcos);
        cothsinh = sinh(2.0*_p[0]);
        cothcosh = cosh(2.0*_p[0]);
        cothden = 1.0/Zeps(cothcosh - cothcos);
        p[0] = w * cothden * cothsinh;
        p[1] = w * cothden * cothsin; }
    else{
        float x, y;
        x = _p[0] * M_PI_2;
        y = _p[1] * M_PI_2;
        sincos(y, cothsin, cothcos);
        cothsinh = sinh(x);
        cothcosh = cosh(x);
        cothden = w / Zeps(cothcosh - cothcos);
        p[0] = cothden * cothsinh;
        p[1] = cothden * cothsin;
    }
}
// 94 ( parametric )
void V_AUGER(vector2 p; const vector2 _p; const float w, freq, scale, sym, ww){
    float  s, t, uu, dy, dx;
    float m_HalfScale = scale/2.0;
    s = sin(freq * _p[0]);
    t = sin(freq * _p[1]);
    dx = _p[0] + ww * (m_HalfScale * t + abs(_p[0]) * t);
    dy = _p[1] + ww * (m_HalfScale * s + abs(_p[1]) * s);
    p[0] = w * (_p[0] + sym * (dx - _p[0]));
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
    p[0] = w * _p[0] + a[0] * exp(-_p[1] * _p[1] * l[0]);
    p[1] = w * _p[1] + a[1] * exp(-_p[0] * _p[0] * l[1]);
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

/*
// BWRAPS PRECALC
//
// 99 ( parametric )
void V_BWRAPS(vector2 p; const vector2 _p; const float w, cellsize, space, gain, innertwist, outertwist, g2, r2, rfactor){
    float max_bubble, Vx, Vy, Cx, Cy, Lx, Ly, rr, theta, ss, cc;
    
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
// 99 L ( parametric )
void V_BWRAPS_L(vector2 p; const vector2 _p; const float w, cellsize, space, gain, innertwist, outertwist; const vector precalc){
    float g2, r2, rfactor, max_bubble, Vx, Vy, Cx, Cy, Lx, Ly, rr, theta, ss, cc;
    // precalc
    g2 = precalc[0];
    r2  = precalc[1];
    rfactor  = precalc[2];

    V_BWRAPS(p, _p, w, cellsize, space, gain, innertwist, outertwist, g2, r2, rfactor);
}
// 99 FF ( parametric )
void V_BWRAPS_FF(vector2 p; const vector2 _p; const float w, cellsize, space, gain, innertwist, outertwist){
    float g2, r2, rfactor, max_bubble, Vx, Vy, Cx, Cy, Lx, Ly, rr, theta, ss, cc;
    // precalc
    vector precalc;
    precalc_V_BWRAPS(precalc, cellsize, space, gain)
    g2 = precalc[0];
    r2  = precalc[1];
    rfactor  = precalc[2];

    V_BWRAPS(p, _p, w, cellsize, space, gain, innertwist, outertwist, g2, r2, rfactor);
}
*/

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
    xp = pow(abs(w) * abs(_p[0]), pow[0]);
    yp = pow(abs(w) * abs(_p[1]), pow[1]);
    p[0] = xp * sgn(_p[0]) + lc[0] * _p[0] + sc[0];
    p[1] = yp * sgn(_p[1]) + lc[1] * _p[1] + sc[1];
}
// 102 ( parametric )
// const float left, top, right, bottom, area, zero(int) )
// prm "zero" need to only be different from Zero to do its job ;)
void V_CROP(vector2 p; const vector2 _p; const float w, m_X0, m_Y0, m_X1, m_Y1, m_S, m_Z;){
    // crop precalc
    float m_W, m_H, m_X0_, m_Y0_, m_X1_, m_Y1_;
    if (m_X0 < m_X1){
        m_X0_ = m_X0;
        m_X1_ = m_X1; }
    else{
        m_X0_ = m_X1;
        m_X1_ = m_X0; }
    if (m_Y0 < m_Y1){
        m_Y0_ = m_Y0;
        m_Y1_ = m_Y1; }
    else{
        m_Y0_ = m_Y1;
        m_Y1_ = m_Y0; }
    m_W = (m_X1_ - m_X0_) * 0.5 * m_S;
    m_H = (m_Y1_ - m_Y0_) * 0.5 * m_S;

    // crop compute
    float x, y;
    x = _p[0];
    y = _p[1];
    if (((x < m_X0_) || (x > m_X1_) || (y < m_Y0_) || (y > m_Y1_)) && m_Z != 0){
        x = 0;
        y = 0;
    }
    else{
        if (x < m_X0_)
            x = m_X0_ + nrandom('twister') * m_W;
        else if (x > m_X1_)
            x = m_X1_ - nrandom('twister') * m_W;

        if (y < m_Y0_)
            y = m_Y0_ + nrandom('twister') * m_H;
        else if (y > m_Y1_)
            y = m_Y1_ - nrandom('twister') * m_H;
    }
    p[0] = w * x;
    p[1] = w * y;
}
// 103
void V_UNPOLAR(vector2 p; const vector2 _p; const float w){
    float m_Vvar2, r, s, c;
    // precalc
    m_Vvar2 = (w / M_PI) * 0.5;
    // unpolar compute
    r = exp(_p[1]);
    sincos(_p[0], s, c);
    p[0] = m_Vvar2 * r * s;
    p[1] = m_Vvar2 * r * c;
}
// 104
void V_GLYNNIA(vector2 p; const vector2 _p; const float w){
    float d, r, m_V2;
    // precalc
    m_V2 = w * sqrt(2) / 2;
    // glynnia compute
    r = SQRT(_p);
    if (r > 1){
        if (nrandom('twister')>0.5){
            d = sqrt(r + _p[0]);
            p[0] = m_V2 * d;
            p[1] = -(m_V2 / d * _p[1]); }
        else{
            d = r + _p[0];
            r = w / sqrt(r * ((_p[1]*_p[1]) + (d*d)));
            p[0] = r * d;
            p[1] = r * _p[1]; } 
        }
    else{
        if (nrandom('twister')>0.5){
            d = Zeps(sqrt(r + _p[0]));
            p[0] = -(m_V2 * d);
            p[1] = -(m_V2 / d * _p[1]); }
        else{
            d = r + _p[0];
            r = w / Zeps(sqrt(r * ((_p[1]*_p[1]) + (d*d))));
            p[0] = -(r * d);
            p[1] = r * _p[1]; } 
        }
}
// 105 ( parametric )
void V_POINT_SYMMETRY(vector2 p; const vector2 _p; const float w, m_Order, m_X, m_Y){
    float angle, dx, dy, cosa, sina, m_TwoPiDivOrder;
    // precalc
    m_TwoPiDivOrder = M_2PI / Zeps(m_Order);
    // compute
    angle = floor(nrandom("twister") * m_Order) * m_TwoPiDivOrder;
    dx = (_p[0] - m_X) * w;
    dy = (_p[1] - m_Y) * w;
    cosa = cos(angle);
    sina = sin(angle);
    p[0] = m_X + dx * cosa + dy * sina;
    p[1] = m_Y + dy * cosa - dx * sina;
}

#endif
