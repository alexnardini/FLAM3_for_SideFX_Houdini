#ifndef __variations_h__
#define __variations_h__

/*  
 /  Title:      SideFX Houdini FRACTAL FLAME generator: 2D
 /  Author:     Alessandro Nardini
 /  date:       October 2020, Last revised April 2021
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

float sgn(float n) { return (n < 0) ? -1 : (n > 0) ? 1 : 0; }

// Dnt need this yet
// float rndsgn(){ float n = nrandom("twister")+nrandom("twister") - 1.0; return (n < 0) ? -1 : (n > 0) ? 1 : 0; }

void sincos(float a, sa, ca){ sa=sin(a); ca=cos(a); }

float fmod(float a, b){ return (a-floor(a/b)*b); }

float precalc(string type; vector pos){
    if(type=="SUMSQ")        return (pos[0]*pos[0] + pos[1]*pos[1]);
    else if(type=="SQRT")    return sqrt((pos[0]*pos[0] + pos[1]*pos[1]));
    else if(type=="ATAN")    return atan2(pos[0], pos[1]);
    else if(type=="ATANYX")  return atan2(pos[1], pos[0]);
    return 0;
}

// Incorporated all precalc functions inside their own variation's function.
// Reasons are to generate a smaller file size on compile and faster first node instance creation time.
//
/*
void perspective_precalc(float angle, dist, vsin, vfcos){
    float ang = angle * M_PI / 2.0;
    vsin = sin(ang);
    vfcos = dist * cos(ang);
}

void waves_precalc(float dx2, dy2, dz2, F, H){
    dx2 = 1.0/(F*F + EPS);
    dy2 = 1.0/(H*H + EPS);
}

void disc2_precalc(float rot, twist, sinadd, cosadd, timespi){
    float k;
    timespi = rot * M_PI;
    sincos(twist, sinadd, cosadd);
    cosadd -= 1;
    if(twist > ( 2*M_PI)){ k = (1 + twist - 2*M_PI); cosadd*=k; sinadd*=k; }
    if(twist < (-2*M_PI)){ k = (1 + twist + 2*M_PI); cosadd*=k; sinadd*=k; }
}

void supershape_precalc(float ss_m, ss_n1, ss_pm_4, ss_pneg_n1){
    ss_pm_4 = ss_m / 4.0;
    ss_pneg_n1 = -1.0 / ss_n1;
}

void wedgejulia_precalc(float wedgeJulia_cf, wedgeJulia_rN, wedgeJulia_cn, power, angle, dist, count){
    wedgeJulia_cf = 1.0 - angle * count * M_1_PI * 0.5;
    wedgeJulia_rN = abs(power);
    wedgeJulia_cn = dist / power / 2.0;
}

void bwraps_precalc(float g2, r2, rfactor, cellsize, space, gain){
    float radius = 0.5 * (cellsize / (1.0 + space*space ));
    g2 = sqrt(gain) / cellsize + 1e-6;
    float max_bubble = g2 * radius;
    if(max_bubble>2.0) max_bubble=1.0;
    else max_bubble *= 1.0/( (max_bubble*max_bubble)/4.0+1.0);
    r2 = radius*radius;
    rfactor = radius/max_bubble;
}
*/

vector biunitcube(){
    return set(fit01(nrandom('twister'), -1, 1), fit01(nrandom('twister'), -1, 1), 0); }

int checkNAN_vector(int ACTIVE, ptn; vector vec){
    if(ACTIVE){
        if(!isfinite(vec[0]) || !isfinite(vec[1]) || isnan(vec[0]) || isnan(vec[1]) || length(vec)>LIMIT) return 1; }
    return 0;
}

void removeNAN_vector(int ACTIVE, ptn; vector vec){ if(checkNAN_vector(ACTIVE, ptn, vec))  removepoint(0, ptn); }

int checkNAN_float(int ACTIVE, ptn; float flt){ if(ACTIVE){ if(!isfinite(flt) || isnan(flt) || flt>LIMIT) return 1; } return 0; }

void removeNAN_float(int ACTIVE, ptn; float flt){ if(checkNAN_float(ACTIVE, ptn, flt)) removepoint(0, ptn); }

void VAR_SYMMETRY(vector pos, pivot; int num, active){
    if(active){
        float angle = 0;
        // 3-way
        if(!num){
            if(nrandom('twister')>(1.0/3.0)){
                angle = 120;
                if(nrandom('twister')>0.5) angle = 240;
                pos *= maketransform(0, 0, 0, set(0, 0, angle), 1, pivot);
            }
        }
        // 5-way
        else if(num){
            if(nrandom('twister')>=0.2){
                float sym = nrandom('twister');
                if(0.2 < sym <= 0.4)        angle =  72;
                else if(0.4 < sym <= 0.6)   angle = 144;
                else if(0.6 < sym <= 0.8)   angle = 216;
                else if(0.8 < sym <= 1.0)   angle = 288;
            }
            pos *= maketransform(0, 0, 0, set(0, 0, angle), 1, pivot);
        }
    }
}

// precalc[0]->precalc_sina; precalc[1]->precalc_cosa; precalc[2]->precalc_sinz
void precalc_utils(int type; vector pos, precalc){
    if(type==9 || type==10 || type==11 || type==19 || type==21 || type==30 || type==35 ){
        precalc = pos / precalc("SQRT", pos);
    }
}

void affine(vector outp, pos; float a, b, d, e, f, h){
    outp +=  set( a*pos[0] + b*pos[1] + d,
                  e*pos[0] + f*pos[1] + h,
                 0 );
}

