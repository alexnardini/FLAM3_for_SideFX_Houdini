#ifndef __genome_h__
#define __genome_h__

/*  
 /  Tested on:  Houdini 19.x
 /              Houdini 19.5
 /              Houdini 20.x
 /              Houdini 20.5
 /
 /  Title:      FLAM3H. SideFX Houdini FLAM3: 2D
 /  Author:     Alessandro Nardini
 /  date:       October 2020, Last revised December 2024
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
 /  Name:       GENOME "CVEX"
 /
 /  Comment:    Genome entities and properties.
*/



// GENOME: SYSTEM (GLOBAL)
struct gemSYSGLB{

    int FF, RIP, MB, F3C, ITER;

    void gemSYSGLBBuild(){
    
        FF = detail(-1, "FF");
        RIP = detail(-1, "RIP");
        MB = detail(-1, "MB");
        F3C = detail(-1, "F3C");
        ITER = detail(-1, "ITER");
    }
}



// GENOME: SYS (XAOS)
struct gemSYS{

    int RES, XS;
    float IW[], XST[];

    void gemSYSBuild(){
    
        RES = detail(-2, "RES");

        IW = detail(-3, "IW");
        XS = detail(-3, "XS");
        XST = detail(-3, "XST");
    }
}



// GENOME: SHADER
struct gemSHD{

    float   CLR[], OM[], A[];
    
    void gemSHDBuild(){

        // SHADER
        A = detail(-4, "A");
        CLR = detail(-4, "CLR");
        OM = detail(-4, "OM");

    }
}



// GENOME: PRE VAR
struct gemPV{

    int     p1t[], p2t[];
    float   pbw[], p1w[], p2w[];
    
    void gemPVBuild(){

        // VARS TYPE
        p1t = detail(-5, "p1t");
        p2t = detail(-5, "p2t");
        // VARS WEIGHT
        pbw = detail(-5, "pbw");
        p1w = detail(-5, "p1w");
        p2w = detail(-5, "p2w");
    }
}



// GENOME: VAR
struct gemV{

    int     v1t[], v2t[], v3t[], v4t[];
    float   v1w[], v2w[], v3w[], v4w[];
    
    void gemVBuild(){

        // VARS TYPE
        v1t = detail(-6, "v1t");
        v2t = detail(-6, "v2t");
        v3t = detail(-6, "v3t");
        v4t = detail(-6, "v4t");
        // VARS WEIGHT
        v1w = detail(-6, "v1w");
        v2w = detail(-6, "v2w");
        v3w = detail(-6, "v3w");
        v4w = detail(-6, "v4w");
    }
}



// GENOME: POST VAR
struct gemVP{

    int     PPL[], P1t[];
    float   P1w[];
    
    void gemVPBuild(){

        // VARS TYPE
        P1t = detail(-7, "P1t");
        // VARS WEIGHT
        P1w = detail(-7, "P1w");
    }
}



// GENOME: PRE AFFINE
struct gemPA{

    vector2 x[], y[], o[];
    
    void gemPABuild(){

        // PRE AFFINE
        x = detail(-8, "X");
        y = detail(-8, "Y");
        o = detail(-8, "O");

    }
}



// GENOME: POST AFFINE
struct gemAP{

    int PPL[];
    vector2 px[], py[], po[];
    
    void gemAPBuild(){

        // POST AFFINE
        PPL = detail(-9, "POST");
        px = detail(-9, "PX");
        py = detail(-9, "PY");
        po = detail(-9, "PO");

    }
}



// GENOME: FF PRE VAR
struct gemFFPV{

    int fp1t;
    float fp1w;
    
    void gemFFPVBuild(){

        // FF VARS TYPE
        fp1t = detail(-10, "fp1t");
        // FF VARS WEIGHT
        fp1w = detail(-10, "fp1w");
    }
}



// GENOME: FF VAR
struct gemFFV{

