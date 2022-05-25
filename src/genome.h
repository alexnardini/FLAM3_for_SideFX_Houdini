#ifndef __genome_h__
#define __genome_h__

/*  
 /  Title:      SideFX Houdini FLAM3: 2D
 /  Author:     Alessandro Nardini
 /  date:       October 2020, Last revised May 2022
 /
 /  info:       Based on the original: "The Fractal Flame Algorithm"
 /  Authors:    Scott Draves, Erik Reckase
 /  Weblink:    https://flam3.com/flame_draves.pdf
 /  Date:       September 2003, Last revised November 2008
 /
 /  Name:       FLAME GENOME   "CVEX"
 /
 /  Comment:    GENOME entities and properties.
*/


#include <functions.h>


// GENOME
struct gem{

    int     TM, FF, PFF, RIP, SYM, iter_f, iter, sym_mod, MB,
            res, v1type[], v2type[], v3type[], v4type[], p1type[], pp1type[], POSTL[], ffv1type, ffv2type, ffv3type, ffp1type;
    float   v1w[], v2w[], v3w[], v4w[], p1w[], pb1w[], pp1w[], CLR[], ONEMINUS[], ALPHA[], ffv1w, ffv2w, ffv3w, ffp1w;
    vector2 x[], y[], o[], px[], py[], po[], fx, fy, fo, pfx, pfy, pfo;
    matrix2 TMm2;
    string  sIDX[];

    float mb_mod = 1.0;
    
