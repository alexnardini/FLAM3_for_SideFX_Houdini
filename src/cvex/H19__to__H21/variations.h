#ifndef __variations_h__
#define __variations_h__

/*  
 /  Tested on:  Houdini 19.0
 /              Houdini 19.5
 /              Houdini 20.0
 /              Houdini 20.5
 /              Houdini 21.0
 /
 /  Title:      FLAM3H™. SideFX Houdini FLAM3: 2D
 /  Author:     Alessandro Nardini
 /  date:       October 2020, Last revised December 2025
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
 /  Name:       VARIATIONS "CVEX"
 /
 /  Comment:    FLAM3 variations.
*/




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
    float _px, _py;
    assign(_px, _py, _p);

    p = w * set(sin(_px), sin(_py));
}
// 02
void V_SPHERICAL(vector2 p; const vector2 _p; const float w){
    float r2 = w / Zeps(SUMSQ(_p));

    p = r2 * _p;
}
// 03
void V_SWIRL(vector2 p; const vector2 _p; const float w){
    float rr, c1, c2, nx, ny, _px, _py;
    assign(_px, _py, _p);

    rr = SUMSQ(_p);
    c1 = sin(rr);
    c2 = cos(rr);
    nx = c1 * _px - c2 * _py;
    ny = c2 * _px + c1 * _py;

    p = w * set(nx, ny);
}
// 04
void V_HORSESHOE(vector2 p; const vector2 _p; const float w){
    float rr, _px, _py;
    assign(_px, _py, _p);
    rr = w / Zeps(SQRT(_p));

    p = set((_px - _py) * (_px + _py) * rr, 2.0 * _px * _py * rr);
}
// 05
void V_POLAR(vector2 p; const vector2 _p; const float w){
    float nx, ny;
    nx = ATAN(_p) * M_1_PI;
    ny = SQRT(_p) - 1.0;

    p = w * set(nx, ny);
}
// 06
void V_HANDKERCHIEF(vector2 p; const vector2 _p; const float w){
    float a = ATAN(_p);
    float _SQRT = SQRT(_p);

    p = w * _SQRT * set(sin(a+_SQRT), cos(a-_SQRT));
}
// 07
void V_HEART(vector2 p; const vector2 _p; const float w){
    float a, r, _SQRT;
    _SQRT = SQRT(_p);
    a = _SQRT * ATAN(_p);
    r = w * _SQRT;

    p = set(r * sin(a), (-r) * cos(a));
}
// 08
void V_DISC(vector2 p; const vector2 _p; const float w){
    float a, r, sr, cr;
    a = ATAN(_p) * M_1_PI;
    r = M_PI * SQRT(_p);
    sincos(r, sr,cr);

    p = w * set(sr, cr) * a;
}
// 09 (precalc _p)
void V_SPIRAL(vector2 p; const vector2 _p; const float w){
    float r, _SQRT, r1, sr, cr;
    _SQRT = SQRT(_p);
    vector2 precalc = _p / _SQRT;
    r = Zeps(_SQRT);
    r1 = w/r;
    sincos(r, sr, cr);

    p = r1 * set((precalc[1] + sr), (precalc[0] - cr));
}
// 10 (precalc _p)
void V_HIPERBOLIC(vector2 p; const vector2 _p; const float w){
    float _SQRT = SQRT(_p);
    float rr = Zeps(_SQRT);
    vector2 precalc = _p / _SQRT;

    p = w * set(precalc[0] / rr, precalc[1] * rr);
}
// 11 (precalc _p)
void V_DIAMOND(vector2 p; const vector2 _p; const float w){
    float a, r, _px, _py;
    assign(_px, _py, _p);
    a = atan2(_px, _py);
    r = SQRT(_p);

    p = w * set(sin(a) * cos(r), cos(a) * sin(r));
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

    p = w * set(m0 + m1, m0 - m1);
}
// 13
void V_JULIA(vector2 p; const vector2 _p; const float w){
    float r, a, sa, ca;
    a = 0.5 * ATAN(_p);
    if(nrandom('twister')<0.5)
        a += M_PI;
    r = w * sqrt(SQRT(_p));
    sincos(a, sa, ca);

    p = r * set(ca, sa);
}
// 14
void V_BENT(vector2 p; const vector2 _p; const float w){
    float nx, ny, _px, _py;
    assign(_px, _py, _p);
    nx = _px;
    ny = _py;
    if(nx < 0.0) nx = nx * 2.0;
    if(ny < 0.0) ny = ny / 2.0;

    p = w * set(nx, ny);
}
// 15
void V_WAVES(vector2 p; const vector2 _p; const float w, b, c, e, f){
    // precalc
    float m_Dx2, m_Dy2, nx, ny, _px, _py;
    assign(_px, _py, _p);
    m_Dx2 = 1 / Zeps(c * c);
    m_Dy2 = 1 / Zeps(f * f);
    // compute
    nx = _px + b * sin(_py * m_Dx2);
    ny = _py + e * sin(_px * m_Dy2);

    p = w * set(nx, ny);
}
// 16
void V_FISHEYE(vector2 p; const vector2 _p; const float w){
    float r = SQRT(_p);
    r = 2 * w / (r+1);

    p = r * _p;
}
// 17
void V_POPCORN(vector2 p; const vector2 _p; const float w, c, f){
    float dx, dy, nx, ny, _px, _py;
    assign(_px, _py, _p);

    dx = tan(3*_py);
    dy = tan(3*_px);
    nx = _px + c * sin(dx);
    ny = _py + f * sin(dy);

    p = w * set(nx, ny);
}
// 18
void V_EXPONENTIAL(vector2 p; const vector2 _p; const float w){
    float dx, dy, sdy, cdy, _px, _py;
    assign(_px, _py, _p);

    dx = w * exp(_px-1.0);
    dy = M_PI * _py;
    sincos(dy, sdy, cdy);

    p = dx * set(cdy, sdy);
}
// 19 (precalc _p)
void V_POWER(vector2 p; const vector2 _p; const float w){
    float _SQRT = SQRT(_p);
    vector2 precalc = _p / _SQRT;
    float r = w * pow(_SQRT, precalc[0]);

    p = r * precalc.yx;
}
// 20
void V_COSINE(vector2 p; const vector2 _p; const float w){
    float a, sa, ca, nx, ny, _px, _py;
    assign(_px, _py, _p);

    a = _px * M_PI;
    sincos(a, sa, ca);
    nx = ca * cosh(_py);
    ny = -sa * sinh(_py);

    p = w * set(nx, ny);
}
// 21 (precalc _p)
void V_RINGS(vector2 p; const vector2 _p; const float w, d){
    float dx, rr, _SQRT;
    _SQRT = SQRT(_p);
    vector2 precalc = _p / _SQRT;
    
    dx = Zeps(d*d);
    rr = _SQRT;
    rr = w * (fmod(rr+dx, 2*dx) - dx + rr * (1 - dx));

    p = rr * precalc.yx;
}
// 22
void V_FAN(vector2 p; const vector2 _p; const float w, c, f){
    float dx, dx2, dy, a, r, sa, ca;
    dx = M_PI * Zeps(c*c);
    dy = f;
    dx2 = 0.5 * dx;
    a = ATAN(_p);
    r = w * SQRT(_p);
    a += (fmod(a+dy,dx) > dx2) ? -dx2 : dx2;
    sincos(a, sa, ca);

    p = r * set(ca, sa);
}
// 23
void V_BUBBLE(vector2 p; const vector2 _p; const float w){
    float r, _px, _py;
    assign(_px, _py, _p);

    r = w / (0.25 * SUMSQ(_p) + 1);

    p = r * _p;
}
// 24
void V_CYLINDER(vector2 p; const vector2 _p; const float w){
    float _px, _py;
    assign(_px, _py, _p);

    p = w * set(sin(_px), _py);
}
// 25
void V_EYEFISH(vector2 p; const vector2 _p; const float w){
    float r =  (w * 2.0) / (1.0 + SQRT(_p));

    p = r * _p;
}
// 26
void V_BLUR(vector2 p; const float w){
    float tmpr, sinr, cosr, r;
    tmpr = nrandom("twister") * M_TAU;
    sincos(tmpr, sinr, cosr);
    r = w * nrandom("twister");

    p = r * set(cosr, sinr);
}
// 27 ( parametric )
void V_CURL(vector2 p; const vector2 _p; const float w; const vector2 c){
    float c1, c2, re, im, r, _px, _py;
    assign(_px, _py, _p);
    assign(c1, c2, c);

    // From FRACTORIUM
    re = 1.0 + c1 * _px + c2 * ((_px*_px) - (_py*_py));
    im = c1 * _py + (2.0*c2) *  _px * _py;
    r = w / Zeps((re*re) + (im*im));

    p = r * set((_px * re + _py * im), (_py * re - _px * im));

    // From APOPHYSIS
    // if(c1==0){
    //     if(c2==0){
    //         p[0] = w * _p[0];
    //         p[1] = w * _p[1];
    //     }
    //     else{
    //         re = 1.0 + c2 * ((_p[0]*_p[0]) - (_p[1]*_p[1]));
    //         im = c2*2.0*_p[0]*_p[1];
    //         r = w / (re*re + im*im);
    //         p[0] = (_p[0] * re + _p[1] * im) * r;
    //         p[1] = (_p[1] * re - _p[0] * im) * r;
    //     }
    // }
    // else{
    //     if(c2==0){
    //         re = 1.0 + c1*_p[0];
    //         im = c1*_p[1];
    //         r = w / (re*re + im*im);
    //         p[0] = (_p[0] * re + _p[1] * im) * r;
    //         p[1] = (_p[1] * re - _p[0] * im) * r;
    //     }
    //     else{
    //         re = 1.0 + c1*_p[0] + c2 * ((_p[0]*_p[0]) - (_p[1]*_p[1]));
    //         im = c1*_p[1] + c2*2.0*_p[0]*_p[1];
    //         r = w / (re*re + im*im);
    //         p[0] = (_p[0]*re + _p[1]*im)*r;
    //         p[1] = (_p[1]*re - _p[0]*im)*r;
    //     }
    // }
}
// 28 ( parametric )
void V_NGON(vector2 p; const vector2 _p; const float w; const vector4 ngon){
    float pow, sides, corners, circle, cpower, csides, csidesinv, r_factor, theta, phi, amp, _px, _py;
    assign(_px, _py, _p);
    assign(pow, sides, corners, circle, ngon);

    cpower = -0.5*pow; csides = 2.0*PI/sides; csidesinv = 1.0/csides;
    r_factor = (_px==0 && _py==0) ? 0 : pow(SUMSQ(_p), cpower);
    theta = ATANYX(_p);
    phi = theta - csides * floor(theta*csidesinv);
    if(phi>0.5*csides) phi -= csides;
    amp = (corners * (1.0/cos(phi) - 1.0) + circle) * w * r_factor;

    p = amp * _p;
}
// 29 ( parametric )
void V_PDJ(vector2 p; const vector2 _p; const float w; const vector4 pp){
    float  nx1, nx2, ny1, ny2, a, b, c, d, _px, _py;
    assign(_px, _py, _p);
    assign(a, b, c, d, pp);

    nx1 = cos(b * _px);
    nx2 = sin(c * _px);
    ny1 = sin(a * _py);
    ny2 = cos(d * _py);

    p = w * set(ny1 - nx1, nx2 - ny2);
}
// 30 ( parametric ) (precalc _p)
void V_BLOB(vector2 p; const vector2 _p; const float w; const vector blob){
    float _SQRT, low, high, wave, blob_coeff, rr, aa, bdiff;
    _SQRT = SQRT(_p);
    vector2 precalc = _p / _SQRT;
    assign(low, high, wave, blob);

    rr = _SQRT;
    aa = ATAN(_p);
    bdiff = high - low;
    rr = rr * (low + bdiff * (0.5 + 0.5 * sin(wave * aa)));

    p = w * rr * precalc;
}
// 31 ( parametric )
void V_JULIAN(vector2 p; const vector2 _p; const float w; const vector2 julian){
    int t_rnd;
    float power, jdist, julian_rN, julian_cn, tmpr, rr, sina, cosa;
    assign(power, jdist, julian);

    julian_rN = power;
    julian_cn = jdist / power / 2.0;
    t_rnd = (int)trunc(julian_rN * nrandom('twister'));
    tmpr = ( ATANYX(_p) + M_TAU * t_rnd ) / power;
    rr = w * pow( SUMSQ(_p), julian_cn );
    sincos(tmpr, sina, cosa);

    p = rr * set(cosa, sina);
}
// 32 ( parametric )
void V_JULIASCOPE(vector2 p; const vector2 _p; const float w; const vector2 juliascope){
    int t_rnd;
    float _ATANYX, power, jdist, julian_rN, julian_cn, tmpr, rr, sina, cosa;
    assign(power, jdist, juliascope);

    _ATANYX = ATANYX(_p);
    julian_rN = power;
    julian_cn = jdist / power / 2.0;
    t_rnd = (int)trunc(julian_rN * nrandom('twister'));
    tmpr = ((t_rnd & 1) == 0) ? (M_TAU * t_rnd + _ATANYX) / power : (M_TAU * t_rnd - _ATANYX) / power;
    sincos(tmpr, sina, cosa);
    rr = w * pow( SUMSQ(_p), julian_cn );

    p = rr * set(cosa, sina);
}
// 33
void V_GAUSSIAN_BLUR(vector2 p; const float w){
    float ang, rr, sina, cosa;
    ang = nrandom('twister') * M_TAU;
    rr = w * (nrandom('twister')+nrandom('twister')+nrandom('twister')+nrandom('twister') - 2.0);

    p = rr * set(cos(ang), sin(ang));
}
// 34 ( parametric )
void V_FAN2(vector2 p; const vector2 _p; const float w; const vector2 fan2){
    float dx, dx2, dy, aa, sa,ca,rr, tt, fx, fy;
    assign(fx, fy, fan2);
    dy = fy;
    dx = M_PI * Zeps(fx*fx);
    dx2 = 0.5*dx;
    aa = ATAN(_p);
    rr = w * SQRT(_p);
    tt = aa + dy - dx * (int)((aa + dy)/dx);
    aa = (tt>dx2) ? aa-dx2 : aa+dx2;
    sincos(aa, sa, ca);

    p = rr * set(sa, ca);
}
// 35 ( parametric ) (precalc _p)
void V_RINGS2(vector2 p; const vector2 _p; const float w, rings2val){
    float _SQRT, rr, dx;
    int nrand;
    _SQRT = SQRT(_p);
    vector2 precalc = _p / _SQRT;
    rr = _SQRT;
    dx = rings2val*rings2val;
    rr += -2.0*dx*(int)((rr+dx)/(2.0*dx)) + rr * (1.0-dx);

    p = w * rr * precalc;
}
// 36 ( parametric )
void V_RECTANGLES(vector2 p; const vector2 _p; const float w; const vector2 rect){
    float _px, _py, rx, ry, x, y;
    assign(rx, ry, rect);
    assign(_px, _py, _p);

    if(rx==0) x = w * _px;
    else x = w * ((2 * floor(_px / rx) + 1) * rx - _px);
    if(ry==0) y = w * _py;
    else y = w * ((2 * floor(_py / ry) + 1) * ry - _py);

    p = set(x, y);
}
// 37 ( parametric )
void V_RADIALBLUR(vector2 p; const vector2 _p; const float w, angle){
    float rndG, tmpa, ra, rz, sa, ca, m_spin, m_zoom, _px, _py;
    assign(_px, _py, _p);

    // precalc ( this probably better done inside the genome.h )
    sincos(angle * M_PI_2, m_spin, m_zoom);

    // compute
    rndG = w * (nrandom('twister')+nrandom('twister')+nrandom('twister')+nrandom('twister') - 2.0);
    ra = SQRT(_p);
    tmpa = ATANYX(_p) + m_spin*rndG;
    sincos(tmpa, sa, ca);
    rz = m_zoom * rndG - 1;

    p = ra * set(ca, sa) + rz * _p;
}
// 38 ( parametric )
void V_PIE(vector2 p; const float w; const vector pie){
    float slices, thickness, rotation, aa, rr, sa, ca, sl;
    assign(slices, thickness, rotation, pie);

    sl = (int)(nrandom('twister')*slices);
    aa = rotation + M_TAU * (sl + nrandom("twister") * thickness) / slices;
    rr = w * nrandom('twister');
    sincos(aa, sa, ca);

    p = rr * set(ca, sa);
}
// 39
void V_ARCH(vector2 p; const vector2 _p; const float w){
    float ang, sinr, cosr;
    ang = nrandom("twister") * w * M_PI;
    sincos(ang, sinr, cosr);

    p = w * set(sinr, (sinr*sinr)/cosr);
}
// 40
void V_TANGENT(vector2 p; const vector2 _p; const float w){
    float _px, _py;
    assign(_px, _py, _p);

    p = w * set((sin(_px)/cos(_py)), tan(_py));
}
// 41
void V_SQUARE(vector2 p; const vector2 _p; const float w){
    p = w * set((nrandom("twister") - 0.5), (nrandom("twister") - 0.5));
}
// 42
void V_RAYS(vector2 p; const vector2 _p; const float w){
    float ang, rr, tanrr, _px, _py;
    assign(_px, _py, _p);

    ang = w * nrandom("twister") * M_PI;
    rr = w / Zeps(SUMSQ(_p));
    tanrr = w * tan(ang) * rr;

    p = tanrr * set(cos(_px), sin(_py));
}
// 43
void V_BLADE(vector2 p; const vector2 _p; const float w){
    float rr, sinr, cosr, _px, _py;
    assign(_px, _py, _p);

    rr = nrandom("twister") * w * SQRT(_p);
    sincos(rr, sinr, cosr);

    p = w * _px * set(cosr + sinr, cosr - sinr);
}
// 44
void V_SECANT2(vector2 p; const vector2 _p; const float w){
    float rr, cr, sr, icr, isr, _px; _px=_p[0];
    rr = w * SQRT(_p);
    cr = cos(rr);
    sr = sin(rr);
    icr = 1.0/cr;

    p = set(w * _px, (cr<0) ? w*(icr+1) : w*(icr-1));
}
// 45
void V_TWINTRIAN(vector2 p; const vector2 _p; const float w){
    float rr, sinr, cosr, diff, _px, _py;
    assign(_px, _py, _p);

    rr = nrandom("twister") * w * SQRT(_p);
    sincos(rr, sinr, cosr);
    diff = log10(sinr*sinr)+cosr;
    if(!isfinite(diff) || isnan(diff))
        diff = -30.0;

    p = w * _px * set(diff, diff - sinr * M_PI);
}
// 46
void V_CROSS(vector2 p; const vector2 _p; const float w){
    float ss, rr, _px, _py;
    assign(_px, _py, _p);

    ss = _px*_px - _py*_py;
    rr = w * sqrt(1.0 / Zeps(ss*ss));

    p = rr * _p;
}
// 47 ( parametric )
void V_DISC2(vector2 p; const vector2 _p; const float w; const vector2 disc2; const vector disc2_pc){
    float rot, twist, disc2_timespi, disc2_sinadd, disc2_cosadd, rr, tt, sinr, cosr;
    assign(rot, twist, disc2);
    assign(disc2_timespi, disc2_sinadd, disc2_cosadd, disc2_pc);

    // PRECALC done inside its detail wrangle core in the Houdini environment
    tt = disc2_timespi * sum(_p);
    sincos(tt, sinr, cosr);
    rr = w * ATAN(_p) / M_PI;

    p = rr * set(sinr + disc2_cosadd, cosr + disc2_sinadd);
}
// // 47 L ( parametric )
// void V_DISC2_L(vector2 p; const vector2 _p; const float w, rot, twist; const vector precalc){
//     float disc2_sinadd, disc2_cosadd, disc2_timespi;
//     // precalc
//     disc2_timespi = precalc[0];
//     disc2_sinadd  = precalc[1];
//     disc2_cosadd  = precalc[2];

