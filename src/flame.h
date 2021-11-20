#ifndef __flame_h__
#define __flame_h__

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
 /  Name:       TheFractalFlameAlgorithm    "VEX"
 /
 /  Comment:    Main FLAME function.
*/


#include <genome.h>
#include <variations.h>


vector2 FLAME(const gemPrm GMP; const int ftype, idx, type; const vector2 pos, x, y, o; const float w){

    //  p = out position
    // _p = incoming position
    vector2 p, _p; _p=pos;
    affine(_p, x, y, o);
    // VARs with precalc pos: 9, 10, 11, 19, 21, 30, 35

    // FLAME VARIATIONS
    //
    // 00 LINEAR
    if(!type) return _p*w;
    else if(type<35){
        if(type<18){
            // 01 SINUSOIDAL
            if(type==1){
                V_SINUSOIDAL(p, _p, w);
                return p; }
            // 02 SPHERICAL
            else if(type==2){
                V_SPHERICAL(p, _p, w);
                return p; }
            // 03 SWIRL
            else if(type==3){
                V_SWIRL(p, _p, w);
                return p; }
            // 04 HORSESHOE
            else if(type==4){
                V_HORSESHOE(p, _p, w);
                return p; }
            // 05 POLAR
            else if(type==5){
                V_POLAR(p, _p, w);
                return p; }
            // 06 HANDKERCHIEF
            else if(type==6){
                V_HANDKERCHIEF(p, _p, w);
                return p; }
            // 07 HEART
            else if(type==7){
                V_HEART(p, _p, w);
                return p; }
            // 08 DISC
            else if(type==8){
                V_DISC(p, _p, w);
                return p; }
            // 09 SPIRAL
            else if(type==9){
                V_SPIRAL(p, _p, w);
                return p; }
            // 10 HIPERBOLIC
            else if(type==10){
                V_HIPERBOLIC(p, _p, w);
                return p; }
            // 11 DIAMOND
            else if(type==11){
                V_DIAMOND(p, _p, w);
                return p; }
            // 12 Ex
            else if(type==12){
                V_EX(p, _p, w);
                return p; }
            // 13 Julia
            else if(type==13){
                V_JULIA(p, _p, w);
                return p; }
            // 14 Bent
            else if(type==14){
                V_BENT(p, _p, w);
                return p; }
            // *15 Waves ( dependent )
            else if(type==15){
                V_WAVES(p, _p, w, o[0], x[1], y[1], o[1]);
                return p; }
            // 16 Fisheye
            else if(type==16){
                V_FISHEYE(p, _p, w);
                return p; }
            // *17 Popcorn ( dependent )
            else if(type==17){
                V_POPCORN(p, _p, w, o[0], o[1]);
                return p; }
        }
        else{
            // 18 Exponential
            if(type==18){
                V_EXPONENTIAL(p, _p, w);
                return p; }
            // 19 Power
            else if(type==19){
                V_POWER(p, _p, w);
                return p; }
            // 20 Cosine
            else if(type==20){
                V_COSINE(p, _p, w);
                return p; }
            // *21 RINGS ( dependent )
            else if(type==21){
                V_RINGS(p, _p, w, o[0]);
                return p; }
            // *22 FAN ( dependent )
            else if(type==22){
                V_FAN(p, _p, w, o[0]);
                return p; }
            // 23 BUBBLE
            else if(type==23){
                V_BUBBLE(p, _p, w);
                return p; }
            // 24 CYLINDER
            else if(type==24){
                V_CYLINDER(p, _p, w);
                return p; }
            // 25 EYEFISH
            else if(type==25){
                V_EYEFISH(p, _p, w);
                return p; }
            // 26 BLUR
            else if(type==26){
                V_BLUR(p, w);
                return p; }
            // 27 CURL ( parametric )
            else if(type==27){
                vector2 curl_c;
                if(!ftype) curl_c = GMP.curl_c[idx];
                else  curl_c = chu(concat(PRX(ftype), "curlc_2"));
                V_CURL(p, _p, w, curl_c[0], curl_c[1]);
                return p; }
            // 28 NGON ( parametric )
            else if(type==28){
                vector4 ngon;
                if(!ftype) ngon = GMP.ngon[idx];
                else  ngon = chp(concat(PRX(ftype), "ngon_2"));
                V_NGON(p, _p, w, ngon[0], ngon[1], ngon[2], ngon[3]);
                return p; }
            // 29 PDJ ( parametric )
            else if(type==29){
                vector4 pp;
                if(!ftype) pp = GMP.pdj_w[idx];
                else  pp = chp(concat(PRX(ftype), "pdjw_2"));
                V_PDJ(p, _p, w, pp);
                return p; }
            // 30 BLOB ( parametric )
            else if(type==30){
                vector blob;
                if(!ftype) blob = GMP.blob[idx];
                else  blob = chv(concat(PRX(ftype), "blob_2"));
                V_BLOB(p, _p, w, blob[1], blob[0], blob[2]);
                return p; }
            // 31 JuliaN ( parametric )
            else if(type==31){
                vector2 julian;
                if(!ftype) julian = GMP.julian[idx];
                else  julian = chu(concat(PRX(ftype), "julian_2"));
                V_JULIAN(p, _p, w, julian[0], julian[1]);
                return p; }
            // 32 JuliaScope ( parametric )
            else if(type==32){
                vector2 juliascope;
                if(!ftype) juliascope = GMP.juliascope[idx];
                else  juliascope = chu(concat(PRX(ftype), "juliascope_2"));
                V_JULIASCOPE(p, _p, w, juliascope[0], juliascope[1]);
                return p; }
            // 33 Gaussian
            else if(type==33){
                V_GAUSSIAN(p, w);
                return p; }
            // 34 Fan2 ( parametric )
            else if(type==34){
                vector2 fan2;
                if(!ftype) fan2 = GMP.fan2[idx];
                else  fan2 = chu(concat(PRX(ftype), "fan2_2"));
                V_FAN2(p, _p, w, fan2);
                return p; }
        }
    }
    else if(type<70){
        if(type<50){
            // 35 Rings2 ( parametric )
            if(type==35){
                float rings2val;
                if(!ftype) rings2val = GMP.rings2_val[idx];
                else  rings2val = chf(concat(PRX(ftype), "rings2val_2"));
                V_RINGS2(p, _p, w, rings2val);
                return p; }
            // 36 Rectangles ( parametric )
            else if(type==36){
                vector2 rect;
                if(!ftype) rect = GMP.rectangles[idx];
                else  rect = chu(concat(PRX(ftype), "rectangles_2"));
                V_RECTANGLES(p, _p, w, rect);
                return p; }
            // 37 Radial Blur ( parametric )
            else if(type==37){
                vector2 radialblur;
                if(!ftype) radialblur = GMP.radialblur[idx];
                else  radialblur = chu(concat(PRX(ftype), "radialblur_2"));
                V_RADIALBLUR(p, _p, w, radialblur[0], radialblur[1]);
                return p; }
            // 38 PIE ( parametric )
            else if(type==38){
                vector pie;
                if(!ftype) pie = GMP.pie[idx];
                else  pie = chv(concat(PRX(ftype), "pie_2"));
                V_PIE(p, w, pie[0], pie[1], pie[2]);
                return p; }
            // 39 ARCH
            else if(type==39){
                V_ARCH(p, _p, w);
                return p; }
            // 40 TANGENT
            else if(type==40){
                V_TANGENT(p, _p, w);
                return p; }
            // 41 SQUARE
            else if(type==41){
                V_SQUARE(p, _p, w);
                return p; }
            // 42 RAYS
            else if(type==42){
                V_RAYS(p, _p, w);
                return p; }
            // 43 BLADE
            else if(type==43){
                V_BLADE(p, _p, w);
                return p; }
            // 44 SECANT2
            else if(type==44){
                V_SECANT2(p, _p, w);
                return p; }
            // 45 TWINTRIAN
            else if(type==45){
                V_TWINTRIAN(p, _p, w);
                return p; }
            // 46 CROSS
            else if(type==46){
                V_CROSS(p, _p, w);
                return p; }
            // 47 DISC2 ( parametric )
            else if(type==47){
                vector2 disc2;
                if(!ftype) disc2 = GMP.disc2[idx];
                else  disc2 = chu(concat(PRX(ftype), "disc2_2"));
                V_DISC2(p, _p, w, disc2[0], disc2[1]);
                return p; }
            // 48 SUPERSHAPE ( parametric )
            else if(type==48){
                vector ss, ss_n;
                if(!ftype){
                    ss   = GMP.supershape[idx];
                    ss_n = GMP.supershape_n[idx];
                }
                else{
                    ss   = chv(concat(PRX(ftype), "supershape_2"));
                    ss_n = chv(concat(PRX(ftype), "supershapen_2"));
                }
                V_SUPERSHAPE(p, _p, w, ss[1], ss[0], ss[2], ss_n);
                return p; }
            // 49 FLOWER ( parametric )
            else if(type==49){
                vector2 flower;
                if(!ftype) flower = GMP.flower[idx];
                else  flower = chu(concat(PRX(ftype), "flower_2"));
                V_FLOWER(p, _p, w, flower[0], flower[1]);
                return p; }
        }
        else{
            // 50 CONIC
            if(type==50){
                vector2 conic;
                if(!ftype) conic = GMP.conic[idx];
                else  conic =  chu(concat(PRX(ftype), "conic_2"));
                V_CONIC(p, _p, w, conic[0], conic[1]);
                return p; }
            // 51 PARABOLA ( parametric )
            else if(type==51){
                vector2 parabola;
                if(!ftype) parabola = GMP.parabola[idx];
                else  parabola = chu(concat(PRX(ftype), "parabola_2"));
                V_PARABOLA(p, _p, w, parabola[0], parabola[1]);
                return p; }
            // 52 BENT2 ( parametric )
            else if(type==52){
                vector2 bent2;
                if(!ftype) bent2 = GMP.bent2[idx];
                else  bent2 = chu(concat(PRX(ftype), "bent2xy_2"));
                V_BENT2(p, _p, w, bent2);
                return p; }
            // 53 BIPOLAR ( parametric )
            else if(type==53){
                float shift;
                if(!ftype) shift = GMP.bipolar_shift[idx];
                else  shift = chf(concat(PRX(ftype), "bipolarshift_2"));
                V_BIPOLAR(p, _p, w, shift);
                return p; }
            // 54 BOARDERS
            else if(type==54){
                V_BOARDERS(p, _p, w);
                return p; }
            // 55 BUTTERFLY
            else if(type==55){
                V_BUTTERFLY(p, _p, w);
                return p; }
            // 56 CELL ( parametric )
            else if(type==56){
                float size;
                if(!ftype) size = GMP.cell_size[idx];
                else  size = chf(concat(PRX(ftype), "cellsize_2"));
                V_CELL(p, _p, w, size);
                return p; }
            // 57 CPOW ( parametric )
            else if(type==57){
                vector cpow;
                if(!ftype) cpow = GMP.cpow[idx];
                else  cpow = chv(concat(PRX(ftype), "cpow_2"));
                V_CPOW(p, _p, w, cpow[0], cpow[1], cpow[2]);
                return p; }
            // 58 EDISC
            else if(type==58){
                V_EDISC(p, _p, w);
                return p; }
            // 59 ELLIPTIC
            else if(type==59){
                V_ELLIPTIC(p, _p, w);
                return p; }
            // 60 NOISE
            else if(type==60){
                V_NOISE(p, _p, w);
                return p; }
            // 61 ESCHER ( parametric )
            else if(type==61){
                float beta;
                if(!ftype) beta = GMP.escher_beta[idx];
                else  beta = chf(concat(PRX(ftype), "escherbeta_2"));
                V_ESCHER(p, _p, w, beta);
                return p; }
            // 62 FOCI
            else if(type==62){
                V_FOCI(p, _p, w);
                return p; }
            // 63 LAZYSUSAN ( parametric )
            else if(type==63){
                vector lazysusan;
                vector2 lazysusanxyz;
                if(!ftype){
                    lazysusanxyz  = GMP.lazysusanxyz[idx];
                    lazysusan     = GMP.lazysusan[idx];
                }
                else{
                    lazysusanxyz  = chu(concat(PRX(ftype), "lazysusanxyz_2"));
                    lazysusan     = chv(concat(PRX(ftype), "lazysusan_2"));
                }
                V_LAZYSUSAN(p, _p, w, lazysusan[0], lazysusan[1], lazysusan[2], lazysusanxyz);
                return p; }
            // 64 LOONIE
            else if(type==64){
                V_LOONIE(p, _p, w);
                return p; }
            // 65 PRE BLUR
            /*
            else if(type==65){
                V_PREBLUR(p, w);
                return p; }
            */
            // 66 MODULUS ( parametric )
            else if(type==66){
                vector2 mod;
                if(!ftype) mod = GMP.modulus[idx];
                else  mod = chu(concat(PRX(ftype), "modulusXYZ_2"));
                V_MODULUS(p, _p, w, mod);
                return p; }
            // 67 OSCOPE ( parametric )
            else if(type==67){
                vector4 oscope;
                if(!ftype) oscope = GMP.oscope[idx];
                else  oscope = chp(concat(PRX(ftype), "oscope_2"));
                V_OSCOPE(p, _p, w, oscope[0], oscope[1], oscope[2], oscope[3]);
                return p; }
            // 68 POLAR2
            else if(type==68){
                V_POLAR2(p, _p, w);
                return p; }
            // 69 POPCORN2 ( parametric )
            else if(type==69){
                float pop2c;
                vector2 pop2;
                if(!ftype){
                    pop2  = GMP.popcorn2[idx];
                    pop2c = GMP.popcorn2_c[idx];
                }
                else{
                    pop2  = chu(concat(PRX(ftype), "popcorn2xyz_2"));
                    pop2c = chf(concat(PRX(ftype), "popcorn2c_2"));
                }
                V_POPCORN2(p, _p, w, pop2c, pop2);
                return p; }
        }
    }
    else if(type<102){
        if(type<86){
            // 70 SCRY ( parametric )
            if(type==70){
                V_SCRY(p, _p, w);
                return p; }
            // 71 SEPARATION ( parametric )
            else if(type==71){
                vector2 sep, ins;
                if(!ftype){
                    sep = GMP.separation[idx];
                    ins = GMP.separation_inside[idx];
                }
                else{
                    sep = chu(concat(PRX(ftype), "separationxyz_2"));
                    ins = chu(concat(PRX(ftype), "separationinsidexyz_2"));
                }
                V_SEPARATION(p, _p, w, sep, ins);
                return p; }
            // 72 SPLIT ( parametric )
            else if(type==72){
                vector2 split;
                if(!ftype) split = GMP.split[idx];
                else  split = chu(concat(PRX(ftype), "splitxyz_2"));
                V_SPLIT(p, _p, w, split);
                return p; }
            // 73 SPLITS ( parametric )
            else if(type==73){
                vector2 splits;
                if(!ftype) splits = GMP.splits[idx];
                else  splits = chu(concat(PRX(ftype), "splitsxyz_2"));
                V_SPLITS(p, _p, w, splits);
                return p; }
            // 74 STRIPES ( parametric )
            else if(type==74){
                vector2 stripes;
                if(!ftype) stripes = GMP.stripes[idx];
                else  stripes = chu(concat(PRX(ftype), "stripes_2"));
                V_STRIPES(p, _p, w, stripes[0], stripes[1]);
                return p; }
            // 75 WEDGE ( parametric )
            else if(type==75){
                vector4 wedge;
                if(!ftype) wedge = GMP.wedge[idx];
                else  wedge = chp(concat(PRX(ftype), "wedge_2"));
                V_WEDGE(p, _p, w, wedge[0], wedge[1], wedge[2], wedge[3]);
                return p; }
            // 76 WEDGE JULIA ( parametric )
            else if(type==76){
                vector4 wedgejulia;
                if(!ftype) wedgejulia = GMP.wedgejulia[idx];
                else  wedgejulia = chp(concat(PRX(ftype), "wedgejulia_2"));
                V_WEDGEJULIA(p, _p, w, wedgejulia[0], wedgejulia[1], wedgejulia[2], wedgejulia[3]);
                return p; }
            // 77 WEDGE SPH ( parametric )
            else if(type==77){
                vector4 wedgesph;
                if(!ftype) wedgesph = GMP.wedgesph[idx];
                else  wedgesph = chp(concat(PRX(ftype), "wedgesph_2"));
                V_WEDGESPH(p, _p, w, wedgesph[0], wedgesph[1], wedgesph[2], wedgesph[3]);
                return p; }
            // 78 WHORL ( parametric )
            else if(type==78){
                vector2 whorl;
                if(!ftype) whorl  = GMP.whorl[idx];
                else  whorl  = chu(concat(PRX(ftype), "whorl_2"));
                V_WHORL(p, _p, w, whorl[0], whorl[1]);
                return p; }
            // 79 WAVES2 ( parametric )
            else if(type==79){
                vector2 scl, freq;
                if(!ftype){
                    scl  = GMP.waves2_scale[idx];
                    freq = GMP.waves2_freq[idx];
                }
                else{
                    scl  = chu(concat(PRX(ftype), "waves2scalexyz_2"));
                    freq = chu(concat(PRX(ftype), "waves2freqxyz_2"));
                }
                V_WAVES2(p, _p, w, scl, freq);
                return p; }
            // 80 COTHE EXP
            else if(type==80){
                V_COTHEEXP(p, _p, w);
                return p; }
            // 81 COTHE LOG
            else if(type==81){
                V_COTHELOG(p, _p, w);
                return p; }
            // 82 COTHE SIN
            else if(type==82){
                V_COTHESIN(p, _p, w);
                return p; }
            // 83 COTHE COS
            else if(type==83){
                V_COTHECOS(p, _p, w);
                return p; }
            // 84 COTHE TAN
            else if(type==84){
                V_COTHETAN(p, _p, w);
                return p; }
            // 85 COTHE SEC
            else if(type==85){
                V_COTHESEC(p, _p, w);
                return p; }
        }
        else{
            // 86 COTHE CSC
            if(type==86){
                V_COTHECSC(p, _p, w);
                return p; }
            // 87 COTHE COT
            else if(type==87){
                V_COTHECOT(p, _p, w);
                return p; }
            // 88 COTHE SINH
            else if(type==88){
                V_COTHESINH(p, _p, w);
                return p; }
            // 89 COTHE COSH
            else if(type==89){
                V_COTHECOSH(p, _p, w);
                return p; }
            // 90 COTHE TANH
            else if(type==90){
                V_COTHETANH(p, _p, w);
                return p; }
            // 91 COTHE SECH
            else if(type==91){
                V_COTHESECH(p, _p, w);
                return p; }
            // 92 COTHE CSCH
            else if(type==92){
                V_COTHECSCH(p, _p, w);
                return p; }
            // 93 COTHE COTH
            else if(type==93){
                V_COTHECOTH(p, _p, w);
                return p; }
            // 94 AUGER ( parametric )
            else if(type==94){
                vector4 auger;
                if(!ftype) auger = GMP.auger[idx];
                else  auger = chp(concat(PRX(ftype), "auger_2"));
                V_AUGER(p, _p, w, auger[0], auger[1], auger[2], auger[3]);
                return p; }
            // 95 FLUX ( parametric )
            else if(type==95){
                float spread;
                if(!ftype) spread = GMP.flux_spread[idx];
                else  spread = chf(concat(PRX(ftype), "fluxspread_2"));
                V_FLUX(p, _p, w, spread);
                return p; }
            // 96 MOBIUS ( parametric )
            else if(type==96){
                vector4 re, im;
                if(!ftype){
                    re = GMP.mobius_re[idx];
                    im = GMP.mobius_im[idx];
                }
                else{
                    re = chp(concat(PRX(ftype), "mobiusre_2"));
                    im = chp(concat(PRX(ftype), "mobiusim_2"));
                }
                V_MOBIUS(p, _p, w, re, im);
                return p; }
            // 97 CURVE ( parametric )
            else if(type==97){
                vector2 lgt, amp;
                if(!ftype){
                    lgt = GMP.curve_lenght[idx];
                    amp = GMP.curve_amp[idx];
                }
                else{
                    lgt = chu(concat(PRX(ftype), "curvexyzlenght_2"));
                    amp = chu(concat(PRX(ftype), "curvexyzamp_2"));
                }
                V_CURVE(p, _p, w, lgt, amp);
                return p; }
            // 98 PERSPECTIVE ( parametric )
            else if(type==98){
                vector2 persp;
                if(!ftype) persp = GMP.persp[idx];
                else  persp = chu(concat(PRX(ftype), "persp_2"));
                V_PERSPECTIVE(p, _p, w, persp[0], persp[1]);
                return p; }
            // 99 BWRAPS ( parametric )
            else if(type==99){
                vector bwraps;
                vector2 bwrapstwist;
                if(!ftype){
                    bwraps = GMP.bwraps[idx];
                    bwrapstwist = GMP.bwrapstwist[idx];
                }
                else{
                    bwraps = chv(concat(PRX(ftype), "bwraps_2"));
                    bwrapstwist = chu(concat(PRX(ftype), "bwrapstwist_2"));
                }
                V_BWRAPS(p, _p, w, bwraps[0], bwraps[1], bwraps[2], bwrapstwist[0], bwrapstwist[1]);
                return p; }
            // 100 HEMISPHERE
            else if(type==100){
                V_HEMISPHERE(p, _p, w);
                return p; }
            // 101 POLYNOMIAL ( parametric )
            else if(type==101){
                vector2 pow, lc, sc;
                if(!ftype){
                    pow = GMP.polynomial_pow[idx];
                    lc  = GMP.polynomial_lc[idx];
                    sc  = GMP.polynomial_sc[idx];
                }
                else{
                    pow = chu(concat(PRX(ftype), "polynomialpow_2"));
                    lc  = chu(concat(PRX(ftype), "polynomiallc_2"));
                    sc  = chu(concat(PRX(ftype), "polynomialsc_2"));
                }
                V_POLYNOMIAL(p, _p, w, pow, lc, sc);
                return p; }
        }
    }
    return _p;
}

#endif
