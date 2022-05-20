#ifndef __flamepp_h__
#define __flamepp_h__

/*  
 /  Title:      SideFX Houdini FLAM3: 2D
 /  Author:     Alessandro Nardini
 /  date:       October 2020, Last revised December 2021
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


#include <variations.h>


vector2 FLAMEPP(const int type; const vector2 pos, x, y, o; const float w){

    //  p = out position
    // _p = incoming position
    vector2 p, _p; _p=pos;
    // VARs with precalc pos: 9, 10, 11, 19, 21, 30, 35

    // FLAME VARIATIONS
    //
    // 00 PREBLUR ( LINEAR removed from pre-variations, for now. )
    if(!type){ V_PREBLUR(_p, w); return _p; }
    else if(type<21){
        if(type<11){
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
        }
        else{
            // 11 DIAMOND
            if(type==11){
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
            // 18 Exponential
            else if(type==18){
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
        }
    }
    else if(type<62){
        if(type<42){
            // *21 RINGS ( dependent )
            if(type==21){
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
            // 33 Gaussian
            else if(type==33){
                V_GAUSSIAN(p, w);
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
        }
        else{
            // 42 RAYS
            if(type==42){
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
            // 54 BOARDERS
            else if(type==54){
                V_BOARDERS(p, _p, w);
                return p; }
            // 55 BUTTERFLY
            else if(type==55){
                V_BUTTERFLY(p, _p, w);
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
        }
    }
    else if(type<101){
        if(type<86){
            // 62 FOCI
            if(type==62){
                V_FOCI(p, _p, w);
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
            // 68 POLAR2
            else if(type==68){
                V_POLAR2(p, _p, w);
                return p; }
            // 70 SCRY ( parametric )
            else if(type==70){
                V_SCRY(p, _p, w);
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
            if(type==87){
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
            // 100 HEMISPHERE
            else if(type==100){
                V_HEMISPHERE(p, _p, w);
                return p; }
        }
    }
    return _p;
}

#endif