void affinePOST(vector pos; float a, b, d, e, f, h){
    pos = set( a*pos[0] + b*pos[1] + d,
               e*pos[0] + f*pos[1] + h,
               0 );
}
// VARIATIONS
//
// 01
void VAR_SINUSOIDAL(vector pos, _inp; float weight){
    pos[0] = weight * sin(_inp[0]);
    pos[1] = weight * sin(_inp[1]);
}
// 02
void VAR_SPHERICAL(vector pos, _inp; float weight){
    float r2 = weight / ( precalc("SUMSQ", _inp) + EPS );
    pos[0] = r2 * _inp[0];
    pos[1] = r2 * _inp[1];
}
// 03
void VAR_SWIRL(vector pos, _inp; float weight){
    float rr = precalc("SUMSQ", _inp);
    float c1, c2, nx, ny, nz;
    c1 = sin(rr);
    c2 = cos(rr);
    nx = c1 * _inp[0] - c2 * _inp[1];
    ny = c2 * _inp[0] + c1 * _inp[1];
    pos[0] = weight * nx;
    pos[1] = weight * ny;
}
// 04
void VAR_HORSESHOE(vector pos, _inp; float weight){
    float rr = weight / (precalc("SQRT", _inp) + EPS);
    pos[0] = (_inp[0] - _inp[1]) * (_inp[0] + _inp[1]) * rr;
    pos[1] = 2.0 * _inp[0] * _inp[1] * rr;
}
// 05
void VAR_POLAR(vector pos, _inp; float weight){
    float nx, ny;
    nx = precalc("ATAN", _inp) * M_1_PI;
    ny = precalc("SQRT", _inp) - 1.0;
    pos[0] = weight * nx;
    pos[1] = weight * ny;
}
// 06
void VAR_HANDKERCHIEF(vector pos, _inp; float weight){
    float aa = precalc("ATAN", _inp);
    pos[0] = weight * precalc("SQRT", _inp) * sin(aa+precalc("SQRT", _inp));
    pos[1] = weight * precalc("SQRT", _inp) * cos(aa-precalc("SQRT", _inp));
}
// 07
void VAR_HEART(vector pos, _inp; float weight){
    float aa, ca, sa, rr;
    aa = precalc("SQRT", _inp) * precalc("ATAN", _inp);
    sa = sin(aa);
    ca = cos(aa);
    rr = weight * precalc("SQRT", _inp) * sa;
    pos[0] = rr * sa;
    pos[1] = (-rr) * ca;
}
// 08
void VAR_DISC(vector pos, _inp; float weight){
    float aa, rr, sr, cr;
    aa = precalc("ATAN", _inp) * (1.0/M_PI);
    rr = M_PI * precalc("SQRT", _inp);
    sincos(rr, sr,cr);
    pos[0] = weight * sr * aa;
    pos[1] = weight * cr * aa;
}
// 09
void VAR_SPIRAL(vector pos, _inp, precalc; float weight){
    float r, r1, sr, cr;
    r = precalc("SQRT", _inp) + EPS;
    r1 = weight/r;
    sincos(r, sr, cr);
    pos[0] = r1 * (precalc[1] + sr);
    pos[1] = r1 * (precalc[0] - cr);
}
// 10
void VAR_HIPERBOLIC(vector pos, _inp, precalc; float weight){
    float rr = precalc("SQRT", _inp) + EPS;
    pos[0] = weight * precalc[0] / rr;
    pos[1] = weight * precalc[1] * rr;
}
// 11
void VAR_DIAMOND(vector pos, _inp, precalc; float weight){
    float rr, sr, cr;
    rr = precalc("SQRT", _inp);
    sincos(rr, sr, cr);
    pos[0] = weight * (precalc[0] * cr);
    pos[1] = weight * (precalc[1] * sr);
}
// 12
void VAR_EX(vector pos, _inp; float weight){
    float aa, rr, n0, n1, m0, m1;
    aa = precalc("ATAN", _inp);
    rr = precalc("SQRT", _inp);
    n0 = sin(aa+rr);
    n1 = cos(aa-rr);
    m0 = n0*n0*n0*rr;
    m1 = n1*n1*n1*rr;
    pos[0] = weight * (m0 + m1);
    pos[1] = weight * (m0 - m1);
}
// 13
void VAR_JULIA(vector pos, _inp; float weight){
    float rr, aa, sa, ca;
    aa = 0.5 * precalc("ATAN", _inp);
    if(nrandom('twister')<0.5)
        aa += M_PI;
    rr = weight * sqrt(precalc("SQRT", _inp));
    sincos(aa, sa, ca);
    pos[0] = rr * ca;
    pos[1] = rr * sa;
}
// 14
void VAR_BENT(vector pos, _inp; float weight){
    float nx, ny, nz;
    nx = _inp[0];
    ny = _inp[1];
    if(nx < 0.0) nx = nx * 2.0;
    if(ny < 0.0) ny = ny / 2.0;
    pos[0] = weight * nx;
    pos[1] = weight * ny;
}
// 15
void VAR_WAVES(vector pos, _inp; float weight, d, e, f, h){
    float dx2, dy2, dz2, nx, ny, nz;
    // precalc
    dx2 = 1.0/(f*f + EPS);
    dy2 = 1.0/(h*h + EPS);

    nx = _inp[0] + d * sin(_inp[1] * dx2);
    ny = _inp[1] + e * sin(_inp[0] * dy2);
    pos[0] = weight * nx;
    pos[1] = weight * ny;
}
// 16
void VAR_FISHEYE(vector pos, _inp; float weight){
    float rr = precalc("SQRT", _inp);
    rr = 2 * weight / (rr+1);
    pos[0] = rr * _inp[1];
    pos[1] = rr * _inp[0];
}
// 17
void VAR_POPCORN(vector pos, _inp; float weight, d, h){
    float dx, dy, nx, ny;
    dx = tan(3*_inp[1]);
    dy = tan(3*_inp[0]);
    nx = _inp[0] + d * sin(dx);
    ny = _inp[1] + h * sin(dy);
    pos[0] = weight * nx;
    pos[1] = weight * ny;
}
// 18
void VAR_EXPONENTIAL(vector pos, _inp; float weight){
    float dx, dy, sdy, cdy;
    dx = weight * exp(_inp[0]-1.0);
    dy = M_PI * _inp[1];
    sincos(dy, sdy, cdy);
    pos[0] = dx * cdy;
    pos[1] = dx * sdy;
}
// 19
void VAR_POWER(vector pos, _inp, precalc; float weight){
    float rr = weight * pow(precalc("SQRT", _inp), precalc[0]);
    pos[0] = rr * precalc[1];
    pos[1] = rr * precalc[0];
}
// 20
void VAR_COSINE(vector pos, _inp; float weight){
    float aa, sa, ca, nx, ny, nz;
    aa = _inp[0] * M_PI;
    sincos(aa, sa, ca);
    nx = ca * cosh(_inp[1]);
    ny = -sa * sinh(_inp[1]);
    pos[0] = weight * nx;
    pos[1] = weight * ny;
}
// 21
void VAR_RINGS(vector pos, _inp, precalc; float weight, d){
    float dx, rr;
    dx = d*d + EPS;
    rr = precalc("SQRT", _inp);
    rr = weight * (fmod(rr+dx, 2*dx) - dx + rr * (1 - dx));
    pos[0] = rr * precalc[1];
    pos[1] = rr * precalc[0];
}
// 22
void VAR_FAN(vector pos, _inp; float weight, d){
    float dx, dx2, dy, aa, rr, sa, ca;
    dx = M_PI * (d*d + EPS);
    dy = d;
    dx2 = 0.5 * dx;
    aa = precalc("ATAN", _inp);
    rr = weight * precalc("SQRT", _inp);
    aa += (fmod(aa+dy,dx) > dx2) ? -dx2 : dx2;
    sincos(aa, sa, ca);
    pos[0] = rr * ca;
    pos[1] = rr * sa;
}
// 23
void VAR_BUBBLE(vector pos, _inp; float weight){
    float rr = weight / (0.25 * precalc("SUMSQ", _inp) + 1);
    pos[0] = rr * _inp[0];
    pos[1] = rr * _inp[1];
}
// 24
void VAR_CYLINDER(vector pos, _inp; float weight){
    pos[0] = weight * sin(_inp[0]);
    pos[1] = weight * _inp[1];
}
// 25
void VAR_EYEFISH(vector pos, _inp; float weight){
    float rr =  (weight * 2.0) / (1.0 + precalc("SQRT", _inp));
    pos[0] =  rr*_inp[0];
    pos[1] =  rr*_inp[1];
}
// 26
void VAR_BLUR(vector pos; float weight){
    float tmpr, sinr, cosr, rr;
    tmpr = nrandom("twister") * 2 * M_PI;
    sincos(tmpr, sinr, cosr);
    rr = weight * nrandom("twister");
    pos[0] = rr * cosr;
    pos[1] = rr * sinr;
}
// 27 ( parametric )
void VAR_CURL(vector pos, _inp; float weight, c1, c2){
    float re, im, rr;
    if(c1==0){
        if(c2==0){
            pos[0] = weight * _inp[0];
            pos[1] = weight * _inp[1];
        }
        else{
            re = 1.0 + c2*(sqrt(_inp[0]) - sqrt(_inp[1]));
            im = c2*2.0*_inp[0]*_inp[1];
            rr = weight / (re*re + im*im);
            pos[0] = (_inp[0] * re + _inp[1] * im) * rr;
            pos[1] = (_inp[1] * re - _inp[0] * im) * rr;
        }
    }
    else{
        if(c2==0){
            re = 1.0 + c1*_inp[0];
            im = c1*_inp[1];
            rr = weight / (re*re + im*im);
            pos[0] = (_inp[0] * re + _inp[1] * im) * rr;
            pos[1] = (_inp[1] * re - _inp[0] * im) * rr;
        }
        else{
            re = 1.0 + c1*_inp[0] + c2*(sqrt(_inp[0]) - sqrt(_inp[1]));
            im = c1*_inp[1] + c2*2.0*_inp[0]*_inp[1];
            rr = weight / (re*re + im*im);
            pos[0] = (_inp[0]*re + _inp[1]*im)*rr;
            pos[1] = (_inp[1]*re - _inp[0]*im)*rr;
        }
    }
}
// 28 ( parametric )
void VAR_NGON(vector pos, _inp; float weight, pow, sides, corners, circle){
    float cpower, csides, csidesinv, r_factor, theta, phi, amp;
    cpower = -0.5*pow; csides = 2.0*PI/sides; csidesinv = 1.0/csides;
    if(_inp[0]==0 && _inp[1]==0) r_factor = 0;
    else r_factor = pow(precalc("SUMSQ", _inp), cpower);
    theta = precalc("ATANYX", _inp);
    phi = theta - csides * floor(theta*csidesinv);
    if(phi>0.5*csides) phi -= csides;
    amp = (corners * (1.0/cos(phi) - 1.0) + circle) * weight * r_factor;
    pos[0] = amp * _inp[0];
    pos[1] = amp * _inp[1];
}
// 29 ( parametric )
void VAR_PDJ(vector pos, _inp; float weight; vector4 pp){
    float  nx1, nx2, ny1, ny2, nz1;
    nx1 = cos(pp[1] * _inp[0]);
    nx2 = sin(pp[2] * _inp[0]);
    ny1 = sin(pp[0] * _inp[1]);
    ny2 = cos(pp[3] * _inp[1]);
    pos[0] = weight * (ny1 - nx1);
    pos[1] = weight * (nx2 - ny2);
}
// 30 ( parametric )
void VAR_BLOB(vector pos, _inp, precalc; float weight, pp1, pp2, pp3){
    float  blob_coeff, rr, aa, bdiff;
    float SQRT = precalc("SQRT", _inp);
    rr = SQRT;
    aa = precalc("ATAN", _inp);
    bdiff = pp1 - pp2;
    rr = rr * (pp2 + bdiff * (0.5 + 0.5 * sin(pp3 * aa)));
    pos[0] = weight * precalc[0] * rr;
    pos[1] = weight * precalc[1] * rr;
}
// 31 ( parametric )
void VAR_JULIAN(vector pos, _inp; float weight, power, jdist){
    int t_rnd;
    float julian_rN, julian_cn, tmpr, rr, sina, cosa;
    julian_rN = power;
    julian_cn = jdist / power / 2.0;
    t_rnd = (int)trunc(julian_rN * nrandom('twister'));
    tmpr = ( precalc("ATANYX", _inp) + 2 * M_PI * t_rnd ) / power;
    rr = weight * pow( precalc("SUMSQ", _inp), julian_cn );
    sincos(tmpr, sina, cosa);
    pos[0] = rr * cosa;
    pos[1] = rr * sina;
}
// 32 ( parametric )
void VAR_JULIASCOPE(vector pos, _inp; float weight, power, jdist){
    int t_rnd;
    float julian_rN, julian_cn, tmpr, rr, sina, cosa;
    julian_rN = power;
    julian_cn = jdist / power / 2.0;
    t_rnd = (int)trunc(julian_rN * nrandom('twister'));
    if((t_rnd & 1) == 0) tmpr = (2.0 * M_PI * t_rnd + precalc("ATANYX", _inp)) / power;
    else tmpr = (2.0 * M_PI * t_rnd - precalc("ATANYX", _inp)) / power;
    sincos(tmpr, sina, cosa);
    rr = weight * pow( precalc("SUMSQ", _inp), julian_cn );
    pos[0] = rr * cosa;
    pos[1] = rr * sina;
}
// 33
void VAR_GAUSSIAN(vector pos; float weight){
    float ang, rr, sina, cosa;
    ang = nrandom('twister') * 2.0 * M_PI;
    rr = weight * (nrandom('twister')+nrandom('twister')+nrandom('twister')+nrandom('twister') - 2.0);
    pos[0] = rr * cos(ang);
    pos[1] = rr * sin(ang);
}
// 34 ( parametric )
void VAR_FAN2(vector pos, _inp; float weight; vector2 fan2){
    float dx, dx2, dy, aa, sa,ca,rr, tt;
    dy = fan2[1];
    dx = M_PI * (fan2[0]*fan2[0] + EPS);
    dx2 = 0.5*dx;
    aa = precalc("ATAN", _inp);
    rr = weight * precalc("SQRT", _inp);
    tt = aa + dy - dx * (int)((aa + dy)/dx);
    if(tt>dx2) aa = aa-dx2;
    else aa = aa+dx2;
    sincos(aa, sa, ca);
    pos[0] = rr * sa;
    pos[1] = rr * ca;
}
// 35 ( parametric )
void VAR_RINGS2(vector pos, _inp, precalc; float weight, rings2val){
    float rr, dx;
    int nrand;
    rr = precalc("SQRT", _inp);
    dx = rings2val*rings2val;
    rr += -2.0*dx*(int)((rr+dx)/(2.0*dx)) + rr * (1.0-dx);
    pos[0] = weight * precalc[0] * rr;
    pos[1] = weight * precalc[1] * rr;
}
// 36 ( parametric )
void VAR_RECTANGLES(vector pos, _inp; float weight; vector2 rect){
    if(rect[0]==0) pos[0] = weight * _inp[0];
    else pos[0] = weight * ((2 * floor(_inp[0] / rect[0]) + 1) * rect[0] - _inp[0]);
    if(rect[1]==0) pos[1] = weight * _inp[1];
    else pos[1] = weight * ((2 * floor(_inp[1] / rect[1]) + 1) * rect[1] - _inp[1]);
}
// 37 ( parametric )
void VAR_RADIALBLUR(vector pos, _inp; float weight, spin, zoom){
    float rndG, tmpa, ra, rz, sa, ca;
    rndG = weight * (nrandom('twister')+nrandom('twister')+nrandom('twister')+nrandom('twister') - 2.0);
    ra = precalc("SQRT", _inp);
    tmpa = precalc("ATANYX", _inp) + spin*rndG;
    sincos(tmpa, sa, ca);
    rz = zoom * rndG - 1;
    pos[0] = ra * ca + rz * _inp[0];
    pos[1] = ra * sa + rz * _inp[1];
}
// 38 ( parametric )
void VAR_PIE(vector pos; float weight, slices, thickness, rotation){
    float aa, rr, sa, ca, sl;
    sl = (int)(nrandom('twister')*slices);
    aa = rotation + 2.0 * M_PI * (sl + nrandom("twister") * thickness) / slices;
    rr = weight * nrandom('twister');
    sincos(aa, sa, ca);
    pos[0] = rr * ca;
    pos[1] = rr * sa;
}
// 39
void VAR_ARCH(vector pos, _inp; float weight){
    float ang, sinr, cosr;
    ang = nrandom("twister") * weight * M_PI;
    sincos(ang, sinr, cosr);
    pos[0] = _inp[0] + (weight * sinr);
    pos[1] = _inp[1] + (weight * (sinr*sinr)/cosr);
}
// 40
void VAR_TANGENT(vector pos, _inp; float weight){
    pos[0] = weight * (sin(_inp[0])/cos(_inp[1]));
    pos[1] = weight * tan(_inp[1]);
}
// 41
void VAR_SQUARE(vector pos, _inp; float weight){
    pos[0] = weight * (nrandom("twister") - 0.5);
    pos[0] = weight * (nrandom("twister") - 0.5);
}
// 42
void VAR_RAYS(vector pos, _inp; float weight){
    float ang, rr, tanrr;
    ang = weight * nrandom("twister") * M_PI;
    rr = weight / (precalc("SUMSQ", _inp) + EPS);
    tanrr = weight * tan(ang) * rr;
    pos[0] = tanrr * cos(_inp[0]);
    pos[1] = tanrr * sin(_inp[1]);
}
// 43
void VAR_BLADE(vector pos, _inp; float weight){
    float rr, sinr, cosr;
    rr = nrandom("twister") * weight * precalc("SQRT", _inp);
    sincos(rr, sinr, cosr);
    pos[0] = weight * _inp[0] * (cosr + sinr);
    pos[1] = weight * _inp[0] * (cosr - sinr);
}
// 44
void VAR_SECANT2(vector pos, _inp; float weight){
    float rr, cr, sr, icr, isr;
    rr = weight * precalc("SQRT", _inp);
    cr = cos(rr);
    sr = sin(rr);
    icr = 1.0/cr;
    pos[0] = weight * _inp[0];
    if(cr<0) pos[1] = weight * (icr+1);
    else pos[1] = weight * (icr-1);
}
// 45
void VAR_TWINTRIAN(vector pos, _inp; float weight){
    float rr, sinr, cosr, diff;
    rr = nrandom("twister") * weight * precalc("SQRT", _inp);
    sincos(rr, sinr, cosr);
    diff = log10(sinr*sinr)+cosr;
    if(!isfinite(diff) || isnan(diff))
        diff = -30.0;
    pos[0] = weight * _inp[0] * diff;
    pos[1] = weight * _inp[0] * (diff - sinr*M_PI);
}
// 46
void VAR_CROSS(vector pos, _inp; float weight){
    float ss, rr;
    ss = _inp[0]*_inp[0] - _inp[1]*_inp[1];
    rr = weight * sqrt(1.0 / (ss*ss+EPS));
    pos[0] = _inp[0]*rr;
    pos[1] = _inp[1]*rr;
}
// 47 ( parametric )
void VAR_DISC2(vector pos, _inp; float weight, rot, twist){
    float rr, tt, sinr, cosr, disc2_sinadd, disc2_cosadd, disc2_timespi;
    // precalc
    float k;
    disc2_timespi = rot * M_PI;
    sincos(twist, disc2_sinadd, disc2_cosadd);
    disc2_cosadd -= 1;
    if(twist > ( 2*M_PI)){ k = (1 + twist - 2*M_PI); disc2_cosadd*=k; disc2_sinadd*=k; }
    if(twist < (-2*M_PI)){ k = (1 + twist + 2*M_PI); disc2_cosadd*=k; disc2_sinadd*=k; }

    tt = disc2_timespi * (_inp[0] + _inp[1]);
    sincos(tt, sinr, cosr);
    rr = weight * precalc("ATAN", _inp) / M_PI;
    pos[0] = (sinr + disc2_cosadd) * rr;
    pos[1] = (cosr + disc2_sinadd) * rr;
}
// 48 ( parametric )
void VAR_SUPERSHAPE(vector pos, _inp; float weight, ss_rnd, ss_m, ss_holes; vector ss_n){
    float theta, st, ct, tt1, tt2, rr, ss_pm_4, ss_pneg1_n1;
    // precalc
    ss_pm_4 = ss_m / 4.0;
    ss_pneg1_n1 = -1.0 / ss_n[0];

    theta = ss_pm_4 * precalc("ATANYX", _inp) + M_PI_4;
    sincos(theta, st, ct);
    tt1 = abs(ct);  tt1 = pow(tt1, ss_n[1]);
    tt2 = abs(st);  tt2 = pow(tt2, ss_n[2]);
    float SQRT = precalc("SQRT", _inp);
    rr = weight * ((ss_rnd*nrandom('twister') + (1.0-ss_rnd)*SQRT) - ss_holes) * pow(tt1+tt2, ss_pneg1_n1) / SQRT;
    pos[0] = rr * _inp[0];
    pos[1] = rr * _inp[1];
}
// 49 ( parametric )
void VAR_FLOWER(vector pos, _inp; float weight, petals, holes){
    float theta, rr;
    theta = precalc("ATANYX", _inp);
    rr = weight * (nrandom("twister") - holes) * cos(petals*theta) / precalc("SQRT", _inp);
    pos[0] = rr * _inp[0];
    pos[1] = rr * _inp[1];
}
// 50
void VAR_CONIC(vector pos, _inp; float weight, eccentricity, holes){
    float ct, rr;
    float SQRT = precalc("SQRT", _inp);
    ct = _inp[0] / SQRT;
    rr = weight * (nrandom("twister") - holes) 
                * eccentricity / (1 + eccentricity*ct) / SQRT;
    pos[0] = rr * _inp[0];
    pos[1] = rr * _inp[1];
}
// 51 ( parametric )
void VAR_PARABOLA(vector pos, _inp; float weight, height, width){
    float rr, sr, cr;
    rr = precalc("SQRT", _inp);
    sincos(rr, sr, cr);
    pos[0] = height * weight * sr*sr * nrandom("twister");
    pos[1] = width  * weight * cr * nrandom("twister");
}
// 52 ( parametric )
void VAR_BENT2(vector pos, _inp; float weight; vector2 bent2){
    float nx, ny, nz;
    nx = _inp[0]; ny = _inp[1];
    if(nx < 0.0)
        nx = nx * bent2[0];
    if(ny < 0.0)
        ny = ny * bent2[1];
    pos[0] = weight * nx;
    pos[1] = weight * ny;
}
// 53 ( parametric )
void VAR_BIPOLAR(vector pos, _inp; float weight, shift){
    float x2y2, tt, x2, ps, y;
    x2y2 = precalc("SUMSQ", _inp);
    tt = x2y2+1;
    x2 = 2*_inp[0];
    ps = -M_PI_2 * shift;
    y = 0.5 * atan2(2.0 * _inp[1], x2y2 - 1.0) + ps;
    if(y > M_PI_2) y = -M_PI_2 + fmod(y + M_PI_2, M_PI);
    else if (y < -M_PI_2) y = M_PI_2 - fmod(M_PI_2 - y, M_PI);
    pos[0] = weight * 0.25 * M_2_PI * log((tt+x2) / (tt-x2));
    pos[1] = weight * M_2_PI * y;
}
// 54
void VAR_BOARDERS(vector pos, _inp; float weight){
    float roundX, roundY, roundZ, offsetX, offsetY, offsetZ;
    roundX = rint(_inp[0]);
    roundY = rint(_inp[1]);
    offsetX = _inp[0] - roundX;
    offsetY = _inp[1] - roundY;
    if(nrandom("twister")>=0.75){
        pos[0] = (offsetX*0.5 + roundX);
        pos[1] = (offsetY*0.5 + roundY);
    }
    else{
        if (abs(offsetX) >= abs(offsetY)) {
            if (offsetX >= 0.0){
                pos[0] = weight*(offsetX*0.5 + roundX + 0.25);
                pos[1] = weight*(offsetY*0.5 + roundY + 0.25 * offsetY / offsetX);
            } 
            else{
                pos[0] = weight*(offsetX*0.5 + roundX - 0.25);
                pos[1] = weight*(offsetY*0.5 + roundY - 0.25 * offsetY / offsetX); 
            }
        }
            else{
                if (offsetY >= 0.0){
                    pos[1] = weight*(offsetY*0.5 + roundY + 0.25);
                    pos[0] = weight*(offsetX*0.5 + roundX + offsetX/offsetY*0.25);
                } 
                else{
                    pos[1] = weight*(offsetY*0.5 + roundY - 0.25);
                    pos[0] = weight*(offsetX*0.5 + roundX - offsetX/offsetY*0.25);
                }
            }
    }
}
// 55
void VAR_BUTTERFLY(vector pos, _inp; float weight){
    float wx, y2, rr, rrz;
    wx = weight*1.3029400317411197908970256609023;
    y2 = _inp[1]*2.0;
    rr = wx*sqrt(abs(_inp[1]*_inp[0])/(EPS + _inp[0]*_inp[0] + y2*y2));
    pos[0] = rr * _inp[0];
    pos[1] = rr * y2;
}
// 56 ( parametric )
void VAR_CELL(vector pos, _inp; float weight, size){
    float inv_cell_size, x, y, z, dx, dy, dz;
    inv_cell_size = 1.0/size;
    x = floor(_inp[0]*inv_cell_size);
    y = floor(_inp[1]*inv_cell_size);
    dx = _inp[0] - x*size;
    dy = _inp[1] - y*size;
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
    pos[0] = (dx + x*size);
    pos[1] = -(dy + y*size);
}
// 57 ( parametric )
void VAR_CPOW(vector pos, _inp; float weight, power, pow_r, pow_i){
    float aa, lnr, va, vc, vd, ang, sa, ca, mm;
    aa = precalc("ATANYX", _inp);
    lnr = 0.5 * log(precalc("SUMSQ", _inp));
    va = 2.0 * M_PI / power;
    vc = pow_r / power;
    vd = pow_i / power;
    ang = vc*aa + vd*lnr + va*floor(power * nrandom("twister"));
    mm = weight * exp(vc * lnr - vd * aa);
    sincos(ang, sa, ca);
    pos[0] = mm * ca;
    pos[1] = mm * sa;
}
// 58
void VAR_EDISC(vector pos, _inp; float weight){
    float tmp, tmp2, rr1, rr2, xmax, aa1, aa2, ww, snv, csv, snhu, cshu;
    tmp = precalc("SUMSQ", _inp);
    tmp2 = 2.0 * _inp[0];
    rr1 = sqrt(tmp+tmp2);
    rr2 = sqrt(tmp-tmp2);
    xmax = (rr1+rr2) * 0.5;
    aa1 = log(xmax + (sqrt(xmax - 1.0)));
    aa2 = -acos(_inp[0]/xmax);
    ww = weight / 11.57034632;;
    sincos(aa1, snv, csv);
    snhu = sinh(aa2);
    cshu = cosh(aa2);
    if(_inp[1] > 0.0) snv = -snv;
    pos[0] = ww * cshu * csv;
    pos[1] = ww * snhu * snv;
}
// 59
void VAR_ELLIPTIC(vector pos, _inp; float weight){
    float tmp, x2, xmax, aa, bb, ssx, ww;
    tmp = precalc("SUMSQ", _inp) + 1.0;
    x2 = 2.0 * _inp[0];
    xmax = 0.5 * (sqrt(tmp+x2) + sqrt(tmp-x2));
    aa = _inp[0] / xmax;
    bb = 1.0 - aa*aa;
    ssx = xmax - 1.0;
    ww = weight / M_PI_2;
    if(bb<0) bb = 0;
    else bb = sqrt(bb);
    if(ssx<0) ssx = 0;
    else ssx = sqrt(ssx);
    pos[0] = ww * atan2(aa,bb);
    if(_inp[1] > 0) pos[1] = ww * log(xmax + ssx);
    else pos[1] = ww * -log(xmax + ssx);
}