    void gemBuild(const int ACTV[]){

        // SYS
        TM     = chi("../dotmglobal");
        FF     = chi("../dofinalflame");
        PFF    = chi("../_dofpost_2");
        RIP    = chi("../delinvalidpt");
        SYM    = chi("../symmetry");
        iter_f = chi("../flamefunc");
        iter   = chi("../iter");
        MB     = chi("../domb");
        if(SYM) sym_mod = chi("../rotational");
        if(MB) mb_mod = detail(1, "Tstep_mult", 0);

        // GENOME
        res = 0;
        float _a, clr, speed;
        vector2 _x, _y;
        matrix2 _m2;
        for(int i=0; i<iter_f; ++i){
            if(!ACTV[i]) continue;
            res++;
            // Collect active variation IDs
            string IDX=itoa(i+1);
            append(sIDX, IDX);
            // Color
            clr = chf(concat("../clr_", IDX));
            speed = chf(concat("../clrspeed_", IDX));
            append(CLR, speed*clr);
            append(ONEMINUS, 1-speed);
            append(ALPHA, chf(concat("../alpha_", IDX)));
            // PRE BLUR
            append(pb1w, chf(concat("../preblurweight_" , IDX)));
            // PRE VAR 01
            append(pp1w, chf(concat("../pre1weight_" , IDX)));
            if(pp1w[-1]>0) append(pp1type, atoi(chs(concat("../pre1type_", IDX))));
            else resize(pp1type, res);
            // VAR 01
            append(v1w, chf(concat("../v1weight_", IDX)));
            if(v1w[-1]!=0) append(v1type, atoi(chs(concat("../v1type_", IDX))));
            else resize(v1type, res);
            // VAR 02
            append(v2w, chf(concat("../v2weight_", IDX)));
            if(v2w[-1]!=0) append(v2type, atoi(chs(concat("../v2type_", IDX))));
            else resize(v2type, res);
            // VAR 03
            append(v3w, chf(concat("../v3weight_", IDX)));
            if(v3w[-1]!=0) append(v3type, atoi(chs(concat("../v3type_", IDX))));
            else resize(v3type, res);
            // VAR 04
            append(v4w, chf(concat("../v4weight_", IDX)));
            if(v4w[-1]!=0) append(v4type, atoi(chs(concat("../v4type_", IDX))));
            else resize(v4type, res);
            // // POST VAR 01
            append(p1w, chf(concat("../p1weight_", IDX)));
            if(p1w[-1]!=0) append(p1type, atoi(chs(concat("../p1type_", IDX))));
            else resize(p1type, res);
            // Collect affine coefficients
            _x = chu(concat("../x_", IDX));
            _y = chu(concat("../y_", IDX));
            _a = chf(concat("../ang_", IDX));
            affineRot(_m2, _x, _y, -radians(_a));
            append(x, set(_m2.xx, _m2.xy));
            append(y, set(_m2.yx, _m2.yy));
            append(o, chu(concat("../o_", IDX)));
            // POST
            append(POSTL, chi(concat("../dopost_", IDX)));
            if(POSTL[-1]){
                _x = chu(concat("../px_", IDX));
                _y = chu(concat("../py_", IDX));
                _a = chf(concat("../pang_", IDX));
                affineRot(_m2, _x, _y, -radians(_a));
                append(px, set(_m2.xx, _m2.xy));
                append(py, set(_m2.yx, _m2.yy));
                append(po, chu(concat("../po_", IDX)));
                }
            else{ resize(px, res); resize(py, res); resize(po, res); }
        }
        // Build TM
        if(TM){
            float grt = chf("../frt");
            TMm2 = (matrix2)maketransform(0, set(0, 0, grt));
        }
        if(FF){
            // FF VAR 01
            ffv1w = chf("../ffv1weight");
            if(ffv1w!=0) ffv1type = chi("../ffv1type");
            // FF VAR 02
            ffv2w = chf("../ffv2weight");
            if(ffv2w!=0) ffv2type = chi("../ffv2type");
            // FF VAR 03
            ffv3w = chf("../ffv3weight");
            if(ffv3w!=0) ffv3type = chi("../ffv3type");
            // // FF POST VAR 01
            ffp1w = chf("../ffp1weight");
            if(ffp1w!=0) ffp1type = chi("../ffp1type");
            // Collect FINAL FLAME TRANSFORM affine coefficients
            _x = chu("../_fx_2");;
            _y = chu("../_fy_2");;
            _a = chf("../_ang_2");
            affineRot(_m2, _x, _y, -radians(_a));
            fx = set(_m2.xx, _m2.xy);
            fy = set(_m2.yx, _m2.yy);
            fo = chu("../_fo_2");
            // POST
            if(PFF){
                _x = chu("../_pfx_2");;
                _y = chu("../_pfy_2");;
                _a = chf("../_pang_2");
                affineRot(_m2, _x, _y, -radians(_a));
                pfx = set(_m2.xx, _m2.xy);
                pfy = set(_m2.yx, _m2.yy);
                pfo = chu("../_pfo_2");
            }
        }
    }
}


// GENOME PARAMETRICS
struct gemPrm{
    float   rings2_val[], bipolar_shift[], cell_size[], escher_beta[], popcorn2_c[], flux_spread[];
    vector  blob[], pie[], supershape[], supershape_n[], cpow[], lazysusan[], bwraps[];
    vector2 curl_c[], parabola[], fan2[], rectangles[], bent2[], lazysusanxyz[], modulus[], popcorn2[], separation[], separation_inside[], split[], splits[], waves2_scale[], waves2_freq[], curve_lenght[], curve_amp[], polynomial_pow[], polynomial_lc[], polynomial_sc[], julian[], juliascope[], radialblur[], disc2[], flower[], conic[], stripes[], whorl[], persp[], bwrapstwist[];
    vector4 ngon[], pdj_w[], oscope[], wedge[], wedgejulia[], wedgesph[], auger[], mobius_re[], mobius_im[];

