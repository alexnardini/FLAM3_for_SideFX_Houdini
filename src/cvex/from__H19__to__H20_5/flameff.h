#ifndef __flameff_h__
#define __flameff_h__

/*  
 /  Tested on:  Houdini 19.x
 /              Houdini 19.5
 /              Houdini 20.x
 /              Houdini 20.5
 /
 /  Title:      FLAM3H. SideFX Houdini FLAM3: 2D
 /  Author:     Alessandro Nardini
 /  date:       October 2020, Last revised April 2025
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
 /  Name:       FLAMEFF "CVEX"
 /
 /  Comment:    FF FLAM3 variation selection.
 /              Type 65 PRE BLUR is missing as it is hardcoded into the chaose game,
 /              so there is a jump from 64 to 66 directly.
*/


/*
    Parametrics parms list:

    NAME            PARMS

    CURL            -> c1, c2
    NGON            -> pow, sides, corners, circle
    PDJ             -> wA, wB, wC, wD
    BLOB            -> low, high, wave
    JULIAN          -> power, distance
    JULIASCOPE      -> power, distance
    FAN2            -> x, y
    RINGS2          -> value
    RECTANGLES      -> x, y
    RADIALBLUR      -> angle
    PIE             -> slices, thickness, rotation
    DISC2           -> (rot, twist), (timespi, sinadd, cosadd)
    SUPERSHAPE      -> (m, rnd, holes), (n1, n2, n3)
    FLOWER          -> petals, holes
    CONIC           -> eccentricity, holes
    PARABOLA        -> height, width
    BENT2           -> x, y
    BIPOLAR         -> shift
    CELL            -> size
    CPOW            -> power, r, i
    ESCHER          -> beta
    LAZYSUSAN       -> (spin, twist, space), (x, y)
    MODULUS         -> x, y
    OSCOPE          -> frequency, amplitude, damping, separation
    POPCORN2        -> x, y, c
    SEPARATION      -> (x, y), (inside_x, inside_y)
    SPLIT           -> x, y
    SPLITS          -> x, y
    STRIPES         -> space, warp
    WEDGE           -> swirl, angle, hole, count
    WEDGEJULIAN     -> power, angle, dist, count
    WEDGESPH        -> swirl, angle, hole, count
    WHORL           -> inside, outside
    WAVES2          -> (scale_x, scale_y), (frequency_x,  frequency_y)
    AUGER           -> frequency, scale, symmetry, weight
    FLUX            -> spread
    MOBIUS          -> (reA, reB, reC, reD), (imA, imB, imC, imD)
    CURVE           -> (lenght_x, lenght_y), (amplitude_x, amplitude_y)
    PERSPECTIVE     -> angle, distance
    BWRAPS          -> (size, space, gain), (in_twist, out_twist)
    POLYNOMIAL      -> (pow_x, pow_y), (Lc_x, Lc_y), (Sc_x, Sc_y)
    CROP            -> (left, top, right, bottom), (area, zero)
    POINT_SYMMETRY  -> order, center_x, center_y
*/