// 60
void VAR_NOISE(vector pos, _inp; float weight){
    float tmpr, sinr, cosr, rr;
    tmpr = nrandom("twister") * 2 * M_PI;
    sincos(tmpr, sinr, cosr);
    rr = weight * nrandom("twister");
    pos[0] = _inp[0] * rr * cosr;
    pos[1] = _inp[1] * rr * sinr;
}
// 61 ( parametric )
void VAR_ESCHER(vector pos, _inp; float weight, beta){
    float aa, lnr, seb, ceb, vc, vd, mm, nn, sn, cn;
    aa = precalc("ATANYX", _inp);
    lnr = 0.5 * log(precalc("SUMSQ", _inp));
    sincos(beta, seb, ceb);
    vc = 0.5 * (1.0 + ceb);
    vd = 0.5 * seb;
    mm = weight * exp(vc*lnr - vd*aa);
    nn = vc*aa + vd*lnr;
    sincos(nn, sn, cn);
    pos[0] = mm * cn;
    pos[1] = mm * sn;
}
// 62
void VAR_FOCI(vector pos, _inp; float weight){
    float expx, expnx, expz, expnz, snz, cnz, sn, cn, tmp, tmpz;
    expx = exp(_inp[0]) * 0.5;
    expnx = 0.25 / expx;
    sincos(_inp[1], sn, cn);
    tmp = weight/(expx + expnx - cn);
    pos[0] = tmp * (expx - expnx);
    pos[1] = tmp * sn;
}
// 63 ( parametric )
void VAR_LAZYSUSAN(vector pos, _inp; float weight, spin, twist, space; vector2 lazy){
    float xx, yy, rr, sina, cosa, aa;
    xx = _inp[0] - lazy[0];
    yy = _inp[1] - lazy[1];
    rr = precalc("SQRT", set(xx,yy,0));
    if(rr<weight){
        aa = precalc("ATANYX", set(xx,yy,0)) + spin + twist * (weight - rr);
        sincos(aa, sina, cosa);
        rr = weight * rr;
        pos[0] = rr*cosa + lazy[0];
        pos[1] = rr*sina + lazy[1];
    }
    else{
        rr = weight * (1.0 + space / rr);
        pos[0] = rr*xx + lazy[0];
        pos[1] = rr*yy + lazy[1];
    }
}
// 64
void VAR_LOONIE(vector pos, _inp; float weight){
    float rr, rr2, w2;
    rr2 = precalc("SUMSQ", _inp);
    w2 = weight * weight;
    if(rr2 < w2){
        rr = weight * sqrt(w2/rr2 - 1.0);
        pos[0] = rr * _inp[0];
        pos[1] = rr * _inp[1];
    }
    else{
        pos[0] = weight * _inp[0];
        pos[1] = weight * _inp[1];
    }
}
// 65
void VAR_PREBLUR(vector pos; float weight){
    float rndG, rndA, sinA, cosA;
    rndG = weight * (nrandom("twister") + nrandom("twister") + nrandom("twister") + nrandom("twister") - 2.0);
    rndA = nrandom("twister") * 2.0 * M_PI;
    sincos(rndA, sinA, cosA);
    pos[0] += rndG * cosA;
    pos[1] += rndG * sinA;
}
// 66 ( parametric )
void VAR_MODULUS(vector pos, _inp; float weight; vector2 m){
    float xr, yr, zr;
    xr = 2*m[0]; yr = 2*m[1];
    if(_inp[0] > m[0])
        pos[0] = weight * (m[0] + fmod(_inp[0] + m[0], xr));
    else if(pos[0] < m[0]) pos[0] = weight * (m[0] - fmod(m[0] + _inp[0], xr));
    else pos[0] = weight * _inp[0];
    if(_inp[1] > m[1]) pos[1] = weight * (m[1] + fmod(_inp[1] + m[1], yr));
    else if(pos[0] < m[0]) pos[1] = weight * (m[1] - fmod(m[1] + _inp[1], yr));
    else pos[1] = weight * _inp[1];
}
// 67 ( parametric )
void VAR_OSCOPE(vector pos, _inp; float weight, freq, amp, damp, sep){
    float tpf, tt;
    tpf = 2 * M_PI * freq;
    if(damp == 0.0) tt = amp * cos(tpf*_inp[0]) + sep;
    else tt = amp * exp(-abs(_inp[0])* damp) * cos(tpf*_inp[0]) + sep;
    if(abs(_inp[1]) <= tt){
        pos[0] = weight * _inp[0];
        pos[1] = weight * -_inp[1];
    }
    else{
        pos[0] = weight * _inp[0];
        pos[1] = weight * _inp[1];
    }
}
// 68
void VAR_POLAR2(vector pos, _inp; float weight){
    float p2v = weight / M_PI;
    pos[0] = p2v * precalc("ATAN", _inp);
    pos[1] = p2v/2.0 * log(precalc("SUMSQ", _inp));
    }
