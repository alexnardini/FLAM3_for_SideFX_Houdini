#ifndef __genome_h__
#define __genome_h__

/*  
 /  Title:      SideFX Houdini FLAM3: 2D
 /  Author:     Alessandro Nardini
 /  date:       October 2020, Last revised February 2023
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


#include <functions.h>


// GENOME
struct gem{

    int     PFF, res, v1t[], v2t[], v3t[], v4t[], p1t[], p2t[], P1t[], PPL[], fv1t, fv2t, fv3t, fp1t, fp2t;
    float   v1w[], v2w[], v3w[], v4w[], pbw[], p1w[], p2w[], P1w[], CLR[], OM[], A[], fv1w, fv2w, fv3w, fp1w, fp2w;
    vector2 x[], y[], o[], px[], py[], po[], fx, fy, fo, pfx, pfy, pfo;
    matrix2 TMm2;
    
    void gemBuild(const string sIDX[]; const int TM, FF){

        // GENOME
        res = len(sIDX);
        resize(v1t, res); v2t=v3t=v4t=p1t=p2t=P1t=PPL=v1t;
        resize(v1w, res); v2w=v3w=v4w=p1w=p2w=P1w=pbw=CLR=OM=A=v1w;
        resize(x,   res); y=o=px=py=po=x;

        float   _a, clr, spd, grt;
        vector2 _x, _y;
        matrix2 _m2;
        string  idx;
        
        for(int i=0; i<res; ++i){

            idx=sIDX[i];
            // SHADER
            clr = chf(concat("../clr_", idx));
            spd = chf(concat("../clrspeed_", idx));
            /*
                From Fractorium->Source->ember->Xform.h ( code line: 561)

                m_OneMinusColorCache = (1 + m_ColorSpeed) / 2;
                m_ColorSpeedCache = m_ColorX * (1 - m_ColorSpeed) / 2; //Apo style.

                m_OneMinusColorCache = static_cast<T>(1) - m_ColorSpeed;
                m_ColorSpeedCache = m_ColorSpeed * m_ColorX;//Flam3 style.
            */
            CLR[i] = clr * (1.0-spd)/2.0;
            OM[i]  = (1.0 + spd)/2.0;
            A[i]   = chf(concat("../alpha_", idx));
            // PRE BLUR
            pbw[i] = chf(concat("../preblurweight_" , idx));
            // PRE VAR 01
            p1w[i] = chf(concat("../pre1weight_" , idx));
            if(p1w[i] >0) p1t[i]=atoi(chs(concat("../pre1type_", idx)));
            // PRE VAR 02
            p2w[i] = chf(concat("../pre2weight_", idx));
            if(p2w[i] >0) p2t[i]=atoi(chs(concat("../pre2type_", idx)));
            // VAR 01
            v1w[i] = chf(concat("../v1weight_", idx));
            if(v1w[i]!=0) v1t[i]=atoi(chs(concat("../v1type_", idx)));
            // VAR 02
            v2w[i] = chf(concat("../v2weight_", idx));
            if(v2w[i]!=0) v2t[i]=atoi(chs(concat("../v2type_", idx)));
            // VAR 03
            v3w[i] = chf(concat("../v3weight_", idx));
            if(v3w[i]!=0) v3t[i]=atoi(chs(concat("../v3type_", idx)));
            // VAR 04
            v4w[i] = chf(concat("../v4weight_", idx));
            if(v4w[i]!=0) v4t[i]=atoi(chs(concat("../v4type_", idx)));
            // POST VAR 01
            P1w[i] = chf(concat("../p1weight_", idx));
            if(P1w[i] >0) P1t[i]=atoi(chs(concat("../p1type_", idx)));
            // AFFINE
            _x = chu(concat("../x_", idx));
            _y = chu(concat("../y_", idx));
            _a = chf(concat("../ang_", idx));
            if(_a!=0){
                affineRot(_m2, _x, _y, -radians(_a));
                _x = set(_m2.xx, _m2.xy);
                _y = set(_m2.yx, _m2.yy);
            }
            x[i] = _x; y[i] = _y;
            o[i] = chu(concat("../o_", idx));
            // POST AFFINE
            PPL[i] = chi(concat("../dopost_", idx));
            if(PPL[i]){
                _x = chu(concat("../px_", idx));
                _y = chu(concat("../py_", idx));
                _a = chf(concat("../pang_", idx));
                if(_a!=0){
                    affineRot(_m2, _x, _y, -radians(_a));
                    _x = set(_m2.xx, _m2.xy);
                    _y = set(_m2.yx, _m2.yy);
                }
                px[i] = _x; py[i] = _y;
                po[i] = chu(concat("../po_", idx));
            }
        }
        // Build TM
        if(TM){
            grt = chf("../tmrt");
            TMm2 = (matrix2)maketransform(0, set(0, 0, grt));
        }
        if(FF){
            // FF VAR 01
            fv1w = chf("../ffv1weight");
            if(fv1w!=0) fv1t = chi("../ffv1type");
            // FF VAR 02
            fv2w = chf("../ffv2weight");
            if(fv2w!=0) fv2t = chi("../ffv2type");
            // FF VAR 03
            fv3w = chf("../ffv3weight");
            if(fv3w!=0) fv3t = chi("../ffv3type");
            // // FF POST VAR 01
            fp1w = chf("../ffp1weight");
            if(fp1w >0) fp1t = chi("../ffp1type");
            // // FF POST VAR 02
            fp2w = chf("../ffp2weight");
            if(fp2w >0) fp2t = chi("../ffp2type");
            // FF AFFINE
            _x = chu("../ffx");
            _y = chu("../ffy");
            _a = chf("../ffang");
            if(_a!=0){
                affineRot(_m2, _x, _y, -radians(_a));
                _x = set(_m2.xx, _m2.xy);
                _y = set(_m2.yx, _m2.yy);
            }
            fx = _x; fy = _y;
            fo = chu("../ffo");
            // FF POST AFFINE
            PFF = chi("../ffdopost");
            if(PFF){
                _x = chu("../ffpx");
                _y = chu("../ffpy");
                _a = chf("../ffpang");
                if(_a!=0){
                    affineRot(_m2, _x, _y, -radians(_a));
                    _x = set(_m2.xx, _m2.xy);
                    _y = set(_m2.yx, _m2.yy);
                }
                pfx = _x; pfy = _y;
                pfo = chu("../ffpo");
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
    vector  pc_DISC2[]; // pc_BWRAPS[], pc_WEDGEJULIA[];

    void gemPrmBuild(const string sIDX[]; const int res, TYPE[]; const float w[]){

        if(max(TYPE)>26){
            
            int T;
            string idx;
            // float
            resize(rings2_val, res); bipolar_shift=cell_size=escher_beta=popcorn2_c=flux_spread=rings2_val;
            // vector
            resize(blob, res); pc_DISC2=pie=supershape=supershape_n=cpow=lazysusan=blob;
            // vector2
            resize(curl_c, res); parabola=fan2=rectangles=bent2=lazysusanxyz=modulus=popcorn2=separation=separation_inside=split=splits=waves2_scale=waves2_freq=curve_lenght=curve_amp=polynomial_pow=polynomial_lc=polynomial_sc=julian=juliascope=radialblur=disc2=flower=conic=stripes=whorl=persp=bwrapstwist=curl_c;
            // vector4
            resize(ngon, res); pdj_w=oscope=wedge=wedgejulia=wedgesph=auger=mobius_re=mobius_im=ngon;

            for(int i=0; i<res; ++i){
                
                T=TYPE[i]; idx=sIDX[i];
                if(T<27 || w[i]==0) continue;
                else if(find( {27, 28, 29, 30, 31, 32, 34, 35, 36, 37, 38, 47, 48, 49, 50, 51, 52, 53, 56, 57} , T )>=0){
                    if(T<38){
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
                        else if(T==37){ radialblur[i] = chu(concat("../radialblur_", idx)); continue; }
                    }
                    else{
                        // 38 PIE
                        if(T==38){ pie[i] = chv(concat("../pie_", idx)); continue; }
                        // 47 DISC2 ( This seem to be the only one to benefit from the precalc: 18% faster. )
                        else if(T==47){
                            disc2[i] = chu(concat("../disc2_", idx));
                            float rot=disc2[i][0]; float twist=disc2[i][1];
                            vector calc; precalc_V_DISC2(calc, rot, twist);
                            pc_DISC2[i] = calc;
                            continue;
                        }
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
                    }
                }
                else if(find( {61, 63, 66, 67, 69, 71, 72, 73, 74, 75, 76, 77, 78, 79, 94, 95, 96, 97, 98, 99, 101} , T )>=0){
                    if(T<77){
                        // 61 ESCHER
                        if(T==61){ escher_beta[i] = chf(concat("../escherbeta_", idx)); continue; }
                        // 63 LAZYSUSAN
                        else if(T==63){
                            lazysusanxyz[i] = chu(concat("../lazysusanxyz_", idx));
                            lazysusan[i]    = chv(concat("../lazysusan_", idx)); continue; }
                        // 66 MODULUS
                        else if(T==66){ modulus[i] = chu(concat("../modulusXYZ_", idx)); continue; }
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
                        // 76 WEDGE JULIA ( The precalc made it 10% slower, I dnt know why...odd. )
                        else if(T==76){ wedgejulia[i] = chp(concat("../wedgejulia_", idx));
                            // precalc
                            // float power=wedgejulia[i][0]; float angle= wedgejulia[i][1]; float dist=wedgejulia[i][2]; float count=wedgejulia[i][3];
                            // vector calc; precalc_V_WEDGEJULIA(calc, power, angle, dist, count);
                            // pc_WEDGEJULIA[i] = calc;
                            continue;
                        }
                    }
                    else{
                        // 77 WEDGE SPH
                        if(T==77){ wedgesph[i] = chp(concat("../wedgesph_", idx)); continue; }
                        // 78 WHORL
                        else if(T==78){ whorl[i]  = chu(concat("../whorl_", idx)); continue; }
                        // 79 WAVES2
                        else if(T==79){
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
                        // 99 BWRAPS ( The precalc made it 15% slower, I dnt know why...odd. )
                        else if(T==99){
                            bwraps[i] = chv(concat("../bwraps_", idx));
                            bwrapstwist[i] = chu(concat("../bwrapstwist_", idx));
                            // precalc
                            // float cellsize=bwraps[i][0]; float space=bwraps[i][1]; float gain=bwraps[i][2];
                            // vector calc; precalc_V_BWRAPS(calc, cellsize, space, gain);
                            // pc_BWRAPS[i] = calc;
                            continue; }
                        // 101 POLYNOMIAL
                        else if(T==101){
                            polynomial_pow[i] = chu(concat("../polynomialpow_", idx));
                            polynomial_lc[i]  = chu(concat("../polynomiallc_", idx));
                            polynomial_sc[i]  = chu(concat("../polynomialsc_", idx)); continue;
                        }
                    }
                }
            }
        }
    }
}

#endif