// From Fractorium: flam3 comptibility (f3c). Check inside variations.h to see both versions of each.
// The behavior of the:
// cos, cosh, cot, coth, csc, csch, sec, sech, sin, sinh, tan and tanh variations
// are different in flam3/Apophysis versus Chaotica.
//      Checked:    use the Apophysis behavior.
//      Unchecked:  use the Chaotica behavior.
vector2 FLAMEFF(const string prx; const int T, f3c; const vector2 pos, x, y, o; const float w){

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
                V_WAVES(p, _p, w, y[0], o[0], y[1], o[1]);
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
                vector2 curl_c = chu(concat(prx, "curlc"));
                V_CURL(p, _p, w, curl_c);
                return p; }
            // 28 NGON ( parametric )
            else if(T==28){
                vector4 ngon = chp(concat(prx, "ngon"));
                V_NGON(p, _p, w, ngon);
                return p; }
            // 29 PDJ ( parametric )
            else if(T==29){
                vector4 pp = chp(concat(prx, "pdjw"));
                V_PDJ(p, _p, w, pp);
                return p; }
            // 30 BLOB ( parametric )
            else if(T==30){
                vector blob = chv(concat(prx, "blob"));
                V_BLOB(p, _p, w, blob);
                return p; }
            // 31 JuliaN ( parametric )
            else if(T==31){
                vector2 julian = chu(concat(prx, "julian"));
                V_JULIAN(p, _p, w, julian);
                return p; }
            // 32 JuliaScope ( parametric )
            else if(T==32){
                vector2 juliascope = chu(concat(prx, "juliascope"));
                V_JULIASCOPE(p, _p, w, juliascope);
                return p; }
            // 33 Gaussian
            else if(T==33){
                V_GAUSSIAN_BLUR(p, w);
                return p; }
            // 34 Fan2 ( parametric )
            else if(T==34){
                vector2 fan2 = chu(concat(prx, "fan2"));
                V_FAN2(p, _p, w, fan2);
                return p; }
        }
    }
    else if(T<70){
        if(T<52){
            // 35 Rings2 ( parametric )
            if(T==35){
                float rings2val = chf(concat(prx, "rings2val"));
                V_RINGS2(p, _p, w, rings2val);
                return p; }
            // 36 Rectangles ( parametric )
            else if(T==36){
                vector2 rect = chu(concat(prx, "rectangles"));
                V_RECTANGLES(p, _p, w, rect);
                return p; }
            // 37 Radial Blur ( parametric )
            else if(T==37){
                float radialblur = chf(concat(prx, "radialblur"));
                V_RADIALBLUR(p, _p, w, radialblur);
                return p; }
            // 38 PIE ( parametric )
            else if(T==38){
                vector pie = chv(concat(prx, "pie"));
                V_PIE(p, w, pie);
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
                vector2 disc2 = chu(concat(prx, "disc2"));
                V_DISC2_FF(p, _p, w, disc2);
                return p; }
            // 48 SUPERSHAPE ( parametric )
            else if(T==48){
                vector ss, ss_n;
                ss = chv(concat(prx, "supershape"));
                ss_n = chv(concat(prx, "supershapen"));
                V_SUPERSHAPE(p, _p, w, ss, ss_n);
                return p; }
            // 49 FLOWER ( parametric )
            else if(T==49){
                vector2 flower = chu(concat(prx, "flower"));
                V_FLOWER(p, _p, w, flower);
                return p; }
            // 50 CONIC ( parametric )
            else if(T==50){
                vector2 conic =  chu(concat(prx, "conic"));
                V_CONIC(p, _p, w, conic);
                return p; }
            // 51 PARABOLA ( parametric )
            else if(T==51){
                vector2 parabola = chu(concat(prx, "parabola"));
                V_PARABOLA(p, _p, w, parabola);
                return p; }
        }
        else{
            // 52 BENT2 ( parametric )
            if(T==52){
                vector2 bent2 = chu(concat(prx, "bent2xy"));
                V_BENT2(p, _p, w, bent2);
                return p; }
            // 53 BIPOLAR ( parametric )
            else if(T==53){
                float shift = chf(concat(prx, "bipolarshift"));
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
                float size = chf(concat(prx, "cellsize"));
                V_CELL(p, _p, w, size);
                return p; }
            // 57 CPOW ( parametric )
            else if(T==57){
                vector cpow = chv(concat(prx, "cpow"));
                V_CPOW(p, _p, w, cpow);
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
                float beta = chf(concat(prx, "escherbeta"));
                V_ESCHER(p, _p, w, beta);
                return p; }
            // 62 FOCI
            else if(T==62){
                V_FOCI(p, _p, w);
                return p; }
            // 63 LAZYSUSAN ( parametric )
            else if(T==63){
                vector lazysusan = chv(concat(prx, "lazysusan"));
                vector2 lazysusanxyz = chu(concat(prx, "lazysusanxyz"));
                V_LAZYSUSAN(p, _p, w, lazysusan, lazysusanxyz);
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
                vector2 mod = chu(concat(prx, "modulusXYZ"));
                V_MODULUS(p, _p, w, mod);
                return p; }
            // 67 OSCOPE ( parametric )
            else if(T==67){
                vector4 oscope = chp(concat(prx, "oscope"));
                V_OSCOPE(p, _p, w, oscope);
                return p; }
            // 68 POLAR2
            else if(T==68){
                V_POLAR2(p, _p, w);
                return p; }
            // 69 POPCORN2 ( parametric )
            else if(T==69){
                float pop2c = chf(concat(prx, "popcorn2c"));
                vector2 pop2 = chu(concat(prx, "popcorn2xyz"));
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
                sep = chu(concat(prx, "separationxyz"));
                ins = chu(concat(prx, "separationinsidexyz"));
                V_SEPARATION(p, _p, w, sep, ins);
                return p; }
            // 72 SPLIT ( parametric )
            else if(T==72){
                vector2 split = chu(concat(prx, "splitxyz"));
                V_SPLIT(p, _p, w, split);
                return p; }
            // 73 SPLITS ( parametric )
            else if(T==73){
                vector2 splits = chu(concat(prx, "splitsxyz"));
                V_SPLITS(p, _p, w, splits);
                return p; }
            // 74 STRIPES ( parametric )
            else if(T==74){
                vector2 stripes = chu(concat(prx, "stripes"));
                V_STRIPES(p, _p, w, stripes);
                return p; }
            // 75 WEDGE ( parametric )
            else if(T==75){
                vector4 wedge = chp(concat(prx, "wedge"));
                V_WEDGE(p, _p, w, wedge);
                return p; }
            // 76 WEDGE JULIA ( parametric )
            else if(T==76){
                vector4 wedgejulia = chp(concat(prx, "wedgejulia"));
                V_WEDGEJULIA(p, _p, w, wedgejulia);
                return p; }
            // 77 WEDGE SPH ( parametric )
            else if(T==77){
                vector4 wedgesph = chp(concat(prx, "wedgesph"));
                V_WEDGESPH(p, _p, w, wedgesph);
                return p; }
            // 78 WHORL ( parametric )
            else if(T==78){
                vector2 whorl = chu(concat(prx, "whorl"));
                V_WHORL(p, _p, w, whorl);
                return p; }
            // 79 WAVES2 ( parametric )
            else if(T==79){
                vector2 scl, freq;
                scl = chu(concat(prx, "waves2scalexyz"));
                freq = chu(concat(prx, "waves2freqxyz"));
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
            else if(T==87){
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
                vector4 auger = chp(concat(prx, "auger"));
                V_AUGER(p, _p, w, auger);
                return p; }
            // 95 FLUX ( parametric )
            else if(T==95){
                float spread = chf(concat(prx, "fluxspread"));
                V_FLUX(p, _p, w, spread);
                return p; }
            // 96 MOBIUS ( parametric )
            else if(T==96){
                vector4 re, im;
                re = chp(concat(prx, "mobiusre"));
                im = chp(concat(prx, "mobiusim"));
                V_MOBIUS(p, _p, w, re, im);
                return p; }
            // 97 CURVE ( parametric )
            else if(T==97){
                vector2 lgt, amp;
                lgt = chu(concat(prx, "curvexyzlenght"));
                amp = chu(concat(prx, "curvexyzamp"));
                V_CURVE(p, _p, w, lgt, amp);
                return p; }
            // 98 PERSPECTIVE ( parametric )
            else if(T==98){
                vector2 persp = chu(concat(prx, "persp"));
                V_PERSPECTIVE(p, _p, w, persp);
                return p; }
            // 99 BWRAPS ( parametric )
            else if(T==99){
                vector bwraps = chv(concat(prx, "bwraps"));
                vector2 bwrapstwist = chu(concat(prx, "bwrapstwist"));
                V_BWRAPS(p, _p, w, bwraps, bwrapstwist);
                return p; }
            // 100 HEMISPHERE
            else if(T==100){
                V_HEMISPHERE(p, _p, w);
                return p; }
            // 101 POLYNOMIAL ( parametric )
            else if(T==101){
                vector2 pow, lc, sc;
                pow = chu(concat(prx, "polynomialpow"));
                lc = chu(concat(prx, "polynomiallc"));
                sc = chu(concat(prx, "polynomialsc"));
                V_POLYNOMIAL(p, _p, w, pow, lc, sc);
                return p; }
            // 102 CROP ( parametric )
            else if(T==102){
                vector4 ltrb = chp(concat(prx, "cropltrb"));
                vector2 az = chu(concat(prx, "cropaz"));
                V_CROP(p, _p, w, ltrb, az);
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
                vector ptsym = chv(concat(prx, "ptsym"));
                V_POINT_SYMMETRY(p, _p, w, ptsym);
                return p; }
        }
    }
    return _p;
}

#endif