//     V_DISC2(p, _p, w, rot, twist, disc2_timespi, disc2_sinadd, disc2_cosadd);
// }
// 47 FF ( parametric )
void V_DISC2_FF(vector2 p; const vector2 _p; const float w; const vector2 disc2){
    float rot, twist, a, b, c;
    vector precalc;
    assign(rot, twist, disc2);

    // precalc
    precalc_V_DISC2(precalc, rot, twist);

    // Execute var
    V_DISC2(p, _p, w, disc2, precalc);
}
// 48 ( parametric )
void V_SUPERSHAPE(vector2 p; const vector2 _p; const float w; const vector ss; const vector ss_n){
    float ss_m, ss_rnd, ss_holes, theta, st, ct, tt1, tt2, rr, ss_pm_4, ss_pneg1_n1, ss_nx, ss_ny, ss_nz;
    assign(ss_m, ss_rnd, ss_holes, ss);
    assign(ss_nx, ss_ny, ss_nz, ss_n);

    // PRECALC
    ss_pm_4 = ss_m / 4.0;
    ss_pneg1_n1 = -1.0 / ss_nx;

    theta = ss_pm_4 * ATANYX(_p) + M_PI_4;
    sincos(theta, st, ct);
    tt1 = abs(ct);  tt1 = pow(tt1, ss_ny);
    tt2 = abs(st);  tt2 = pow(tt2, ss_nz);
    float SQRT = SQRT(_p);
    rr = w * ((ss_rnd*nrandom('twister') + (1.0-ss_rnd)*SQRT) - ss_holes) * pow(tt1+tt2, ss_pneg1_n1) / SQRT;

    p = rr * _p;
}
// 49 ( parametric )
void V_FLOWER(vector2 p; const vector2 _p; const float w; const vector2 flower){
    float petals, holes, theta, rr;
    assign(petals, holes, flower);

    theta = ATANYX(_p);
    rr = w * (nrandom("twister") - holes) * cos(petals*theta) / SQRT(_p);

    p = rr * _p;
}
// 50 ( parametric )
void V_CONIC(vector2 p; const vector2 _p; const float w; const vector2 conic){
    float eccentricity, holes, ct, rr, _px, _py;
    assign(_px, _py, _p);
    assign(eccentricity, holes, conic);

    float SQRT = SQRT(_p);
    ct = _px / SQRT;
    rr = w * (nrandom("twister") - holes) * eccentricity / (1 + eccentricity*ct) / SQRT;

    p = rr * _p;
}
// 51 ( parametric )
void V_PARABOLA(vector2 p; const vector2 _p; const float w; const vector2 parabola){
    float height, width, rr, sr, cr;
    assign(height, width, parabola);

    rr = SQRT(_p);
    sincos(rr, sr, cr);

    p = w * set(height * sr*sr * nrandom("twister"), width  * cr * nrandom("twister"));
}
// 52 ( parametric )
void V_BENT2(vector2 p; const vector2 _p; const float w; const vector2 bent2){
    float nx, ny, b2x, b2y;
    assign(nx, ny, _p);
    assign(b2x, b2y, bent2);
    
    if(nx < 0.0)
        nx = nx * b2x;
    if(ny < 0.0)
        ny = ny * b2y;

    p = w * set(nx, ny);
}
// 53 ( parametric )
void V_BIPOLAR(vector2 p; const vector2 _p; const float w, shift){
    float x2y2, tt, x2, ps, y, _px, _py;
    assign(_px, _py, _p);

    x2y2 = SUMSQ(_p);
    tt = x2y2+1;
    x2 = 2*_px;
    ps = -M_PI_2 * shift;
    y = 0.5 * atan2(2.0 * _py, x2y2 - 1.0) + ps;
    if(y > M_PI_2) y = -M_PI_2 + fmod(y + M_PI_2, M_PI);
    else if (y < -M_PI_2) y = M_PI_2 - fmod(M_PI_2 - y, M_PI);

    p = w * set(0.25 * M_2_PI * log((tt+x2) / (tt-x2)), M_2_PI * y);
}
// 54
void V_BOARDERS(vector2 p; const vector2 _p; const float w){
    float roundX, roundY, offsetX, offsetY, _px, _py;
    assign(_px, _py, _p);

    roundX = rint(_px);
    roundY = rint(_py);
    offsetX = _px - roundX;
    offsetY = _py - roundY;
    if(nrandom("twister")>=0.75){
        p = set(offsetX, offsetY) * 0.5 + set(roundX, roundY);
    }
    else{
        if (abs(offsetX) >= abs(offsetY)) {
            if (offsetX >= 0.0){
                p = w * set((offsetX*0.5 + roundX + 0.25), (offsetY*0.5 + roundY + 0.25 * offsetY / offsetX));
            } 
            else{
                p = w * set((offsetX*0.5 + roundX - 0.25), (offsetY*0.5 + roundY - 0.25 * offsetY / offsetX)); 
            }
        }
            else{
                if (offsetY >= 0.0){
                    p = w * set((offsetX*0.5 + roundX + offsetX/offsetY*0.25), (offsetY*0.5 + roundY + 0.25));
                } 
                else{
                    p = w * set((offsetX*0.5 + roundX - offsetX/offsetY*0.25), (offsetY*0.5 + roundY - 0.25));
                }
            }
    }
}
// 55
void V_BUTTERFLY(vector2 p; const vector2 _p; const float w){
    float wx, y2, rr, _px, _py;
    assign(_px, _py, _p);

    wx = w*1.3029400317411197908970256609023;
    y2 = _py*2.0;
    rr = wx*sqrt(abs(_py*_px)/(Zeps(_px*_px + y2*y2)));

    p = rr * set(_px, y2);
}
// 56 ( parametric )
void V_CELL(vector2 p; const vector2 _p; const float w, size){
    float inv_cell_size, x, y, dx, dy, _px, _py;
    assign(_px, _py, _p);

    inv_cell_size = 1 / size;
    x = floor(_px * inv_cell_size);
    y = floor(_py * inv_cell_size);
    dx = _px - x * size;
    dy = _py - y * size;
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

    p = set(w * (dx + x * size), -(w * (dy + y * size)));
}
// 57 ( parametric )
void V_CPOW(vector2 p; const vector2 _p; const float w; const vector cpow){
    float power, pow_r, pow_i, aa, lnr, va, vc, vd, ang, sa, ca, mm;
    assign(power, pow_r, pow_i, cpow);

    aa = ATANYX(_p);
    lnr = 0.5 * log(SUMSQ(_p));
    va = M_TAU / power;
    vc = pow_r / power;
    vd = pow_i / power;
    ang = vc*aa + vd*lnr + va * floor(power * nrandom("twister"));
    mm = w * exp(vc * lnr - vd * aa);
    sincos(ang, sa, ca);

    p = mm * set(ca, sa);
}
// 58
void V_EDISC(vector2 p; const vector2 _p; const float w){
    float tmp, tmp2, rr1, rr2, xmax, aa1, aa2, ww, snv, csv, snhu, cshu, _px, _py;
    assign(_px, _py, _p);

    tmp = SUMSQ(_p) + 1;
    tmp2 = 2.0 * _px;
    rr1 = sqrt(tmp+tmp2);
    rr2 = sqrt(tmp-tmp2);
    xmax = Zeps((rr1+rr2) * 0.5);
    aa1 = log(xmax + (sqrt(xmax - 1.0)));
    aa2 = -acos(_px/xmax);
    ww = w / 11.57034632;
    sincos(aa1, snv, csv);
    snhu = sinh(aa2);
    cshu = cosh(aa2);
    if(_py > 0.0) snv = -snv;

    p = ww * set(cshu * csv, snhu * snv);
}
// 59
void V_ELLIPTIC(vector2 p; const vector2 _p; const float w){

    // FLAM3 version
    //
    /*
    float tmp, xmax, aa, bb, ww, _px, _py;
    assign(_px, _py, _p);

    tmp = SUMSQ(_p) + 1.0;
    x2 = 2.0 * _px;
    xmax = 0.5 * (sqrt(tmp+x2) + sqrt(tmp-x2));
    aa = _px / xmax;
    bb = 1.0 - aa*aa;
    ssx = xmax - 1.0;
    ww = w / M_PI_2;
    bb = (bb<0) ? 0 : sqrt(bb);
    ssx = (ssx<0) ? 0 : sqrt(ssx);
    p[0] = ww * atan2(aa,bb);
    p[1] = (_py > 0) ? ww*log(xmax+ssx) : ww * -log(xmax+ssx);
    */


    // An improved Elliptic version which helps with rounding errors. Give its best at 64bit(DP).
    // Even at 32bit(SP) is already much much better than the original FLAM3 version, so I keep this one.
    // Source: https://mathr.co.uk/blog/2017-11-01_a_more_accurate_elliptic_variation.html
    //
    float x2, sq, u, v, xmaxm1, a, ssx, weightDivPiDiv2, _px, _py;
    assign(_px, _py, _p);

    x2 = 2.0 * _px;
    sq = SUMSQ(_p);
    u = sq + x2;
    v = sq - x2;
    xmaxm1 = 0.5 * (Sqrt1pm1(u) + Sqrt1pm1(v));
    a = _px / (1 + xmaxm1);
    ssx = xmaxm1;
    weightDivPiDiv2 = w / M_PI_2;
    ssx = (ssx<0) ? 0 : sqrt(ssx);
  
    p = set(weightDivPiDiv2 * asin(clamp(a, -1, 1)), (_py > 0) ? weightDivPiDiv2 * log1p(xmaxm1 + ssx) : -(weightDivPiDiv2 * log1p(xmaxm1 + ssx)));
}
// 60
void V_NOISE(vector2 p; const vector2 _p; const float w){
    float tmpr, sinr, cosr, rr;

    tmpr = nrandom("twister") * M_TAU;
    sincos(tmpr, sinr, cosr);
    rr = w * nrandom("twister");

    p = _p * rr * set(cosr, sinr);
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

    p = mm * set(cn, sn);
}
// 62
void V_FOCI(vector2 p; const vector2 _p; const float w){
    float expx, expnx, sn, cn, tmp, _px, _py;
    assign(_px, _py, _p);

    expx = exp(_px) * 0.5;
    expnx = 0.25 / Zeps(expx);
    sincos(_py, sn, cn);
    tmp = w / Zeps(expx + expnx - cn);

    p = tmp * set(expx - expnx, sn);
}
// 63 ( parametric )
void V_LAZYSUSAN(vector2 p; const vector2 _p; const float w; const vector lazysusan; const vector2 lazy){
    float spin, twist, space, xx, yy, rr, sina, cosa, aa, _px, _py, lx, ly;
    assign(_px, _py, _p);
    assign(spin, twist, space, lazysusan);
    assign(lx, ly, lazy);

    xx = _px - lx;
    yy = _py + ly;
    rr = SQRT(set(xx,yy));
    if(rr<w){
        aa = ATANYX(set(xx,yy)) + spin + twist * (w - rr);
        sincos(aa, sina, cosa);
        rr = w * rr;

        p = rr * set(cosa + lx, sina - ly);
    }
    else{
        rr = w * (1.0 + space / rr);

        p = rr * set(xx + lx, yy - ly);
    }
}
// 64
void V_LOONIE(vector2 p; const vector2 _p; const float w){
    float rr, rr2, w2, _px, _py;
    assign(_px, _py, _p);

    rr2 = SUMSQ(_p);
    w2 = w * w;
    if(rr2 < w2){
        rr = w * sqrt(w2/rr2 - 1.0);
        p = rr * _p;
    }
    else{
        p = w * _p;
    }
}
// 65
void V_PREBLUR(vector2 p; const float w){
    float rndG, rndA, sinA, cosA;
    rndG = w * (nrandom("twister") + nrandom("twister") + nrandom("twister") + nrandom("twister") - 2.0);
    rndA = nrandom("twister") * M_TAU;
    sincos(rndA, sinA, cosA);

    p += rndG * set(cosA, sinA);
}
// 66 ( parametric )
void V_MODULUS(vector2 p; const vector2 _p; const float w; const vector2 m){
    float mx, my, xr, yr, _px, _py, x, y;
    assign(_px, _py, _p);
    assign(mx, my, m);
    
    xr=2*mx; yr=2*my;
    if(_px > mx)
        x = w * (-mx + fmod(_px + mx, xr));
    else if(_px < -mx)
        x = w * (mx - fmod(mx - _px, xr));
    else
        x = w * _px;

    if(_py > my)
        y = w * (-my + fmod(_py + my, yr));
    else if(_py < -my)
        y = w * (my - fmod(my - _py, yr));
    else
        y = w * _py;

    p = set(x, y);
}
// 67 ( parametric )
void V_OSCOPE(vector2 p; const vector2 _p; const float w; const vector4 oscope){
    float freq, amp, damp, sep, tpf, tt, _px, _py;
    assign(_px, _py, _p);
    assign(freq, amp, damp, sep, oscope);

    tpf = M_TAU * freq;
    if(damp == 0.0) tt = amp * cos(tpf*_px) + sep;
    else tt = amp * exp(-abs(_px)* damp) * cos(tpf*_px) + sep;
    if(abs(_py) <= tt){

        p = w * set(_px, -_py);
    }
    else{
        p = w * _p;
    }
}
// 68
void V_POLAR2(vector2 p; const vector2 _p; const float w){
    float p2v = w / M_PI;
    p = set(p2v * ATAN(_p), p2v/2.0 * log(SUMSQ(_p)));
    }
