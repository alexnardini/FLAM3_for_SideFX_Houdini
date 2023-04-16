#ifndef __flame_h__
#define __flame_h__

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
 /  Name:       FLAME "CVEX"
 /
 /  Comment:    FLAM3 variation selection.
 /              Type 65 PRE BLUR is missing as it is hardcoded into the chaose game,
 /              so there is a jump from 64 to 66 directly.
*/


#include <genome.h>
#include <variations.h>

// From Fractorium: flam3 comptibility (f3c). Check inside variations.h to see both versions of each.
// The behavior of the cos, cosh, cot, coth, csc, csch, sec, sech, sin, sinh, tan and tanh variations are different in flam3/Apophysis versus Chaotica.
// Checked: use the Apophysis behavior. Unchecked: use the Chaotica behavior.
vector2 FLAME(const gemPrm GMP; const int idx, T, f3c; const vector2 pos, x, y, o; const float w){

    //  p = out position
    // _p = incoming position
    vector2 p, _p; _p = pos;
    
    // VARs with precalc pos: 9, 10, 11, 19, 21, 30, 35

    // FLAME VARIATIONS
    //
    // 00 LINEAR
    if(!T) return _p*w;
    else if(T<35){
        if(T<18){
            // 01 SINUSOIDAL
            if(T==1){
                V_SINUSOIDAL(p, _p, w);
                return p; }
            // 02 SPHERICAL
            else if(T==2){
                V_SPHERICAL(p, _p, w);
                return p; }
            // 03 SWIRL
            else if(T==3){
                V_SWIRL(p, _p, w);
                return p; }
            // 04 HORSESHOE
            else if(T==4){
                V_HORSESHOE(p, _p, w);
                return p; }
            // 05 POLAR
            else if(T==5){
                V_POLAR(p, _p, w);
                return p; }
            // 06 HANDKERCHIEF
            else if(T==6){
                V_HANDKERCHIEF(p, _p, w);
                return p; }
            // 07 HEART
            else if(T==7){
                V_HEART(p, _p, w);
                return p; }
            // 08 DISC
            else if(T==8){
                V_DISC(p, _p, w);
                return p; }
            // 09 SPIRAL
            else if(T==9){
                V_SPIRAL(p, _p, w);
                return p; }
            // 10 HIPERBOLIC
            else if(T==10){
                V_HIPERBOLIC(p, _p, w);
                return p; }
            // 11 DIAMOND
            else if(T==11){
                V_DIAMOND(p, _p, w);
                return p; }
            // 12 Ex
            else if(T==12){
                V_EX(p, _p, w);
                return p; }
            // 13 Julia
            else if(T==13){
                V_JULIA(p, _p, w);
                return p; }
            // 14 Bent
            else if(T==14){
                V_BENT(p, _p, w);
                return p; }
            // *15 Waves ( dependent )
            else if(T==15){
                V_WAVES(p, _p, w, x[1], y[0], o[0], o[1]);
                return p; }
            // 16 Fisheye
            else if(T==16){
                V_FISHEYE(p, _p, w);
                return p; }
            // *17 Popcorn ( dependent )
            else if(T==17){
                V_POPCORN(p, _p, w, o[0], o[1]);
                return p; }
        }
        else{
            // 18 Exponential
            if(T==18){
                V_EXPONENTIAL(p, _p, w);
                return p; }
            // 19 Power
            else if(T==19){
                V_POWER(p, _p, w);
                return p; }
            // 20 Cosine
            else if(T==20){
                V_COSINE(p, _p, w);
                return p; }
            // *21 RINGS ( dependent )
            else if(T==21){
                V_RINGS(p, _p, w, o[0]);
                return p; }
            // *22 FAN ( dependent )
            else if(T==22){
                V_FAN(p, _p, w, o[0], o[1]);
                return p; }
            // 23 BUBBLE
            else if(T==23){
                V_BUBBLE(p, _p, w);
                return p; }
            // 24 CYLINDER
            else if(T==24){
                V_CYLINDER(p, _p, w);
                return p; }
            // 25 EYEFISH
            else if(T==25){
                V_EYEFISH(p, _p, w);
                return p; }
            // 26 BLUR
            else if(T==26){
                V_BLUR(p, w);
                return p; }
            // 27 CURL ( parametric )
            else if(T==27){
                vector2 curl_c = GMP.curl_c[idx];
                V_CURL(p, _p, w, curl_c[0], curl_c[1]);
                return p; }
            // 28 NGON ( parametric )
            else if(T==28){
                vector4 ngon = GMP.ngon[idx];
                V_NGON(p, _p, w, ngon[0], ngon[1], ngon[2], ngon[3]);
                return p; }
            // 29 PDJ ( parametric )
            else if(T==29){
                vector4 pp = GMP.pdj_w[idx];
                V_PDJ(p, _p, w, pp);
                return p; }
            // 30 BLOB ( parametric )
            else if(T==30){
                vector blob = GMP.blob[idx];
                V_BLOB(p, _p, w, blob[1], blob[0], blob[2]);
                return p; }
            // 31 JuliaN ( parametric )
            else if(T==31){
                vector2 julian = GMP.julian[idx];
                V_JULIAN(p, _p, w, julian[0], julian[1]);
                return p; }
            // 32 JuliaScope ( parametric )
            else if(T==32){
                vector2 juliascope = GMP.juliascope[idx];
                V_JULIASCOPE(p, _p, w, juliascope[0], juliascope[1]);
                return p; }
            // 33 Gaussian
            else if(T==33){
                V_GAUSSIAN_BLUR(p, w);
                return p; }
            // 34 Fan2 ( parametric )
            else if(T==34){
                vector2 fan2 = GMP.fan2[idx];
                V_FAN2(p, _p, w, fan2);
                return p; }
        }
    }
    else if(T<70){
        if(T<52){
            // 35 Rings2 ( parametric )
            if(T==35){
                float rings2val = GMP.rings2_val[idx];
                V_RINGS2(p, _p, w, rings2val);
                return p; }
            // 36 Rectangles ( parametric )
            else if(T==36){
                vector2 rect = GMP.rectangles[idx];
                V_RECTANGLES(p, _p, w, rect);
                return p; }
            // 37 Radial Blur ( parametric )
            else if(T==37){
                vector2 radialblur = GMP.radialblur[idx];
                V_RADIALBLUR(p, _p, w, radialblur[0], radialblur[1]);
                return p; }
            // 38 PIE ( parametric )
            else if(T==38){
                vector pie = GMP.pie[idx];
                V_PIE(p, w, pie[0], pie[1], pie[2]);
                return p; }
            // 39 ARCH
            else if(T==39){
                V_ARCH(p, _p, w);
                return p; }
            // 40 TANGENT
            else if(T==40){
                V_TANGENT(p, _p, w);
                return p; }
            // 41 SQUARE
            else if(T==41){
                V_SQUARE(p, _p, w);
                return p; }
            // 42 RAYS
            else if(T==42){
                V_RAYS(p, _p, w);
                return p; }
            // 43 BLADE
            else if(T==43){
                V_BLADE(p, _p, w);
                return p; }
            // 44 SECANT2
            else if(T==44){
                V_SECANT2(p, _p, w);
                return p; }
            // 45 TWINTRIAN
            else if(T==45){
                V_TWINTRIAN(p, _p, w);
                return p; }
            // 46 CROSS
            else if(T==46){
                V_CROSS(p, _p, w);
                return p; }
            // 47 DISC2 ( parametric )
            else if(T==47){
                vector2 disc2 = GMP.disc2[idx];
                vector precalc = GMP.pc_DISC2[idx];
                V_DISC2_L(p, _p, w, disc2[0], disc2[1], precalc);
                return p; }
            // 48 SUPERSHAPE ( parametric )
            else if(T==48){
                vector ss, ss_n;
                ss = GMP.supershape[idx];
                ss_n = GMP.supershape_n[idx];
                V_SUPERSHAPE(p, _p, w, ss[1], ss[0], ss[2], ss_n);
                return p; }
            // 49 FLOWER ( parametric )
            else if(T==49){
                vector2 flower = GMP.flower[idx];
                V_FLOWER(p, _p, w, flower[0], flower[1]);
                return p; }
            // 50 CONIC ( parametric )
            else if(T==50){
                vector2 conic = GMP.conic[idx];
                V_CONIC(p, _p, w, conic[0], conic[1]);
                return p; }
            // 51 PARABOLA ( parametric )
            else if(T==51){
                vector2 parabola = GMP.parabola[idx];
                V_PARABOLA(p, _p, w, parabola[0], parabola[1]);
                return p; }
        }
        else{
            // 52 BENT2 ( parametric )
            if(T==52){
                vector2 bent2 = GMP.bent2[idx];
                V_BENT2(p, _p, w, bent2);
                return p; }
            // 53 BIPOLAR ( parametric )
            else if(T==53){
                float shift = GMP.bipolar_shift[idx];
                V_BIPOLAR(p, _p, w, shift);
                return p; }
            // 54 BOARDERS
            else if(T==54){
                V_BOARDERS(p, _p, w);
                return p; }
            // 55 BUTTERFLY
            else if(T==55){
                V_BUTTERFLY(p, _p, w);
                return p; }
            // 56 CELL ( parametric )
            else if(T==56){
                float size = GMP.cell_size[idx];
                V_CELL(p, _p, w, size);
                return p; }
            // 57 CPOW ( parametric )
            else if(T==57){
                vector cpow = GMP.cpow[idx];
                V_CPOW(p, _p, w, cpow[0], cpow[1], cpow[2]);
                return p; }
            // 58 EDISC
            else if(T==58){
                V_EDISC(p, _p, w);
                return p; }
            // 59 ELLIPTIC
            else if(T==59){
                V_ELLIPTIC(p, _p, w);
                return p; }
            // 60 NOISE
            else if(T==60){
                V_NOISE(p, _p, w);
                return p; }
            // 61 ESCHER ( parametric )
            else if(T==61){
                float beta = GMP.escher_beta[idx];
                V_ESCHER(p, _p, w, beta);
                return p; }
            // 62 FOCI
            else if(T==62){
                V_FOCI(p, _p, w);
                return p; }
            // 63 LAZYSUSAN ( parametric )
            else if(T==63){
                vector lazysusan = GMP.lazysusan[idx];
                vector2 lazysusanxyz = GMP.lazysusanxyz[idx];
                V_LAZYSUSAN(p, _p, w, lazysusan[0], lazysusan[1], lazysusan[2], lazysusanxyz);
                return p; }
            // 64 LOONIE
            else if(T==64){
                V_LOONIE(p, _p, w);
                return p; }
            // 65 PRE BLUR ( Hard coded into the chaos game )
            /*
            else if(T==65){
                V_PREBLUR(p, w);
                return p; }
            */
            // 66 MODULUS ( parametric )
            else if(T==66){
                vector2 mod = GMP.modulus[idx];
                V_MODULUS(p, _p, w, mod);
                return p; }
            // 67 OSCOPE ( parametric )
            else if(T==67){
                vector4 oscope = GMP.oscope[idx];
                V_OSCOPE(p, _p, w, oscope[0], oscope[1], oscope[2], oscope[3]);
                return p; }
            // 68 POLAR2
            else if(T==68){
                V_POLAR2(p, _p, w);
                return p; }
            // 69 POPCORN2 ( parametric )
            else if(T==69){
                float pop2c = GMP.popcorn2_c[idx];
                vector2 pop2 = GMP.popcorn2[idx];
                V_POPCORN2(p, _p, w, pop2c, pop2);
                return p; }
        }
    }
    else{
        if(T<88){
            // 70 SCRY ( parametric )
            if(T==70){
                V_SCRY(p, _p, w);
                return p; }
            // 71 SEPARATION ( parametric )
            else if(T==71){
                vector2 sep, ins;
                sep = GMP.separation[idx];
                ins = GMP.separation_inside[idx];
                V_SEPARATION(p, _p, w, sep, ins);
                return p; }
            // 72 SPLIT ( parametric )
            else if(T==72){
                vector2 split = GMP.split[idx];
                V_SPLIT(p, _p, w, split);
                return p; }
            // 73 SPLITS ( parametric )
            else if(T==73){
                vector2 splits = GMP.splits[idx];
                V_SPLITS(p, _p, w, splits);
                return p; }
            // 74 STRIPES ( parametric )
            else if(T==74){
                vector2 stripes = GMP.stripes[idx];
                V_STRIPES(p, _p, w, stripes[0], stripes[1]);
                return p; }
            // 75 WEDGE ( parametric )
            else if(T==75){
                vector4 wedge = GMP.wedge[idx];
                V_WEDGE(p, _p, w, wedge[0], wedge[1], wedge[2], wedge[3]);
                return p; }
            // 76 WEDGE JULIA ( parametric )
            else if(T==76){
                vector4 wedgejulia = GMP.wedgejulia[idx];
                V_WEDGEJULIA(p, _p, w, wedgejulia[0], wedgejulia[1], wedgejulia[2], wedgejulia[3]);
                // vector precalc = GMP.pc_WEDGEJULIA[idx];
                // V_WEDGEJULIA_L(p, _p, w, wedgejulia[0], wedgejulia[1], wedgejulia[2], wedgejulia[3], precalc);
                return p; }
            // 77 WEDGE SPH ( parametric )
            else if(T==77){
                vector4 wedgesph = GMP.wedgesph[idx];
                V_WEDGESPH(p, _p, w, wedgesph[0], wedgesph[1], wedgesph[2], wedgesph[3]);
                return p; }
            // 78 WHORL ( parametric )
            else if(T==78){
                vector2 whorl = GMP.whorl[idx];
                V_WHORL(p, _p, w, whorl[0], whorl[1]);
                return p; }
            // 79 WAVES2 ( parametric )
            else if(T==79){
                vector2 scl, freq;
                scl = GMP.waves2_scale[idx];
                freq = GMP.waves2_freq[idx];
                V_WAVES2(p, _p, w, scl, freq);
                return p; }
            // 80 COTHE EXP
            else if(T==80){
                V_EXP(p, _p, w);
                return p; }
            // 81 COTHE LOG
            else if(T==81){
                V_LOG(p, _p, w);
                return p; }
            // 82 COTHE SIN
            else if(T==82){
                V_SIN(f3c, p, _p, w);
                return p; }
            // 83 COTHE COS
            else if(T==83){
                V_COS(f3c, p, _p, w);
                return p; }
            // 84 COTHE TAN
            else if(T==84){
                V_TAN(f3c, p, _p, w);
                return p; }
            // 85 COTHE SEC
            else if(T==85){
                V_SEC(f3c, p, _p, w);
                return p; }
            // 86 COTHE CSC
            else if(T==86){
                V_CSC(f3c, p, _p, w);
                return p; }
            // 87 COTHE COT
            if(T==87){
                V_COT(f3c, p, _p, w);
                return p; }
        }
        else{
            // 88 COTHE SINH
            if(T==88){
                V_SINH(f3c, p, _p, w);
                return p; }
            // 89 COTHE COSH
            else if(T==89){
                V_COSH(f3c, p, _p, w);
                return p; }
            // 90 COTHE TANH
            else if(T==90){
                V_TANH(f3c, p, _p, w);
                return p; }
            // 91 COTHE SECH
            else if(T==91){
                V_SECH(f3c, p, _p, w);
                return p; }
            // 92 COTHE CSCH
            else if(T==92){
                V_CSCH(f3c, p, _p, w);
                return p; }
            // 93 COTHE COTH
            else if(T==93){
                V_COTH(f3c, p, _p, w);
                return p; }
            // 94 AUGER ( parametric )
            else if(T==94){
                vector4 auger = GMP.auger[idx];
                V_AUGER(p, _p, w, auger[0], auger[1], auger[2], auger[3]);
                return p; }
            // 95 FLUX ( parametric )
            else if(T==95){
                float spread = GMP.flux_spread[idx];
                V_FLUX(p, _p, w, spread);
                return p; }
            // 96 MOBIUS ( parametric )
            else if(T==96){
                vector4 re, im;
                re = GMP.mobius_re[idx];
                im = GMP.mobius_im[idx];
                V_MOBIUS(p, _p, w, re, im);
                return p; }
            // 97 CURVE ( parametric )
            else if(T==97){
                vector2 lgt, amp;
                lgt = GMP.curve_lenght[idx];
                amp = GMP.curve_amp[idx];
                V_CURVE(p, _p, w, lgt, amp);
                return p; }
            // 98 PERSPECTIVE ( parametric )
            else if(T==98){
                vector2 persp = GMP.persp[idx];
                V_PERSPECTIVE(p, _p, w, persp[0], persp[1]);
                return p; }
            // 99 BWRAPS ( parametric )
            else if(T==99){
                vector bwraps = GMP.bwraps[idx];
                vector2 bwrapstwist = GMP.bwrapstwist[idx];
                V_BWRAPS(p, _p, w, bwraps[0], bwraps[1], bwraps[2], bwrapstwist[0], bwrapstwist[1]);
                // vector precalc = GMP.pc_BWRAPS[idx];
                // V_BWRAPS_L(p, _p, w, bwraps[0], bwraps[1], bwraps[2], bwrapstwist[0], bwrapstwist[1], precalc);
                return p; }
            // 100 HEMISPHERE
            else if(T==100){
                V_HEMISPHERE(p, _p, w);
                return p; }
            // 101 POLYNOMIAL ( parametric )
            else if(T==101){
                vector2 pow, lc, sc;
                pow = GMP.polynomial_pow[idx];
                lc = GMP.polynomial_lc[idx];
                sc = GMP.polynomial_sc[idx];
                V_POLYNOMIAL(p, _p, w, pow, lc, sc);
                return p; }
            // 102 CROP ( parametric )
            else if(T==102){
                vector4 ltrb = GMP.crop_ltrb[idx];
                vector2 az = GMP.crop_az[idx];
                V_CROP(p, _p, w, ltrb[0], ltrb[1], ltrb[2], ltrb[3], az[0], az[1]);
                return p; }
            // 103 UNPOLAR
            else if(T==103){
                V_UNPOLAR(p, _p, w);
                return p; }
            // 104 GLYNNIA
            else if(T==104){
                V_GLYNNIA(p, _p, w);
                return p; }
            // 105 POINT_SYMMETRY ( parametric )
            else if(T==105){
                vector ptsym = GMP.point_symmetry[idx];
                V_POINT_SYMMETRY(p, _p, w, ptsym[0], ptsym[1], ptsym[2]);
                return p; }
        }
    }
    return _p;
}

#endif
