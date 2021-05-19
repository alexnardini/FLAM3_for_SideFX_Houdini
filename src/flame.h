#ifndef __flame_h__
#define __flame_h__

/*  
 /  Title:      SideFX Houdini FRACTAL FLAME generator: 2D
 /  Author:     Alessandro Nardini
 /  date:       October 2020, Last revised May 2021
 /
 /  info:       Based on the original: "The Fractal Flame Algorithm"
 /  Authors:    Scott Draves, Erik Reckase
 /  Weblink:    https://flam3.com/flame_draves.pdf
 /  Date:       September 2003, Last revised November 2008
 /
 /  Name:       TheFractalFlameAlgorithm    "VEX"
 /
 /  Comment:    Main FLAME function.
*/


#include <genome.h>
#include <variations.h>

vector FLAME(genomeParametrics GMP; string ftype; vector pos; int idx, type; vector2 x, y, o; float weight){

    vector outp, _inp, precalc; _inp=0;
    affine(_inp, pos, x, y, o);
    precalc_utils(type, _inp, precalc);
    // FLAME VARIATIONS
    //
    // 00 LINEAR
    if(!type) return _inp * weight;
    if(type<35){
        if(type<18){
            // 01 SINUSOIDAL
            if(type==1){
                VAR_SINUSOIDAL(outp, _inp, weight);
                return outp; }
            // 02 SPHERICAL
            else if(type==2){
                VAR_SPHERICAL(outp, _inp, weight);
                return outp; }
            // 03 SWIRL
            else if(type==3){
                VAR_SWIRL(outp, _inp, weight);
                return outp; }
            // 04 HORSESHOE
            else if(type==4){
                VAR_HORSESHOE(outp, _inp, weight);
                return outp; }
            // 05 POLAR
            else if(type==5){
                VAR_POLAR(outp, _inp, weight);
                return outp; }
            // 06 HANDKERCHIEF
            else if(type==6){
                VAR_HANDKERCHIEF(outp, _inp, weight);
                return outp; }
            // 07 HEART
            else if(type==7){
                VAR_HEART(outp, _inp, weight);
                return outp; }
            // 08 DISC
            else if(type==8){
                VAR_DISC(outp, _inp, weight);
                return outp; }
            // 09 SPIRAL
            else if(type==9){
                VAR_SPIRAL(outp, _inp, precalc, weight);
                return outp; }
            // 10 HIPERBOLIC
            else if(type==10){
                VAR_HIPERBOLIC(outp, _inp, precalc, weight);
                return outp; }
            // 11 DIAMOND
            else if(type==11){
                VAR_DIAMOND(outp, _inp, precalc, weight);
                return outp; }
            // 12 Ex
            else if(type==12){
                VAR_EX(outp, _inp, weight);
                return outp; }
            // 13 Julia
            else if(type==13){
                VAR_JULIA(outp, _inp, weight);
                return outp; }
            // 14 Bent
            else if(type==14){
                VAR_BENT(outp, _inp, weight);
                return outp; }
            // *15 Waves ( dependent )
            else if(type==15){
                VAR_WAVES(outp, _inp, weight, o[0], x[1], y[1], o[1]);
                return outp; }
            // 16 Fisheye
            else if(type==16){
                VAR_FISHEYE(outp, _inp, weight);
                return outp; }
            // *17 Popcorn ( dependent )
            else if(type==17){
                VAR_POPCORN(outp, _inp, weight, o[0], o[1]);
                return outp; }
        }
        else{
            // 18 Exponential
            if(type==18){
                VAR_EXPONENTIAL(outp, _inp, weight);
                return outp; }
            // 19 Power
            else if(type==19){
                VAR_POWER(outp, _inp, precalc, weight);
                return outp; }
            // 20 Cosine
            else if(type==20){
                VAR_COSINE(outp, _inp, weight);
                return outp; }
            // *21 RINGS ( dependent )
            else if(type==21){
                VAR_RINGS(outp, _inp, precalc, weight, o[0]);
                return outp; }
            // *22 FAN ( dependent )
            else if(type==22){
                VAR_FAN(outp, _inp, weight, o[0]);
                return outp; }
            // 23 BUBBLE
            else if(type==23){
                VAR_BUBBLE(outp, _inp, weight);
                return outp; }
            // 24 CYLINDER
            else if(type==24){
                VAR_CYLINDER(outp, _inp, weight);
                return outp; }
            // 25 EYEFISH
            else if(type==25){
                VAR_EYEFISH(outp, _inp, weight);
                return outp; }
            // 26 BLUR
            else if(type==26){
                VAR_BLUR(outp, weight);
                return outp; }
            // 27 CURL ( parametric )
            else if(type==27){
                vector2 curl_c;
                if(ftype=="LOCAL") curl_c = GMP.curl_c[idx];
                else  curl_c = chu("../_curlc_2");
                VAR_CURL(outp, _inp, weight, curl_c[0], curl_c[1]);
                return outp; }
            // 28 NGON ( parametric )
            else if(type==28){
                vector4 ngon;
                if(ftype=="LOCAL") ngon = GMP.ngon[idx];
                else  ngon = chp("../_ngon_2");
                VAR_NGON(outp, _inp, weight, ngon[0], ngon[1], ngon[2], ngon[3]);
                return outp; }
            // 29 PDJ ( parametric )
            else if(type==29){
                vector4 pp;
                if(ftype=="LOCAL") pp = GMP.pdj_w[idx];
                else  pp = chp("../_pdjw_2");
                VAR_PDJ(outp, _inp, weight, pp);
                return outp; }
            // 30 BLOB ( parametric )
            else if(type==30){
                vector blob;
                if(ftype=="LOCAL") blob = GMP.blob[idx];
                else  blob = chv("../_blob_2");
                VAR_BLOB(outp, _inp, precalc, weight, blob[1], blob[0], blob[2]);
                return outp; }
            // 31 JuliaN ( parametric )
            else if(type==31){
                vector2 julian;
                if(ftype=="LOCAL") julian = GMP.julian[idx];
                else  julian = chu("../_julian_2");
                VAR_JULIAN(outp, _inp, weight, julian[0], julian[1]);
                return outp; }
            // 32 JuliaScope ( parametric )
            else if(type==32){
                vector2 juliascope;
                if(ftype=="LOCAL") juliascope = GMP.juliascope[idx];
                else  juliascope = chu("../_juliascope_2");
                VAR_JULIASCOPE(outp, _inp, weight, juliascope[0], juliascope[1]);
                return outp; }
            // 33 Gaussian
            else if(type==33){
                VAR_GAUSSIAN(outp, weight);
                return outp; }
            // 34 Fan2 ( parametric )
            else if(type==34){
                vector2 fan2;
                if(ftype=="LOCAL") fan2 = GMP.fan2[idx];
                else  fan2 = chu("../_fan2_2");
                VAR_FAN2(outp, _inp, weight, fan2);
                return outp; }
        }
    }
    else if(type<70){
        if(type<50){
            // 35 Rings2 ( parametric )
            if(type==35){
                float rings2val;
                if(ftype=="LOCAL") rings2val = GMP.rings2_val[idx];
                else  rings2val = chf("../_rings2val_2");
                VAR_RINGS2(outp, _inp, precalc, weight, rings2val);
                return outp; }
            // 36 Rectangles ( parametric )
            else if(type==36){
                vector2 rect;
                if(ftype=="LOCAL") rect = GMP.rectangles[idx];
                else  rect = chu("../_rectangles_2");
                VAR_RECTANGLES(outp, _inp, weight, rect);
                return outp; }
            // 37 Radial Blur ( parametric )
            else if(type==37){
                vector2 radialblur;
                if(ftype=="LOCAL") radialblur = GMP.radialblur[idx];
                else  radialblur = chu("../_radialblur_2");
                VAR_RADIALBLUR(outp, _inp, weight, radialblur[0], radialblur[1]);
                return outp; }
            // 38 PIE ( parametric )
            else if(type==38){
                vector pie;
                if(ftype=="LOCAL") pie = GMP.pie[idx];
                else  pie = chv("../_pie_2");
                VAR_PIE(outp, weight, pie[0], pie[1], pie[2]);
                return outp; }
            // 39 ARCH
            else if(type==39){
                VAR_ARCH(outp, _inp, weight);
                return outp; }
            // 40 TANGENT
            else if(type==40){
                VAR_TANGENT(outp, _inp, weight);
                return outp; }
            // 41 SQUARE
            else if(type==41){
                VAR_SQUARE(outp, _inp, weight);
                return outp; }
            // 42 RAYS
            else if(type==42){
                VAR_RAYS(outp, _inp, weight);
                return outp; }
            // 43 BLADE
            else if(type==43){
                VAR_BLADE(outp, _inp, weight);
                return outp; }
            // 44 SECANT2
            else if(type==44){
                VAR_SECANT2(outp, _inp, weight);
                return outp; }
            // 45 TWINTRIAN
            else if(type==45){
                VAR_TWINTRIAN(outp, _inp, weight);
                return outp; }
            // 46 CROSS
            else if(type==46){
                VAR_CROSS(outp, _inp, weight);
                return outp; }
            // 47 DISC2 ( parametric )
            else if(type==47){
                vector2 disc2;
                if(ftype=="LOCAL") disc2 = GMP.disc2[idx];
                else  disc2 = chu("../_disc2_2");
                VAR_DISC2(outp, _inp, weight, disc2[0], disc2[1]);
                return outp; }
            // 48 SUPERSHAPE ( parametric )
            else if(type==48){
                vector ss, ss_n;
                if(ftype=="LOCAL"){
                    ss   = GMP.supershape[idx];
                    ss_n = GMP.supershape_n[idx];
                }
                else{
                    ss   = chv("../_supershape_2");
                    ss_n = chv("../_supershapen_2");
                }
                VAR_SUPERSHAPE(outp, _inp, weight, ss[1], ss[0], ss[2], ss_n);
                return outp; }
            // 49 FLOWER ( parametric )
            else if(type==49){
                vector2 flower;
                if(ftype=="LOCAL") flower = GMP.flower[idx];
                else  flower = chu("../_flower_2");
                VAR_FLOWER(outp, _inp, weight, flower[0], flower[1]);
                return outp; }
        }
        else{
            // 50 CONIC
            if(type==50){
                vector2 conic;
                if(ftype=="LOCAL") conic = GMP.conic[idx];
                else  conic =  chu("../_conic_2");
                VAR_CONIC(outp, _inp, weight, conic[0], conic[1]);
                return outp; }
            // 51 PARABOLA ( parametric )
            else if(type==51){
                vector2 parabola;
                if(ftype=="LOCAL") parabola = GMP.parabola[idx];
                else  parabola = chu("../_parabola_2");
                VAR_PARABOLA(outp, _inp, weight, parabola[0], parabola[1]);
                return outp; }
            // 52 BENT2 ( parametric )
            else if(type==52){
                vector2 bent2;
                if(ftype=="LOCAL") bent2 = GMP.bent2[idx];
                else  bent2 = chu("../_bent2xy_2");
                VAR_BENT2(outp, _inp, weight, bent2);
                return outp; }
            // 53 BIPOLAR ( parametric )
            else if(type==53){
                float shift;
                if(ftype=="LOCAL") shift = GMP.bipolar_shift[idx];
                else  shift = chf("../_bipolarshift_2");
                VAR_BIPOLAR(outp, _inp, weight, shift);
                return outp; }
            // 54 BOARDERS
            else if(type==54){
                VAR_BOARDERS(outp, _inp, weight);
                return outp; }
            // 55 BUTTERFLY
            else if(type==55){
                VAR_BUTTERFLY(outp, _inp, weight);
                return outp; }
            // 56 CELL ( parametric )
            else if(type==56){
                float size;
                if(ftype=="LOCAL") size = GMP.cell_size[idx];
                else  size = chf("../_cellsize_2");
                VAR_CELL(outp, _inp, weight, size);
                return outp; }
            // 57 CPOW ( parametric )
            else if(type==57){
                vector cpow;
                if(ftype=="LOCAL") cpow = GMP.cpow[idx];
                else  cpow = chv("../_cpow_2");
                VAR_CPOW(outp, _inp, weight, cpow[0], cpow[1], cpow[2]);
                return outp; }
            // 58 EDISC
            else if(type==58){
                VAR_EDISC(outp, _inp, weight);
                return outp; }
            // 59 ELLIPTIC
            else if(type==59){
                VAR_ELLIPTIC(outp, _inp, weight);
                return outp; }
            // 60 NOISE
            else if(type==60){
                VAR_NOISE(outp, _inp, weight);
                return outp; }
            // 61 ESCHER ( parametric )
            else if(type==61){
                float beta;
                if(ftype=="LOCAL") beta = GMP.escher_beta[idx];
                else  beta = chf("../_escherbeta_2");
                VAR_ESCHER(outp, _inp, weight, beta);
                return outp; }
            // 62 FOCI
            else if(type==62){
                VAR_FOCI(outp, _inp, weight);
                return outp; }
            // 63 LAZYSUSAN ( parametric )
            else if(type==63){
                vector lazysusan;
                vector2 lazysusanxyz;
                if(ftype=="LOCAL"){
                    lazysusanxyz  = GMP.lazysusanxyz[idx];
                    lazysusan     = GMP.lazysusan[idx];
                }
                else{
                    lazysusanxyz  = chu("../_lazysusanxyz_2");
                    lazysusan     = chv("../_lazysusan_2");
                }
                VAR_LAZYSUSAN(outp, _inp, weight, lazysusan[0], lazysusan[1], lazysusan[2], lazysusanxyz);
                return outp; }
            // 64 LOONIE
            else if(type==64){
                VAR_LOONIE(outp, _inp, weight);
                return outp; }
            // 65 PRE BLUR
            /*
            else if(type==65){
                VAR_PREBLUR(outp, weight);
                return outp; }
            */
            // 66 MODULUS ( parametric )
            else if(type==66){
                vector2 mod;
                if(ftype=="LOCAL") mod = GMP.modulus[idx];
                else  mod = chu("../_modulusXYZ_2");
                VAR_MODULUS(outp, _inp, weight, mod);
                return outp; }
            // 67 OSCOPE ( parametric )
            else if(type==67){
                vector4 oscope;
                if(ftype=="LOCAL") oscope = GMP.oscope[idx];
                else  oscope = chp("../_oscope_2");
                VAR_OSCOPE(outp, _inp, weight, oscope[0], oscope[1], oscope[2], oscope[3]);
                return outp; }
            // 68 POLAR2
            else if(type==68){
                VAR_POLAR2(outp, _inp, weight);
                return outp; }
            // 69 POPCORN2 ( parametric )
            else if(type==69){
                float pop2c;
                vector2 pop2;
                if(ftype=="LOCAL"){
                    pop2  = GMP.popcorn2[idx];
                    pop2c = GMP.popcorn2_c[idx];
                }
                else{
                    pop2  = chu("../_popcorn2xyz_2");
                    pop2c = chf("../_popcorn2c_2");
                }
                VAR_POPCORN2(outp, _inp, weight, pop2c, pop2);
                return outp; }
        }
    }
    else if(type<102){
        if(type<86){
            // 70 SCRY ( parametric )
            if(type==70){
                VAR_SCRY(outp, _inp, weight);
                return outp; }
            // 71 SEPARATION ( parametric )
            else if(type==71){
                vector2 sep, ins;
                if(ftype=="LOCAL"){
                    sep = GMP.separation[idx];
                    ins = GMP.separation_inside[idx];
                }
                else{
                    sep = chu("../_separationxyz_2");
                    ins = chu("../_separationinsidexyz_2");
                }
                VAR_SEPARATION(outp, _inp, weight, sep, ins);
                return outp; }
            // 72 SPLIT ( parametric )
            else if(type==72){
                vector2 split;
                if(ftype=="LOCAL") split = GMP.split[idx];
                else  split = chu("../_splitxyz_2");
                VAR_SPLIT(outp, _inp, weight, split);
                return outp; }
            // 73 SPLITS ( parametric )
            else if(type==73){
                vector2 splits;
                if(ftype=="LOCAL") splits = GMP.splits[idx];
                else  splits = chu("../_splitsxyz_2");
                VAR_SPLITS(outp, _inp, weight, splits);
                return outp; }
            // 74 STRIPES ( parametric )
            else if(type==74){
                vector2 stripes;
                if(ftype=="LOCAL") stripes = GMP.stripes[idx];
                else  stripes = chu("../_stripes_2");
                VAR_STRIPES(outp, _inp, weight, stripes[0], stripes[1]);
                return outp; }
            // 75 WEDGE ( parametric )
            else if(type==75){
                vector4 wedge;
                if(ftype=="LOCAL") wedge = GMP.wedge[idx];
                else  wedge = chp("../_wedge_2");
                VAR_WEDGE(outp, _inp, weight, wedge[0], wedge[1], wedge[2], wedge[3]);
                return outp; }
            // 76 WEDGE JULIA ( parametric )
            else if(type==76){
                vector4 wedgejulia;
                if(ftype=="LOCAL") wedgejulia = GMP.wedgejulia[idx];
                else  wedgejulia = chp("../_wedgejulia_2");
                VAR_WEDGEJULIA(outp, _inp, weight, wedgejulia[0], wedgejulia[1], wedgejulia[2], wedgejulia[3]);
                return outp; }
            // 77 WEDGE SPH ( parametric )
            else if(type==77){
                vector4 wedgesph;
                if(ftype=="LOCAL") wedgesph = GMP.wedgesph[idx];
                else  wedgesph = chp("../_wedgesph_2");
                VAR_WEDGESPH(outp, _inp, weight, wedgesph[0], wedgesph[1], wedgesph[2], wedgesph[3]);
                return outp; }
            // 78 WHORL ( parametric )
            else if(type==78){
                vector2 whorl;
                if(ftype=="LOCAL") whorl  = GMP.whorl[idx];
                else  whorl  = chu("../_whorl_2");
                VAR_WHORL(outp, _inp, weight, whorl[0], whorl[1]);
                return outp; }
            // 79 WAVES2 ( parametric )
            else if(type==79){
                vector2 scl, freq;
                if(ftype=="LOCAL"){
                    scl  = GMP.waves2_scale[idx];
                    freq = GMP.waves2_freq[idx];
                }
                else{
                    scl  = chu("../_waves2scalexyz_2");
                    freq = chu("../_waves2freqxyz_2");
                }
                VAR_WAVES2(outp, _inp, weight, scl, freq);
                return outp; }
            // 80 COTHE EXP
            else if(type==80){
                VAR_COTHEEXP(outp, _inp, weight);
                return outp; }
            // 81 COTHE LOG
            else if(type==81){
                VAR_COTHELOG(outp, _inp, weight);
                return outp; }
            // 82 COTHE SIN
            else if(type==82){
                VAR_COTHESIN(outp, _inp, weight);
                return outp; }
            // 83 COTHE COS
            else if(type==83){
                VAR_COTHECOS(outp, _inp, weight);
                return outp; }
            // 84 COTHE TAN
            else if(type==84){
                VAR_COTHETAN(outp, _inp, weight);
                return outp; }
            // 85 COTHE SEC
            else if(type==85){
                VAR_COTHESEC(outp, _inp, weight);
                return outp; }
        }
        else{
            // 86 COTHE CSC
            if(type==86){
                VAR_COTHECSC(outp, _inp, weight);
                return outp; }
            // 87 COTHE COT
            else if(type==87){
                VAR_COTHECOT(outp, _inp, weight);
                return outp; }
            // 88 COTHE SINH
            else if(type==88){
                VAR_COTHESINH(outp, _inp, weight);
                return outp; }
            // 89 COTHE COSH
            else if(type==89){
                VAR_COTHECOSH(outp, _inp, weight);
                return outp; }
            // 90 COTHE TANH
            else if(type==90){
                VAR_COTHETANH(outp, _inp, weight);
                return outp; }
            // 91 COTHE SECH
            else if(type==91){
                VAR_COTHESECH(outp, _inp, weight);
                return outp; }
            // 92 COTHE CSCH
            else if(type==92){
                VAR_COTHECSCH(outp, _inp, weight);
                return outp; }
            // 93 COTHE COTH
            else if(type==93){
                VAR_COTHECOTH(outp, _inp, weight);
                return outp; }
            // 94 AUGER ( parametric )
            else if(type==94){
                vector4 auger;
                if(ftype=="LOCAL") auger = GMP.auger[idx];
                else  auger = chp("../_auger_2");
                VAR_AUGER(outp, _inp, weight, auger[0], auger[1], auger[2], auger[3]);
                return outp; }
            // 95 FLUX ( parametric )
            else if(type==95){
                float spread;
                if(ftype=="LOCAL") spread = GMP.flux_spread[idx];
                else  spread = chf("../_fluxspread_2");
                VAR_FLUX(outp, _inp, weight, spread);
                return outp; }
            // 96 MOBIUS ( parametric )
            else if(type==96){
                vector4 re, im;
                if(ftype=="LOCAL"){
                    re  = GMP.mobius_re[idx];
                    im  = GMP.mobius_im[idx];
                }
                else{
                    re  = chp("../_mobiusre_2");
                    im  = chp("../_mobiusim_2");
                }
                VAR_MOBIUS(outp, _inp, weight, re, im);
                return outp; }
            // 97 CURVE ( parametric )
            else if(type==97){
                vector2 lgt, amp;
                if(ftype=="LOCAL"){
                    lgt = GMP.curve_lenght[idx];
                    amp = GMP.curve_amp[idx];
                }
                else{
                    lgt = chu("../_curvexyzlenght_2");
                    amp = chu("../_curvexyzamp_2");
                }
                VAR_CURVE(outp, _inp, weight, lgt, amp);
                return outp; }
            // 98 PERSPECTIVE ( parametric )
            else if(type==98){
                vector2 persp;
                if(ftype=="LOCAL") persp = GMP.persp[idx];
                else  persp = chu("../_persp_2");
                VAR_PERSPECTIVE(outp, _inp, weight, persp[0], persp[1]);
                return outp; }
            // 99 BWRAPS ( parametric )
            else if(type==99){
                vector bwraps;
                vector2 bwrapstwist;
                if(ftype=="LOCAL"){
                    bwraps = GMP.bwraps[idx];
                    bwrapstwist = GMP.bwrapstwist[idx];
                }
                else{
                    bwraps = chv("../_bwraps_2");
                    bwrapstwist = chu("../_bwrapstwist_2");
                }
                VAR_BWRAPS(outp, _inp, weight, bwraps[0], bwraps[1], bwraps[2], bwrapstwist[0], bwrapstwist[1]);
                return outp; }
            // 100 HEMISPHERE
            else if(type==100){
                VAR_HEMISPHERE(outp, _inp, weight);
                return outp; }
            // 101 POLYNOMIAL ( parametric )
            else if(type==101){
                vector2 pow, lc, sc;
                if(ftype=="LOCAL"){
                    pow = GMP.polynomial_pow[idx];
                    lc  = GMP.polynomial_lc[idx];
                    sc  = GMP.polynomial_sc[idx];
                }
                else{
                    pow = chu("../_polynomialpow_2");
                    lc  = chu("../_polynomiallc_2");
                    sc  = chu("../_polynomialsc_2");
                }
                VAR_POLYNOMIAL(outp, _inp, weight, pow, lc, sc);
                return outp; }
        }
    }
    return _inp;
}

#endif