    void gemPrmBuild(const string sIDX[]; const int res, GEMTYPE[]; const float w[]){

        if(max(GEMTYPE)>26){
            int TYPE;
            string IDX;
            // FLOAT
            resize(rings2_val, res); bipolar_shift=cell_size=escher_beta=popcorn2_c=flux_spread=rings2_val;
            // VECTOR
            resize(blob, res);       pie=supershape=supershape_n=cpow=lazysusan=blob;
            // VECTOR2
            resize(curl_c, res);     parabola=fan2=rectangles=bent2=lazysusanxyz=modulus=popcorn2=separation=separation_inside=split=splits=waves2_scale=waves2_freq=curve_lenght=curve_amp=polynomial_pow=polynomial_lc=polynomial_sc=julian=juliascope=radialblur=disc2=flower=conic=stripes=whorl=persp=bwrapstwist=curl_c;
            // VECTOR4
            resize(ngon, res);       pdj_w=oscope=wedge=wedgejulia=wedgesph=auger=mobius_re=mobius_im=ngon;

            for(int i=0; i<res; ++i){
                TYPE=GEMTYPE[i]; IDX=sIDX[i];
                if(TYPE<27 || w[i]==0) continue;
                else if(find( {27, 28, 29, 30, 31, 32, 34, 35, 36, 37, 38, 47, 48, 49, 50, 51, 52, 53, 56, 57} , TYPE)>=0){
                    if(TYPE<38){
                        // 27 CURL
                        if(TYPE==27){ curl_c[i] = chu(concat("../curlc_", IDX)); continue; }
                        // 28 NGON
                        else if(TYPE==28){ ngon[i]  = chp(concat("../ngon_", IDX)); continue; }
                        // 29 PDJ
                        else if(TYPE==29){ pdj_w[i] = chp(concat("../pdjw_", IDX)); continue; }
                        // 30 BLOB
                        else if(TYPE==30){ blob[i]  = chv(concat("../blob_", IDX)); continue; }
                        // 31 JuliaN
                        else if(TYPE==31){ julian[i] = chu(concat("../julian_", IDX)); continue; }
                        // 32 JuliaScope
                        else if(TYPE==32){ juliascope[i] = chu(concat("../juliascope_", IDX)); continue; }
                        // 34 FAN2
                        else if(TYPE==34){ fan2[i] = chu(concat("../fan2_", IDX)); continue; }
                        // 35 RINGS2
                        else if(TYPE==35){ rings2_val[i] = chf(concat("../rings2val_", IDX)); continue; }
                        // 36 RECTANGLES
                        else if(TYPE==36){ rectangles[i] = chu(concat("../rectangles_", IDX)); continue; }
                        // 37 RADIAL BLUR
                        else if(TYPE==37){ radialblur[i] = chu(concat("../radialblur_", IDX)); continue; }
                    }
                    else{
                        // 38 PIE
                        if(TYPE==38){ pie[i] = chv(concat("../pie_", IDX)); continue; }
                        // 47 DISC2
                        else if(TYPE==47){ disc2[i] = chu(concat("../disc2_", IDX)); continue; }
                        // 48 SUPERSHAPE
                        else if(TYPE==48){
                            supershape[i]   = chv(concat("../supershape_", IDX));
                            supershape_n[i] = chv(concat("../supershapen_", IDX)); continue; }
                        // 49 FLOWER
                        else if(TYPE==49){ flower[i] = chu(concat("../flower_", IDX)); continue; }
                        // 50 CONIC
                        else if(TYPE==50){ conic[i] = chu(concat("../conic_", IDX)); continue; }
                        // 51 PARABOLA
                        else if(TYPE==51){ parabola[i] = chu(concat("../parabola_", IDX)); continue; }
                        // 52 BENT2
                        else if(TYPE==52){ bent2[i] = chu(concat("../bent2xy_", IDX)); continue; }
                        // 53 BIPOLAR
                        else if(TYPE==53){ bipolar_shift[i] = chf(concat("../bipolarshift_", IDX)); continue; }
                        // 56 CELL
                        else if(TYPE==56){ cell_size[i] = chf(concat("../cellsize_", IDX)); continue; }
                        // 57 CPOW
                        else if(TYPE==57){ cpow[i] = chv(concat("../cpow_", IDX)); continue; }
                    }
                }
                else if(find( {61, 63, 66, 67, 69, 71, 72, 73, 74, 75, 76, 77, 78, 79, 94, 95, 96, 97, 98, 99, 101} , TYPE)>=0){
                    if(TYPE<77){
                        // 61 ESCHER
                        if(TYPE==61){ escher_beta[i] = chf(concat("../escherbeta_", IDX)); continue; }
                        // 63 LAZYSUSAN
                        else if(TYPE==63){
                            lazysusanxyz[i] = chu(concat("../lazysusanxyz_", IDX));
                            lazysusan[i]    = chv(concat("../lazysusan_", IDX)); continue; }
                        // 66 MODULUS
                        else if(TYPE==66){ modulus[i] = chu(concat("../modulusXYZ_", IDX)); continue; }
                        // 67 OSCOPE
                        else if(TYPE==67){ oscope[i] = chp(concat("../oscope_", IDX)); continue; }
                        // 69 POPCORN2
                        else if(TYPE==69){
                            popcorn2[i]   = chu(concat("../popcorn2xyz_", IDX));
                            popcorn2_c[i] = chf(concat("../popcorn2c_", IDX)); continue; }
                        // 71 SEPARATION
                        else if(TYPE==71){
                            separation[i]        = chu(concat("../separationxyz_", IDX));
                            separation_inside[i] = chu(concat("../separationinsidexyz_", IDX)); continue; }
                        // 72 SPLIT
                        else if(TYPE==72){ split[i] = chu(concat("../splitxyz_", IDX)); continue; }
                        // 73 SPLITS
                        else if(TYPE==73){ splits[i] = chu(concat("../splitsxyz_", IDX)); continue; }
                        // 74 STRIPES
                        else if(TYPE==74){ stripes[i] = chu(concat("../stripes_", IDX)); continue; }
                        // 75 WEDGE
                        else if(TYPE==75){ wedge[i] = chp(concat("../wedge_", IDX)); continue; }
                        // 76 WEDGE JULIA
                        else if(TYPE==76){ wedgejulia[i] = chp(concat("../wedgejulia_", IDX)); continue; }
                    }
                    else{
                        // 77 WEDGE SPH
                        if(TYPE==77){ wedgesph[i] = chp(concat("../wedgesph_", IDX)); continue; }
                        // 78 WHORL
                        else if(TYPE==78){ whorl[i]  = chu(concat("../whorl_", IDX)); continue; }
                        // 79 WAVES2
                        else if(TYPE==79){
                            waves2_scale[i] = chu(concat("../waves2scalexyz_", IDX));
                            waves2_freq[i]  = chu(concat("../waves2freqxyz_", IDX)); continue; }
                        // 94 AUGER
                        else if(TYPE==94){ auger[i] = chp(concat("../auger_", IDX)); continue; }
                        // 95 FLUX
                        else if(TYPE==95){ flux_spread[i] = chf(concat("../fluxspread_", IDX)); continue; }
                        // 96 MOBIUS
                        else if(TYPE==96){
                            mobius_re[i] = chp(concat("../mobiusre_", IDX));
                            mobius_im[i] = chp(concat("../mobiusim_", IDX)); continue; }
                        // 97 CURVE
                        else if(TYPE==97){
                            curve_lenght[i] = chu(concat("../curvexyzlenght_", IDX));
                            curve_amp[i]    = chu(concat("../curvexyzamp_", IDX)); continue; }
                        // 98 PERSPECTIVE
                        else if(TYPE==98){ persp[i] = chu(concat("../persp_", IDX)); continue; }
                        // 99 BWRAPS
                        else if(TYPE==99){
                            bwraps[i] = chv(concat("../bwraps_", IDX));
                            bwrapstwist[i] = chu(concat("../bwrapstwist_", IDX)); continue; }
                        // 101 POLYNOMIAL
                        else if(TYPE==101){
                            polynomial_pow[i] = chu(concat("../polynomialpow_", IDX));
                            polynomial_lc[i]  = chu(concat("../polynomiallc_", IDX));
                            polynomial_sc[i]  = chu(concat("../polynomialsc_", IDX)); continue; }
                    }
                }
            }
        }
    }
}

#endif