// 69 ( parametric )
void VAR_POPCORN2(vector pos, _inp; float weight, pop2c; vector2 pop2){
    pos[0] = weight * (_inp[0] + pop2[0] * sin(tan(_inp[1]*pop2c)));
    pos[1] = weight * (_inp[1] + pop2[1] * sin(tan(_inp[0]*pop2c)));
    }
// 70 ( parametric )
void VAR_SCRY(vector pos, _inp; float weight){
    float tt, rr;
    tt = precalc("SUMSQ", _inp);
    rr = 1.0 / (precalc("SQRT", _inp) * (tt + 1.0/(weight+EPS)));
    pos[0] = _inp[0] * rr;
    pos[1] = _inp[1] * rr;
}
// 71 ( parametric )
void VAR_SEPARATION(vector pos, _inp; float weight; vector2 sep, ins){
    float sx2, sy2, sz2;
    sx2 = sep[0]*sep[0];
    sy2 = sep[1]*sep[1];
    if(_inp[0] > 0.0) pos[0] = weight * (sqrt(_inp[0]*_inp[0] + sx2) - _inp[0]*ins[0]);
    else pos[0] = weight * -(sqrt(_inp[0]*_inp[0] + sx2) + _inp[0]*ins[0]);
    if(_inp[1] > 0.0) pos[1] = weight * (sqrt(_inp[1]*_inp[1] + sy2) - _inp[1]*ins[1]);
    else pos[1] = weight * -(sqrt(_inp[1]*_inp[1] + sy2) + _inp[1]*ins[1]);
}
// 72 ( parametric )
void VAR_SPLIT(vector pos, _inp; float weight; vector2 split){
    if(cos(_inp[0]*split[0]*M_PI) >= 0) pos[1] = weight * _inp[1];
    else pos[1] = weight * -_inp[1];
    if(cos(_inp[1]*split[1]*M_PI) >= 0) pos[0] = weight * _inp[0];
    else pos[0] = weight * -_inp[0];
}
// 73 ( parametric )
void VAR_SPLITS(vector pos, _inp; float weight; vector2 splits){
    if(_inp[0] >= 0) pos[0] = weight * (_inp[0] + splits[0]);
    else pos[0] = weight * (_inp[0] - splits[0]);
    if(_inp[1] >= 0) pos[1] = weight * (_inp[1] + splits[1]);
    else pos[1] = weight * (_inp[1] - splits[1]);
}
// 74 ( parametric )
void VAR_STRIPES(vector pos, _inp; float weight, space, warp){
    float roundx, offsetx;
    roundx = floor(_inp[0] + 0.5);
    offsetx = _inp[0] - roundx;
    pos[0] = weight * (offsetx * (1.0 - space) + roundx);
    pos[1] = weight * (_inp[1] + offsetx*offsetx*warp);
}
// 75 ( parametric )
void VAR_WEDGE(vector pos, _inp; float weight, swirl, angle, hole, count){
    float rr, aa, cc, comp_fac, sa, ca;
    rr = precalc("SQRT", _inp);
    aa = precalc("ATANYX", _inp) + swirl * rr;
    cc = floor( (count * aa + M_PI) * M_1_PI*0.5 );
    comp_fac = 1 - angle*count*M_1_PI*0.5;
    aa = aa * comp_fac + cc * angle;
    sincos(aa, sa, ca);
    rr = weight * (rr + hole);
    pos[0] = rr*ca;
    pos[1] = rr*sa;
}
// 76 ( parametric )
void VAR_WEDGEJULIA(vector pos, _inp; float weight, power, angle, dist, count){
    float wedgeJulia_cf, wedgeJulia_rN, wedgeJulia_cn, rr, t_rnd, aa, cc, sa, ca;
    // precalc
    wedgeJulia_cf = 1.0 - angle * count * M_1_PI * 0.5;
    wedgeJulia_rN = abs(power);
    wedgeJulia_cn = dist / power / 2.0;

    rr = weight * pow(precalc("SUMSQ", _inp), wedgeJulia_cn);
    t_rnd = (int)((wedgeJulia_rN)*nrandom("twister"));
    aa = (precalc("ATANYX", _inp) + 2 * M_PI * t_rnd) / power;
    cc = floor( (count * aa + M_PI)*M_1_PI*0.5 );
    aa = aa * wedgeJulia_cf + cc * angle;
    sincos(aa, sa, ca);
    pos[0] = rr * ca;
    pos[1] = rr * sa;
}
// 77 ( parametric )
void VAR_WEDGESPH(vector pos, _inp; float weight, swirl, angle, hole, count){
    float rr, aa, cc, comp_fac, sa, ca;
    rr = 1.0/(precalc("SQRT", _inp) + EPS);
    aa = precalc("ATANYX", _inp) + swirl * rr;
    cc = floor( (count * aa + M_PI)*M_1_PI*0.5 );
    comp_fac = 1 - angle*count*M_1_PI*0.5;
    aa = aa * comp_fac + cc * angle;
    sincos(aa, sa, ca);
    rr = weight * (rr + hole);
    pos[0] = rr * ca;
    pos[1] = rr * sa;
}
// 78 ( parametric )
void VAR_WHORL(vector pos, _inp; float weight, inside, outside){
    float rr, rrz, aa, aaz, sa, ca, saz, caz;
    rr = precalc("SQRT", _inp);
    if(rr<weight) aa = precalc("ATANYX", _inp) + inside/(weight-rr);
    else aa = precalc("ATANYX", _inp) + outside/(weight-rr);
    sincos(aa, sa, ca);
    pos[0] = weight*rr*ca;
    pos[1] = weight*rr*sa;
}
// 79 ( parametric )
void VAR_WAVES2(vector pos, _inp; float weight; vector2 scl, freq){
    pos[0] = weight*(_inp[0] + scl[0]*sin(_inp[1]*freq[0]));
    pos[1] = weight*(_inp[1] + scl[1]*sin(_inp[0]*freq[1]));
}
// 80
void VAR_COTHEEXP(vector pos, _inp; float weight){
    float expe, expz, expsin, expcos;
    expe = exp(_inp[0]);
    sincos(pos[1], expsin, expcos);
    pos[0] = weight * expe * expcos;
    pos[1] = weight * expe * expsin;
}
// 81
void VAR_COTHELOG(vector pos, _inp; float weight){
    pos[0] = weight * 0.5 * log(precalc("SUMSQ", _inp));
    pos[1] = weight * precalc("ATANYX", _inp);
}
// 82
void VAR_COTHESIN(vector pos, _inp; float weight){
    float sinsin, sinacos, sinsinh, sincosh;
    sincos(_inp[0], sinsin, sinacos);
    sinsinh = sinh(_inp[1]);
    sincosh = cosh(_inp[1]);
    pos[0] = weight * sinsin * sincosh;
    pos[1] = weight * sinacos * sinsinh;
}
// 83
void VAR_COTHECOS(vector pos, _inp; float weight){
    float cossin, coscos, cossinh, coscosh;
    sincos(_inp[0], cossin, coscos);
    cossinh = sinh(_inp[1]);
    coscosh = cosh(_inp[1]);
    pos[0] = weight * coscos * coscosh;
    pos[1] = weight * cossin * cossinh;
}
// 84
void VAR_COTHETAN(vector pos, _inp; float weight){
    float tansin, tancos, tansinz, tancosz, tansinh, tancosh, tanden;
    sincos(2*_inp[0], tansin, tancos);
    tansinh = sinh(2.0*_inp[1]);
    tancosh = cosh(2.0*_inp[1]);
    tanden = 1.0/(tancos + tancosh);
    pos[0] = weight * tanden * tansinh;
    pos[1] = weight * tanden * tancosh;
}
// 85
void VAR_COTHESEC(vector pos, _inp; float weight){
    float secsin, seccos, secsinh, seccosh, secden;
    sincos(_inp[0], secsin, seccos);
    secsinh = sinh(_inp[1]);
    seccosh = cosh(_inp[1]);
    secden = 2.0/(cos(2.0*_inp[0]) + cosh(2.0*_inp[1]));
    pos[0] = weight * secden * seccos * seccosh;
    pos[1] = weight * secden * secsin * secsinh;
}
// 86
void VAR_COTHECSC(vector pos, _inp; float weight){
    float cscsin, csccos, cscsinz, csccosz, cscsinh, csccosh, cscden, cscdenz;
    sincos(pos[0], cscsin, csccos);
    cscsinh = sinh(_inp[1]);
    csccosh = cosh(_inp[1]);
    cscden = 2.0/(cosh(2.0*_inp[1]) - cos(2.0*_inp[0]));
    pos[0] = weight * cscden * cscsin * csccosh;
    pos[1] = weight * cscden * csccos * cscsinh;
}
// 87
void VAR_COTHECOT(vector pos, _inp; float weight){
    float cotsin, cotcos, cotsinz, cotcosz, cotsinh, cotcosh, cotden, cotdenz;
    sincos(2.0*_inp[0], cotsin, cotcos);
    cotsinh = sinh(2.0*_inp[1]);
    cotcosh = cosh(2.0*_inp[1]);
    cotden = 1.0/(cotcosh - cotcos);
    pos[0] = weight * cotden * cotsin;
    pos[1] = weight * cotden * -1 * cotsinh;
}
// 88
void VAR_COTHESINH(vector pos, _inp; float weight){
    float sinhsin, sinhcos, sinhsinh, sinhcosh;
    sincos(_inp[1], sinhsin, sinhcos);
    sinhsinh = sinh(_inp[0]);
    sinhcosh = cosh(_inp[0]);
    pos[0] = weight * sinhsinh * sinhcos;
    pos[1] = weight * sinhcosh * sinhsin;
}
// 89
void VAR_COTHECOSH(vector pos, _inp; float weight){
    float coshsin, coshcos, coshsinh, coshcosh;
    sincos(_inp[1], coshsin, coshcos);
    coshsinh = sinh(_inp[0]);
    coshcosh = cosh(_inp[0]);
    pos[0] = weight * coshcosh * coshcos;
    pos[1] = weight * coshsinh * coshsin;
}
// 90
void VAR_COTHETANH(vector pos, _inp; float weight){
    float tanhsin, tanhcos, tanhsinh, tanhcosh, tanhden, tanhdenz;
    sincos(2.0*_inp[1], tanhsin, tanhcos);
    tanhsinh = sinh(_inp[0]);
    tanhcosh = cosh(_inp[0]);
    tanhden = 1.0/(tanhcos + tanhcosh);
    pos[0] = weight * tanhden * tanhsinh;
    pos[1] = weight * tanhden * tanhsin;
}
// 91
void VAR_COTHESECH(vector pos, _inp; float weight){
    float sechsin, sechcos, sechsinh, sechcosh, sechden, sechdenz;
    sincos(_inp[1], sechsin, sechcos);
    sechsinh = sinh(_inp[0]);
    sechcosh = cosh(_inp[0]);
    sechden = 2.0/(cos(2.0*_inp[1]) + cosh(2.0*_inp[0]));
    pos[0] = weight * sechden * sechcos * sechcosh;
    pos[1] = weight * sechden * sechsin * sechsinh;
}
// 92
void VAR_COTHECSCH(vector pos, _inp; float weight){
    float cschsin, cschcos, cschsinh, cschcosh, cschden, cschdenz;
    sincos(_inp[1], cschsin, cschcos);
    cschsinh = sinh(_inp[0]);
    cschcosh = cosh(_inp[0]);
    cschden = 2.0/(cosh(2.0*_inp[0]) - cos(2.0*_inp[1]));
    pos[0] = weight * cschden * cschsinh * cschcos;
    pos[1] = weight * cschden * cschcosh * cschsin;
}
// 93
void VAR_COTHECOTH(vector pos, _inp; float weight){
    float cothsin, cothcos, cothsinh, cothcosh, cothden, cothdenz;
    sincos(2.0*_inp[1], cothsin, cothcos);
    cothsinh = sinh(2.0*_inp[0]);
    cothcosh = cosh(2.0*_inp[0]);
    cothden = 1.0/(cothcosh - cothcos);
    pos[0] = weight * cothden * cothsinh;
    pos[1] = weight * cothden * cothsin;
}
// 94 ( parametric )
void VAR_AUGER(vector pos, _inp; float weight, freq, scale, sym, ww){
    float  ss, tt, uu, dy, dx, dz;
    ss = sin(freq * _inp[0]);
    tt = sin(freq * _inp[1]);
    dx = _inp[1] + ww*(scale*ss/2.0 + abs(_inp[1])*ss);
    dy = _inp[0] + ww*(scale*tt/2.0 + abs(_inp[0])*tt);
    pos[0] = weight * (_inp[0] + sym*(dx*_inp[0]));
    pos[1] = weight * dy;
}
// 95 ( parametric )
void VAR_FLUX(vector pos, _inp; float weight, spread){
    float xpw, xmw, avgr, avga;
    xpw = _inp[0] + weight;
    xmw = _inp[0] - weight;
    avgr = weight * (2 + spread) * sqrt(sqrt(_inp[1]*_inp[1]+xpw*xpw) / sqrt(_inp[1]*_inp[1] + xmw*xmw));
    avga = ( atan2(_inp[1], xmw) - atan2(_inp[1], xpw)) * 0.5;
    pos[0] = avgr * cos(avga);
    pos[1] = avgr * sin(avga);
}
// 96 ( parametric )
void VAR_MOBIUS(vector pos, _inp; float weight; vector4 re, im){
    float reu, imu, rev, imv, radv;
    reu = re[0] * _inp[0] - im[0] * _inp[1] + re[1];
    imu = re[0] * _inp[1] + im[0] * _inp[0] + im[1];
    rev = re[2] * _inp[0] - im[2] * _inp[1] + re[3];
    imv = re[2] * _inp[1] + im[2] * _inp[0] + im[3];
    radv = weight / (rev*rev + imv*imv);
    pos[0] = radv * (reu*rev + imu*imv);
    pos[1] = radv * (imu*rev - reu*imv);
}
// 97 ( parametric )
void VAR_CURVE(vector pos, _inp; float weight; vector2 l, a){
    float pc_xlen, pc_ylen, pc_zlen;
    pc_xlen = l[0]*l[0];
    pc_ylen = l[1]*l[1];
    if (pc_xlen<1E-20) pc_xlen = 1E-20;
    if (pc_ylen<1E-20) pc_ylen = 1E-20;
    pos[0] = weight * (_inp[0] + a[0] * exp(_inp[1]*_inp[1]/l[0]));
    pos[1] = weight * (_inp[1] + a[1] * exp(_inp[0]*_inp[0]/l[1]));
}
// 98 ( parametric )
void VAR_PERSPECTIVE(vector pos, _inp; float weight, angle, dist){
    float tt, vsin, vfcos;
    // precalc
    float ang = angle * M_PI / 2.0;
    vsin = sin(ang);
    vfcos = dist * cos(ang);

    tt = 1.0 / (dist - _inp[1] * vsin);
    pos[0] = weight * dist * _inp[0] * tt;
    pos[1] = weight * vfcos * _inp[1] * tt;
}
// 99 ( parametric )
void VAR_BWRAPS(vector pos, _inp; float weight, cellsize, space, gain, innertwist, outertwist){
    float g2, r2, rfactor, max_bubble, Vx, Vy, Cx, Cy, Lx, Ly, rr, theta, ss, cc;
    // precalc
    float radius = 0.5 * (cellsize / (1.0 + space*space ));
    g2 = sqrt(gain) / cellsize + 1e-6;
    max_bubble = g2 * radius;
    if(max_bubble>2.0) max_bubble=1.0;
    else max_bubble *= 1.0/( (max_bubble*max_bubble)/4.0+1.0);
    r2 = radius*radius;
    rfactor = radius/max_bubble;

    Vx = _inp[0];
    Vy = _inp[1];
    if(cellsize == 0.0){
        pos[0] = weight * Vx;
        pos[1] = weight * Vy;
    }
    else{
        Cx = (floor(Vx / cellsize) + 0.5) * cellsize;
        Cy = (floor(Vy / cellsize) + 0.5) * cellsize;
        Lx = Vx - Cx;
        Ly = Vy - Cy;
        if((Lx*Lx + Ly*Ly) > r2){
            pos[0] = weight * Vx;
            pos[1] = weight * Vy;
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
            pos[0] = weight * Vx;
            pos[1] = weight * Vy;
        }
    }
}
// 100
void VAR_HEMISPHERE(vector pos, _inp; float weight){
    float tt;
    tt = weight / sqrt(precalc("SUMSQ", _inp) + 1);
    pos[0] = _inp[0] * tt;
    pos[1] = _inp[1] * tt;
}
// 101 ( parametric )
void VAR_POLYNOMIAL(vector pos, _inp; float weight; vector2 pow, lc, sc){
    float xp, yp;
    xp = pow(weight * abs(_inp[0]), pow[0]);
    yp = pow(weight * abs(_inp[1]), pow[1]);
    pos[0] = xp * sgn(_inp[0]) + lc[0] * _inp[0] * sc[0];
    pos[1] = yp * sgn(_inp[1]) + lc[1] * _inp[1] * sc[1];
}

#endif