// 69 ( parametric )
void V_POPCORN2(vector2 p; const vector2 _p; const float w, pop2c; const vector2 pop2){
    float _px, _py, pop2x, pop2y;
    assign(_px, _py, _p);
    assign(pop2x, pop2y, pop2);

    p = w * (_p + set(pop2x, pop2y) * set(sin(SafeTan(_py*pop2c)), sin(SafeTan(_px*pop2c))));
}
// 70 ( parametric )
void V_SCRY(vector2 p; const vector2 _p; const float w){
    float tt, rr;

    tt = SUMSQ(_p);
    rr = 1.0 / (SQRT(_p) * (tt + 1.0/Zeps(w)));

    p = rr * _p;
}
// 71 ( parametric )
void V_SEPARATION(vector2 p; const vector2 _p; const float w; const vector2 sep, ins){
    float sx, sy, sx2, sy2, _px, _py, ix, iy, x, y;
    assign(sx, sy, sep);
    assign(_px, _py, _p);
    assign(ix, iy, ins);

    sx2 = sx*sx;
    sy2 = sy*sy;
    if(_px > 0.0) x = w * (sqrt(_px*_px + sx2) - _px*ix);
    else x = w * -(sqrt(_px*_px + sx2) + _px*ix);
    if(_py > 0.0) y = w * (sqrt(_py*_py + sy2) - _py*iy);
    else y = w * -(sqrt(_py*_py + sy2) + _py*iy);

    p = set(x, y);
}
// 72 ( parametric )
void V_SPLIT(vector2 p; const vector2 _p; const float w; const vector2 split){
    float _px, _py, sx, sy, x, y;
    assign(_px, _py, _p);
    assign(sx, sy, split);

    if(cos(_px*sx*M_PI) >= 0) y = w * _py;
    else y = w * -_py;
    if(cos(_py*sy*M_PI) >= 0) x = w * _px;
    else x = w * -_px;

    p = set(x, y);
}
// 73 ( parametric )
void V_SPLITS(vector2 p; const vector2 _p; const float w; const vector2 splits){
    float _px, _py, sx, sy, x, y;
    assign(_px, _py, _p);
    assign(sx, sy, splits);

    if(_px >= 0) x = w * (_px + sx);
    else x = w * (_px - sx);
    if(_py >= 0) y = w * (_py + sy);
    else y = w * (_py - sy);

    p = set(x, y);
}
// 74 ( parametric )
void V_STRIPES(vector2 p; const vector2 _p; const float w; const vector2 stripes){
    float space, warp, roundx, offsetx, _px, _py;
    assign(_px, _py, _p);
    assign(space, warp, stripes);

    roundx = floor(_px + 0.5);
    offsetx = _px - roundx;

    p = w * set((offsetx * (1.0 - space) + roundx), (_py + offsetx*offsetx*warp));
}
// 75 ( parametric )
void V_WEDGE(vector2 p; const vector2 _p; const float w; const vector4 wedge){
    float swirl, angle, hole, count, r, a, c, m_CompFac;
    assign(swirl, angle, hole, count, wedge);

    m_CompFac = 1 - angle * count * M_1_2PI;
    r = SQRT(_p);
    a = ATANYX(_p) + swirl * r;
    c = floor((count * a + M_PI) * M_1_2PI);
    a = a * m_CompFac + c * angle;
    r = w * (r + hole);

    p = r * set(cos(a), sin(a));
}
// 76 ( parametric ) // const vector precalc)
void V_WEDGEJULIA(vector2 p; const vector2 _p; const float w; const vector4 wedgejulia){ 
    float power, angle, dist, count, wedgeJulia_cf, wedgeJulia_rN, wedgeJulia_cn, rr, t_rnd, aa, cc, sa, ca;
    assign(power, angle, dist, count, wedgejulia);

    // PRECALC
    wedgeJulia_cf = 1.0 - angle * count * M_1_2PI;
    wedgeJulia_rN = abs(power);
    wedgeJulia_cn = dist / power / 2.0;

    rr = w * pow(SUMSQ(_p), wedgeJulia_cn);
    t_rnd = (int)((wedgeJulia_rN)*nrandom("twister"));
    aa = (ATANYX(_p) + M_TAU * t_rnd) / power;
    cc = floor( (count * aa + M_PI) * M_1_2PI );
    aa = aa * wedgeJulia_cf + cc * angle;
    sincos(aa, sa, ca);

    p = rr * set(ca, sa);
}
// 77 ( parametric )
void V_WEDGESPH(vector2 p; const vector2 _p; const float w; const vector4 wedgesph){
    float swirl, angle, hole, count, rr, aa, cc, comp_fac, sa, ca;
    assign(swirl, angle, hole, count, wedgesph);

    rr = 1.0/Zeps(SQRT(_p));
    aa = ATANYX(_p) + swirl * rr;
    cc = floor( (count * aa + M_PI) * M_1_2PI );
    comp_fac = 1 - angle*count * M_1_2PI;
    aa = aa * comp_fac + cc * angle;
    sincos(aa, sa, ca);
    rr = w * (rr + hole);

    p = rr * set(ca, sa);
}
// 78 ( parametric )
void V_WHORL(vector2 p; const vector2 _p; const float w; const vector2 whorl){
    float inside, outside, rr, aa, sa, ca;
    assign(inside, outside, whorl);

    rr = SQRT(_p);
    if(rr<w) aa = ATANYX(_p) + inside/(w-rr);
    else aa = ATANYX(_p) + outside/(w-rr);
    sincos(aa, sa, ca);

    p = w * rr * set(ca, sa);
}
// 79 ( parametric )
void V_WAVES2(vector2 p; const vector2 _p; const float w; const vector2 scl, freq){
    p = w * (_p + scl * sin(_p.yx * freq));
}
// 80
void V_EXP(vector2 p; const vector2 _p; const float w){
    float expe, expz, expsin, expcos, _px, _py;
    assign(_px, _py, _p);
    expe = w * exp(_px);

    p = expe * set(cos(_py), sin(_py));
}
// 81
void V_LOG(vector2 p; const vector2 _p; const float w){

    p = w * set(0.5 * log(SUMSQ(_p)), ATANYX(_p));
}
// 82
void V_SIN(const int f3c; vector2 p; const vector2 _p; const float w){
    float _px, _py;
    assign(_px, _py, _p);

    if(f3c){
        p = w * set(sin(_px) * cosh(_py), cos(_px) * sinh(_py));
    }
    else{
        float x, y;
        x = _px * M_PI_2;
        y = _py * M_PI_2;

        p = w * set(sin(x) * cosh(y), cos(x) * sinh(y));
    }
}
// 83
void V_COS(const int f3c; vector2 p; const vector2 _p; const float w){
    float _px, _py;
    assign(_px, _py, _p);

    if(f3c){
        p = set(w * cos(_px) * cosh(_py), -(w * sin(_px) * sinh(_py))); }
    else{
        float x, y;
        x = _px * M_PI_2;
        y = _py * M_PI_2;

        p = w * set(cos(x) * cosh(y), -sin(x) * sinh(y)); }
}
// 84
void V_TAN(const int f3c; vector2 p; const vector2 _p; const float w){
    float tansin, tancos, tansinh, tancosh, tanden, _px, _py;
    assign(_px, _py, _p);

    if(f3c){
        sincos(2 * _px, tansin, tancos);
        tansinh = sinh(2 * _py);
        tancosh = cosh(2 * _py);
        tanden = 1 / Zeps(tancos + tancosh);

        p = w * tanden * set(tansin, tansinh);}
    else{
        float x, y, den;
        x = _px * M_PI_2;
        y = _py * M_PI_2;
        den = w / Zeps(cos(x) + cosh(y));

        p = set(sin(x) * den, sinh(y) * den);
    }
}
// 85
void V_SEC(const int f3c; vector2 p; const vector2 _p; const float w){
    float secsin, seccos, secsinh, seccosh, secden, _px, _py;
    assign(_px, _py, _p);

    if(f3c){
        sincos(_px, secsin, seccos);
        secsinh = sinh(_py);
        seccosh = cosh(_py);
        secden = 2.0/(cos(2.0*_px) + cosh(2.0*_py));

        p = w * secden * set(seccos * seccosh, secsin * secsinh);}
    else{
        float x, y;
        x = _px * M_PI;
        y = _py * M_PI;
        sincos(x, secsin, seccos);
        secsinh = sinh(y);
        seccosh = cosh(y);
        secden = w * (2 / Zeps(cos(2 * x) + cosh(2 * y)));

        p = secden * set(seccos * seccosh, secsin * secsinh); 
    }
}
// 86 This somehow do not work as expected...
void V_CSC(const int f3c; vector2 p; const vector2 _p; const float w){
    float cscsin, csccos, cscsinh, csccosh, cscden, _px, _py;
    assign(_px, _py, _p);

    if(f3c){
        sincos(_px, cscsin, csccos);
        cscsinh = sinh(_py);
        csccosh = cosh(_py);
        cscden = 2 / Zeps(cosh(2 * _py) - cos(2 * _px));

        p = set(w * cscden * cscsin * csccosh, -(w * cscden * csccos * cscsinh));
    }
    else{
        float x, y, d;
        x = _px * M_PI_2;
        y = _py * M_PI_2;
        sincos(x, cscsin, csccos);
        cscsinh = sinh(y);
        csccosh = cosh(y);
        d = 1 + 2 * cscsinh * cscsinh - cos(2 * x);
        cscden = 2 * w / d;

        p = cscden * set(cscsin * csccosh, csccos * cscsinh);}
}
// 87
void V_COT(const int f3c; vector2 p; const vector2 _p; const float w){
    float cotsin, cotcos, cotsinh, cotcosh, cotden, _px, _py;
    assign(_px, _py, _p);

    if(f3c){
        sincos(2.0*_px, cotsin, cotcos);
        cotsinh = sinh(2.0*_py);
        cotcosh = cosh(2.0*_py);
        cotden = 1.0/(cotcosh - cotcos);

        p = w * cotden * set(cotsin, -1 * cotsinh);}
    else{
        float x, y;
        x = _px * M_PI_2;
        y = _py * M_PI_2;
        sincos(x, cotsin, cotcos);
        cotsinh = sinh(y);
        cotcosh = cosh(y);
        cotden = w / Zeps(cotcosh - cotcos);

        p = cotden * set(cotsin, cotsinh);
    }
}
// 88
void V_SINH(const int f3c; vector2 p; const vector2 _p; const float w){
    float sinhsin, sinhcos, sinhsinh, sinhcosh, _px, _py;
    assign(_px, _py, _p);

    if(f3c){
        sincos(_py, sinhsin, sinhcos);
        sinhsinh = sinh(_px);
        sinhcosh = cosh(_px);

        p = w * set(sinhsinh * sinhcos, sinhcosh * sinhsin);}
    else{
        float x, y;
        x = _px * M_PI_4;
        y = _py * M_PI_4;
        sincos(y, sinhsin, sinhcos);
        sinhsinh = sinh(x);
        sinhcosh = cosh(x);

        p = w * set(sinhsinh * sinhcos, sinhcosh * sinhsin);
    }
}
// 89
void V_COSH(const int f3c; vector2 p; const vector2 _p; const float w){
    float coshsin, coshcos, coshsinh, coshcosh, _px, _py;
    assign(_px, _py, _p);

    if(f3c){
        sincos(_py, coshsin, coshcos);
        coshsinh = sinh(_px);
        coshcosh = cosh(_px);

        p = w * set(coshcosh * coshcos, coshsinh * coshsin);}
    else{
        float x, y;
        x = _px * M_PI_2;
        y = _py * M_PI_2;
        sincos(y, coshsin, coshcos);
        coshsinh = sinh(x);
        coshcosh = cosh(x);

        p = w * set(coshcosh * coshcos, coshsinh * coshsin);
    }
}
// 90
void V_TANH(const int f3c; vector2 p; const vector2 _p; const float w){
    float tanhsin, tanhcos, tanhsinh, tanhcosh, tanhden, _px, _py;
    assign(_px, _py, _p);

    if(f3c){
        sincos(2.0*_py, tanhsin, tanhcos);
        tanhsinh = sinh(2 * _px);
        tanhcosh = cosh(2 * _px);
        tanhden = 1 / Zeps(tanhcos + tanhcosh);

        p = w * tanhden * set(tanhsinh, tanhsin);}
    else{
        float x, y;
        x = _px * M_PI_2;
        y = _py * M_PI_2;
        sincos(y, tanhsin, tanhcos);
        tanhsinh = sinh(x);
        tanhcosh = cosh(x);
        tanhden = w / Zeps(tanhcos + tanhcosh);

        p = tanhden * set(tanhsinh, tanhsin);
    }
}
// 91
void V_SECH(const int f3c; vector2 p; const vector2 _p; const float w){
    float sechsin, sechcos, sechsinh, sechcosh, sechden, _px, _py;
    assign(_px, _py, _p);

    if(f3c){
        sincos(_py, sechsin, sechcos);
        sechsinh = sinh(_px);
        sechcosh = cosh(_px);
        sechden = 2 / Zeps(cos(2 * _py) + cosh(2 * _px));

        p = set(w * sechden * sechcos * sechcosh, -(w * sechden * sechsin * sechsinh));}
    else{
        float x, y;
        x = _px * M_PI_4;
        y = _py * M_PI_4;
        sincos(y, sechsin, sechcos);
        sechsinh = sinh(x);
        sechcosh = cosh(x);
        sechden = w * (2 / Zeps(cos(y * 2) + cosh(x * 2)));

        p = sechden * set(sechcos * sechcosh, sechsin * sechsinh);
    }
}
// 92
void V_CSCH(const int f3c; vector2 p; const vector2 _p; const float w){
    float cschsin, cschcos, cschsinh, cschcosh, cschden, _px, _py;
    assign(_px, _py, _p);

    if(f3c){
        sincos(_py, cschsin, cschcos);
        cschsinh = sinh(_px);
        cschcosh = cosh(_px);
        cschden = 2 / Zeps(cosh(2 * _px) - cos(2 * _py));

        p = set(w * cschden * cschsinh * cschcos, -(w * cschden * cschcosh * cschsin));
    }
    else{
        float x, y;
        x = _px * M_PI_4;
        y = _py * M_PI_4;
        sincos(y, cschsin, cschcos);
        cschsinh = sinh(x);
        cschcosh = cosh(x);
        cschden = w * (2 / Zeps(cosh(2 * x) - cos(2 * y)));

        p = cschden * set(cschsinh * cschcos, cschcosh * cschsin);}
}
// 93
void V_COTH(const int f3c; vector2 p; const vector2 _p; const float w){
    float cothsin, cothcos, cothsinh, cothcosh, cothden, _px, _py;
    assign(_px, _py, _p);

    if(f3c){
        sincos(2.0*_py, cothsin, cothcos);
        cothsinh = sinh(2.0*_px);
        cothcosh = cosh(2.0*_px);
        cothden = 1.0/Zeps(cothcosh - cothcos);

        p = w * cothden * set(cothsinh, cothsin);}
    else{
        float x, y;
        x = _px * M_PI_2;
        y = _py * M_PI_2;
        sincos(y, cothsin, cothcos);
        cothsinh = sinh(x);
        cothcosh = cosh(x);
        cothden = w / Zeps(cothcosh - cothcos);

        p = cothden * set(cothsinh, cothsin);
    }
}
// 94 ( parametric )
void V_AUGER(vector2 p; const vector2 _p; const float w; const vector4 auger){
    float  freq, scale, sym, ww, s, t, uu, dy, dx, _px, _py;
    assign(_px, _py, _p);
    assign(freq, scale, sym, ww, auger);

    float m_HalfScale = scale/2.0;
    s = sin(freq * _px);
    t = sin(freq * _py);
    dx = _px + ww * (m_HalfScale * t + abs(_px) * t);
    dy = _py + ww * (m_HalfScale * s + abs(_py) * s);

    p = w * set((_px + sym * (dx - _px)), dy);
}
// 95 ( parametric )
void V_FLUX(vector2 p; const vector2 _p; const float w, spread){
    float xpw, xmw, avgr, avga, _px, _py;
    assign(_px, _py, _p);

    xpw = _px + w;
    xmw = _px - w;
    avgr = w * (2 + spread) * sqrt(sqrt(_py*_py+xpw*xpw) / sqrt(_py*_py + xmw*xmw));
    avga = ( atan2(_py, xmw) - atan2(_py, xpw)) * 0.5;

    p = avgr * set(cos(avga), sin(avga));
}
// 96 ( parametric )
void V_MOBIUS(vector2 p; const vector2 _p; const float w; const vector4 re, im){
    float reu, imu, rev, imv, radv, _px, _py, reA, reB, reC, reD, imA, imB, imC, imD;
    assign(_px, _py, _p);
    assign(reA, reB, reC, reD, re);
    assign(imA, imB, imC, imD, im); 

    reu = reA * _px - imA * _py + reB;
    imu = reA * _py + imA * _px + imB;
    rev = reC * _px - imC * _py + reD;
    imv = reC * _py + imC * _px + imD;
    radv = w / (rev*rev + imv*imv);

    p = radv * set((reu*rev + imu*imv), (imu*rev - reu*imv));
}
// 97 ( parametric )
void V_CURVE(vector2 p; const vector2 _p; const float w; const vector2 l, a){
    p = w * _p + a * exp(-_p.yx * _p.yx * l);
}
// 98 ( parametric )
void V_PERSPECTIVE(vector2 p; const vector2 _p; const float w; const vector2 persp){
    float angle, dist, tt, vsin, vfcos, _px, _py;
    assign(_px, _py, _p);
    assign(angle, dist, persp);

    // PRECALC
    float ang = angle * M_PI_2;
    vsin = sin(ang);
    vfcos = dist * cos(ang);
    tt = 1.0 / (dist - _py * vsin);

    p = w * set(dist * _px * tt, vfcos * _py * tt);
}
// 99 ( parametric )
void V_BWRAPS(vector2 p; const vector2 _p; const float w; const vector bwraps; const vector2 twist){
    float cellsize, space, gain, innertwist, outertwist, g2, r2, rfactor, max_bubble, Vx, Vy, Cx, Cy, Lx, Ly, rr, theta, ss, cc;
    assign(Vx, Vy, _p);
    assign(cellsize, space, gain, bwraps);
    assign(innertwist, outertwist, twist);

    // PRECALC
    float radius = 0.5 * (cellsize / (1.0 + space*space ));
    g2 = sqrt(gain) / cellsize + 1e-6;
    max_bubble = g2 * radius;
    max_bubble = (max_bubble>2.0) ? 1.0 : max_bubble*1.0/( (max_bubble*max_bubble)/4.0+1.0);
    r2 = radius*radius;
    rfactor = radius/max_bubble;

    if(cellsize == 0.0){

        p = w * _p;
    }
    else{
        Cx = (floor(Vx / cellsize) + 0.5) * cellsize;
        Cy = (floor(Vy / cellsize) + 0.5) * cellsize;
        Lx = Vx - Cx;
        Ly = Vy - Cy;
        if((Lx*Lx + Ly*Ly) > r2){

            p = w * _p;
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

            p = w * set(Vx, Vy);
        }
    }
}
// 100
void V_HEMISPHERE(vector2 p; const vector2 _p; const float w){
    float tt = w / sqrt(SUMSQ(_p) + 1);

    p = tt * _p;
}
// 101 ( parametric )
void V_POLYNOMIAL(vector2 p; const vector2 _p; const float w; const vector2 pow, lc, sc){
    float xp, yp, pwx, pwy, lx, ly, sx, sy, _px, _py;
    assign(_px, _py, _p);
    assign(pwx, pwy, pow);
    assign(lx, ly, lc);
    assign(sx, sy, sc);

    xp = pow(abs(w) * abs(_px), pwx);
    yp = pow(abs(w) * abs(_py), pwy);

    p = set(xp * sgn(_px) + lx * _px + sx, yp * sgn(_py) + ly * _py + sy);
}
// 102 ( parametric )
// ltrb -> const float left, top, right, bottom
// az -> area, zero(int) - prm "zero" need to only be different from Zero to do its job ;)
void V_CROP(vector2 p; const vector2 _p; const float w; const vector4 ltrb; const vector2 az;){
    float x, y, m_X0, m_Y0, m_X1, m_Y1, m_S, m_Z;
    assign(x, y, _p);
    assign(m_X0, m_Y0, m_X1, m_Y1, ltrb);
    assign(m_S, m_Z, az);

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
    p = w * set(x, y);
}
// 103
void V_UNPOLAR(vector2 p; const vector2 _p; const float w){
    float m_Vvar2, r, s, c, _px, _py;
    assign(_px, _py, _p);

    // precalc
    m_Vvar2 = (w / M_PI) * 0.5;
    // unpolar compute
    r = exp(_py);
    sincos(_px, s, c);

    p = m_Vvar2 * r * set(s, c);
}
// 104
void V_GLYNNIA(vector2 p; const vector2 _p; const float w){
    float d, r, m_V2, _px, _py;
    assign(_px, _py, _p);

    // precalc
    m_V2 = w * sqrt(2) / 2;
    // glynnia compute
    r = SQRT(_p);
    if (r > 1){
        if (nrandom('twister')>0.5){
            d = sqrt(r + _px);

            p = set(m_V2 * d, -(m_V2 / d * _py));}
        else{
            d = r + _px;
            r = w / sqrt(r * ((_py*_py) + (d*d)));

            p = r * set(d, _py);} 
        }
    else{
        if (nrandom('twister')>0.5){
            d = Zeps(sqrt(r + _px));

            p = set(-(m_V2 * d), -(m_V2 / d * _py));}
        else{
            d = r + _px;
            r = w / Zeps(sqrt(r * ((_py*_py) + (d*d))));

            p = set(-(r * d), r * _py);}
        }
}
// 105 ( parametric )
void V_POINT_SYMMETRY(vector2 p; const vector2 _p; const float w; const vector ptsym){
    float m_Order, m_X, m_Y, angle, dx, dy, cosa, sina, m_TwoPiDivOrder, _px, _py;
    assign(_px, _py, _p);
    assign(m_Order, m_X, m_Y, ptsym);
    
    // precalc
    m_TwoPiDivOrder = M_TAU / Zeps(m_Order);
    // compute
    angle = floor(nrandom("twister") * m_Order) * m_TwoPiDivOrder;
    dx = (_px - m_X) * w;
    dy = (_py - m_Y) * w;
    cosa = cos(angle);
    sina = sin(angle);

    p = set(m_X, m_Y) + set(dx, dy) * cosa + set(dy, -dx) * sina;
}

#endif
