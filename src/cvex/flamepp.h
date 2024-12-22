#ifndef __flamepp_h__
#define __flamepp_h__

/*  
 /  Tested on:  Houdini 19.x
 /              Houdini 19.5
 /              Houdini 20.x
 /              Houdini 20.5
 /
 /  Title:      FLAM3H. SideFX Houdini FLAM3: 2D
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
 /  Name:       FLAMEPP "CVEX"
 /
 /  Comment:    THIS IS NOT USED ANYMORE: I'll leave it as it may come handy again.
 /
 /              FLAM3 variation selection. Only non parametrics.
 /              Type 65 PRE BLUR is missing as it is hardcoded into the chaose game,
 /              so there is a jump from 64 to 68 directly.
*/




vector2 FLAMEPP(const int T; const vector2 pos, x, y, o; const float w){

    //  p = out position
    // _p = incoming position
    vector2 p, _p; _p=pos;
    // pre affine are their identity matrix for pre/post variations.

    // VARs with precalc pos: 9, 10, 11, 19, 21

    // FLAME VARIATIONS
    //
    // 00 LINEAR
    if(!T) return _p*w;
    else if(T<21){
        if(T<11){
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
        }
        else{
            // 11 DIAMOND
            if(T==11){
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
            // 18 Exponential
            else if(T==18){
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
        }
    }
    else if(T<62){
        if(T<42){
            // *21 RINGS ( dependent )
            if(T==21){
                V_RINGS(p, _p, w, o[0]);
                return p; }
            // *22 FAN ( dependent )
            else if(T==22){
                V_FAN(p, _p, w, o[0]);
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
            // 33 Gaussian
            else if(T==33){
                V_GAUSSIAN_BLUR(p, w);
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
        }
        else{
            // 42 RAYS
            if(T==42){
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
            // 54 BOARDERS
            else if(T==54){
                V_BOARDERS(p, _p, w);
                return p; }
            // 55 BUTTERFLY
            else if(T==55){
                V_BUTTERFLY(p, _p, w);
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
        }
    }
    else if(T<101){
        if(T<86){
            // 62 FOCI
            if(T==62){
                V_FOCI(p, _p, w);
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
            // 68 POLAR2
            else if(T==68){
                V_POLAR2(p, _p, w);
                return p; }
            // 70 SCRY ( parametric )
            else if(T==70){
                V_SCRY(p, _p, w);
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
                V_SIN(p, _p, w);
                return p; }
            // 83 COTHE COS
            else if(T==83){
                V_COS(p, _p, w);
                return p; }
            // 84 COTHE TAN
            else if(T==84){
                V_TAN(p, _p, w);
                return p; }
            // 85 COTHE SEC
            else if(T==85){
                V_SEC(p, _p, w);
                return p; }
        }
        else{
            // 86 COTHE CSC
            if(T==86){
                V_CSC(p, _p, w);
                return p; }
            // 87 COTHE COT
            if(T==87){
                V_COT(p, _p, w);
                return p; }
            // 88 COTHE SINH
            else if(T==88){
                V_SINH(p, _p, w);
                return p; }
            // 89 COTHE COSH
            else if(T==89){
                V_COSH(p, _p, w);
                return p; }
            // 90 COTHE TANH
            else if(T==90){
                V_TANH(p, _p, w);
                return p; }
            // 91 COTHE SECH
            else if(T==91){
                V_SECH(p, _p, w);
                return p; }
            // 92 COTHE CSCH
            else if(T==92){
                V_CSCH(p, _p, w);
                return p; }
            // 93 COTHE COTH
            else if(T==93){
                V_COTH(p, _p, w);
                return p; }
            // 100 HEMISPHERE
            else if(T==100){
                V_HEMISPHERE(p, _p, w);
                return p; }
        }
    }
    return _p;
}

#endif