    int fv1t, fv2t;
    float fv1w, fv2w;
    
    void gemFFVBuild(){

        // FF VARS TYPE
        fv1t = detail(-11, "fv1t");
        fv2t = detail(-11, "fv2t");
        // FF VARS WEIGHT
        fv1w = detail(-11, "fv1w");
        fv2w = detail(-11, "fv2w");
    }
}



// GENOME: FF POST VAR
struct gemFFVP{

    int fP1t, fP2t;
    float fP1w, fP2w;
    
    void gemFFVPBuild(){

        // FF VARS TYPE
        fP1t = detail(-12, "fP1t");
        fP2t = detail(-12, "fP2t");
        // FF VARS WEIGHT
        fP1w = detail(-12, "fP1w");
        fP2w = detail(-12, "fP2w");
    }
}



// GENOME: FF PRE AFFINE
struct gemFFPA{

    vector2 fx, fy, fo;
    
    void gemFFPABuild(){

        // FF PRE AFFINE
        fx = detail(-13, "FX"); 
        fy = detail(-13, "FY");
        fo = detail(-13, "FO");

    }
}



// GENOME: FF POST AFFINE
struct gemFFAP{

    int PFF;
    vector2 pfx, pfy, pfo;
    
    void gemFFAPBuild(){

        // FF POST AFFINE
        PFF = detail(-14, "PFF");
        pfx = detail(-14, "PFX");
        pfy = detail(-14, "PFY");
        pfo = detail(-14, "PFO");
    }
}


/* GENOME PARAMETRICS
 /
 / THIS IS NOT USED ANYMORE
 / It has been substituted in favor of wrangle cores nodes for each parametric variation' parameters set.
 / While this was actually working great and added very little to the computation, the interactivity of the tool suffered
 / as this data structure needed to alway be built ahead of time for the current point/sample to be processed.
 /
 / Now, using details wrangle cores nodes, the point/sample can just grab a subset of this data only when it needs it without building and storing it first.
 / I leave this code here for reference as well as the associated (commented) code inside the file: "flame.h" to complete this reference.
 /
*/ 

struct gemPrm{

    float   rings2_val[], bipolar_shift[], cell_size[], radialblur[], escher_beta[], popcorn2_c[], flux_spread[];
    vector  blob[], pie[], supershape[], supershape_n[], cpow[], lazysusan[], bwraps[], point_symmetry[];
    vector2 curl_c[], parabola[], fan2[], rectangles[], bent2[], lazysusanxyz[], modulus[], popcorn2[], separation[], separation_inside[], split[], splits[], waves2_scale[], waves2_freq[], curve_lenght[], curve_amp[], polynomial_pow[], polynomial_lc[], polynomial_sc[], julian[], juliascope[], disc2[], flower[], conic[], stripes[], whorl[], persp[], bwrapstwist[], crop_az[];
    vector4 ngon[], pdj_w[], oscope[], wedge[], wedgejulia[], wedgesph[], auger[], mobius_re[], mobius_im[], crop_ltrb[];
    vector  pc_DISC2[]; // pc_BWRAPS[], pc_WEDGEJULIA[];

    void gemPrmBuild(const string sIDX[]; const int res, TYPE[]; const float w[]){

        if(max(TYPE)>26){
            
            int T;
            string idx;

            for(int i=0; i<res; ++i){
                
                T=TYPE[i]; idx=sIDX[i];
                if(T<27 || w[i]==0) continue;
                else if(find( {27, 28, 29, 30, 31, 32, 34, 35, 36, 37, 38, 47, 48, 49, 50, 51, 52, 53, 56, 57, 61, 63} , T )>=0){
                    if(T<39){
                        // 27 CURL
                        if(T==27){ curl_c[i] = chu(concat("../curlc_", idx)); continue; }
                        // 28 NGON
                        else if(T==28){ ngon[i]  = chp(concat("../ngon_", idx)); continue; }
                        // 29 PDJ
                        else if(T==29){ pdj_w[i] = chp(concat("../pdjw_", idx)); continue; }
                        // 30 BLOB
                        else if(T==30){ blob[i]  = chv(concat("../blob_", idx)); continue; }
                        // 31 JuliaN
                        else if(T==31){ julian[i] = chu(concat("../julian_", idx)); continue; }
                        // 32 JuliaScope
                        else if(T==32){ juliascope[i] = chu(concat("../juliascope_", idx)); continue; }
                        // 34 FAN2
                        else if(T==34){ fan2[i] = chu(concat("../fan2_", idx)); continue; }
                        // 35 RINGS2
                        else if(T==35){ rings2_val[i] = chf(concat("../rings2val_", idx)); continue; }
                        // 36 RECTANGLES
                        else if(T==36){ rectangles[i] = chu(concat("../rectangles_", idx)); continue; }
                        // 37 RADIAL BLUR
                        else if(T==37){ radialblur[i] = chf(concat("../radialblur_", idx)); continue; }
                        // 38 PIE
                        else if(T==38){ pie[i] = chv(concat("../pie_", idx)); continue; }
                    }
                    else{
                        // 47 DISC2
                        if(T==47){
                            //( This seem to be the only one to benefit from the precalc: 18% faster. )
                            disc2[i] = chu(concat("../disc2_", idx));
                            float rot=disc2[i][0]; float twist=disc2[i][1];
                            vector calc; precalc_V_DISC2(calc, rot, twist);
                            pc_DISC2[i] = calc;
                            continue; }
                        // 48 SUPERSHAPE
                        else if(T==48){
                            supershape[i]   = chv(concat("../supershape_", idx));
                            supershape_n[i] = chv(concat("../supershapen_", idx)); continue; }
                        // 49 FLOWER
                        else if(T==49){ flower[i] = chu(concat("../flower_", idx)); continue; }
                        // 50 CONIC
                        else if(T==50){ conic[i] = chu(concat("../conic_", idx)); continue; }
                        // 51 PARABOLA
                        else if(T==51){ parabola[i] = chu(concat("../parabola_", idx)); continue; }
                        // 52 BENT2
                        else if(T==52){ bent2[i] = chu(concat("../bent2xy_", idx)); continue; }
                        // 53 BIPOLAR
                        else if(T==53){ bipolar_shift[i] = chf(concat("../bipolarshift_", idx)); continue; }
                        // 56 CELL
                        else if(T==56){ cell_size[i] = chf(concat("../cellsize_", idx)); continue; }
                        // 57 CPOW
                        else if(T==57){ cpow[i] = chv(concat("../cpow_", idx)); continue; }
                        // 61 ESCHER
                        else if(T==61){ escher_beta[i] = chf(concat("../escherbeta_", idx)); continue; }
                        // 63 LAZYSUSAN
                        else if(T==63){
                            lazysusanxyz[i] = chu(concat("../lazysusanxyz_", idx));
                            lazysusan[i]    = chv(concat("../lazysusan_", idx)); continue; }
                    }
                }
                else if(find( {66, 67, 69, 71, 72, 73, 74, 75, 76, 77, 78, 79, 94, 95, 96, 97, 98, 99, 101, 102, 103, 105} , T )>=0){
                    if(T<79){
                        // 66 MODULUS
                        if(T==66){ modulus[i] = chu(concat("../modulusXYZ_", idx)); continue; }
                        // 67 OSCOPE
                        else if(T==67){ oscope[i] = chp(concat("../oscope_", idx)); continue; }
                        // 69 POPCORN2
                        else if(T==69){
                            popcorn2[i]   = chu(concat("../popcorn2xyz_", idx));
                            popcorn2_c[i] = chf(concat("../popcorn2c_", idx)); continue; }
                        // 71 SEPARATION
                        else if(T==71){
                            separation[i]        = chu(concat("../separationxyz_", idx));
                            separation_inside[i] = chu(concat("../separationinsidexyz_", idx)); continue; }
                        // 72 SPLIT
                        else if(T==72){ split[i] = chu(concat("../splitxyz_", idx)); continue; }
                        // 73 SPLITS
                        else if(T==73){ splits[i] = chu(concat("../splitsxyz_", idx)); continue; }
                        // 74 STRIPES
                        else if(T==74){ stripes[i] = chu(concat("../stripes_", idx)); continue; }
                        // 75 WEDGE
                        else if(T==75){ wedge[i] = chp(concat("../wedge_", idx)); continue; }
                        // 76 WEDGE JULIA
                        else if(T==76){ wedgejulia[i] = chp(concat("../wedgejulia_", idx));
                            // precalc ( The precalc made it 10% slower, I dnt know why...odd. )
                            // float power=wedgejulia[i][0]; float angle= wedgejulia[i][1]; float dist=wedgejulia[i][2]; float count=wedgejulia[i][3];
                            // vector calc; precalc_V_WEDGEJULIA(calc, power, angle, dist, count);
                            // pc_WEDGEJULIA[i] = calc;
                            continue; }
                        // 77 WEDGE SPH
                        else if(T==77){ wedgesph[i] = chp(concat("../wedgesph_", idx)); continue; }
                        // 78 WHORL
                        else if(T==78){ whorl[i]  = chu(concat("../whorl_", idx)); continue; }
                    }
                    else{
                        // 79 WAVES2
                        if(T==79){
                            waves2_scale[i] = chu(concat("../waves2scalexyz_", idx));
                            waves2_freq[i]  = chu(concat("../waves2freqxyz_", idx)); continue; }
                        // 94 AUGER
                        else if(T==94){ auger[i] = chp(concat("../auger_", idx)); continue; }
                        // 95 FLUX
                        else if(T==95){ flux_spread[i] = chf(concat("../fluxspread_", idx)); continue; }
                        // 96 MOBIUS
                        else if(T==96){
                            mobius_re[i] = chp(concat("../mobiusre_", idx));
                            mobius_im[i] = chp(concat("../mobiusim_", idx)); continue; }
                        // 97 CURVE
                        else if(T==97){
                            curve_lenght[i] = chu(concat("../curvexyzlenght_", idx));
                            curve_amp[i]    = chu(concat("../curvexyzamp_", idx)); continue; }
                        // 98 PERSPECTIVE
                        else if(T==98){ persp[i] = chu(concat("../persp_", idx)); continue; }
                        // 99 BWRAPS
                        else if(T==99){
                            bwraps[i] = chv(concat("../bwraps_", idx));
                            bwrapstwist[i] = chu(concat("../bwrapstwist_", idx));
                            // precalc ( The precalc made it 15% slower, I dnt know why...odd. )
                            // float cellsize=bwraps[i][0]; float space=bwraps[i][1]; float gain=bwraps[i][2];
                            // vector calc; precalc_V_BWRAPS(calc, cellsize, space, gain);
                            // pc_BWRAPS[i] = calc;
                            continue; }
                        // 101 POLYNOMIAL
                        else if(T==101){
                            polynomial_pow[i] = chu(concat("../polynomialpow_", idx));
                            polynomial_lc[i]  = chu(concat("../polynomiallc_", idx));
                            polynomial_sc[i]  = chu(concat("../polynomialsc_", idx)); continue; }
                        // 102 CROP
                        else if(T==102){
                            crop_ltrb[i] = chp(concat("../cropltrb_", idx));
                            crop_az[i] = chu(concat("../cropaz_", idx)); continue; }
                        // 105 POINT SYMMETRY
                        else if(T==105){ point_symmetry[i] = chv(concat("../ptsym_", idx)); continue; }
                    }
                }
            }
        }
    }
}


#endif
