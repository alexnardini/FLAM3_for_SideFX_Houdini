#ifndef __genome_h__
#define __genome_h__

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
 /  Name:       FLAME GENOME   "VEX"
 /
 /  Comment:    GENOME entities and properties.
*/


struct genomeSYS{
    int TMG, DELINVALIDPT, POSTF, FF, iter_f, symmetry, sym_mode, iter, domb, vizmb;
    float mb_modulate;

    void genomeSYSBuild(){
        TMG           = chi("../dotmglobal");
        FF            = chi("../dofinalflame");
        POSTF         = chi("../_dofpost_2");
        DELINVALIDPT  = chi("../delinvalidpt");
        symmetry      = chi("../symmetry");
        iter_f        = chi("../flamefunc");
        iter          = chi("../iter");
        domb          = chi("../domb");
        mb_modulate   = 1.0;
        if(symmetry) sym_mode = chi("../rotational");
        if(domb){ vizmb = chi("../vizmb"); mb_modulate = detail(1, "Tstep_mult", 0); }
    }
}

struct genome{
    int     v1type[], v2type[], v3type[], v4type[], p1type[], POSTL[], ffv1type, ffv2type, ffv3type, ffp1type;
    float   IW[], v1weight[], v2weight[], v3weight[], v4weight[], p1weight[], PBWEIGHT[], CLR[], ONEMINUS[], ffv1weight, ffv2weight, ffv3weight, ffp1weight, grt;
    vector2 gtr, gsc, x[], y[], o[], px[], py[], po[], fx, fy, fo, pfx, pfy, pfo;
    string  sIDX[];

    void genomeBuild(const int VACTIVE[]; const genomeSYS SYS){
        float coord, speed;
        for(int i=0; i<SYS.iter_f; i++){
            if(!VACTIVE[i]) continue;
            string IDX=itoa(i+1);
            // Collect active variation IDs
            append(sIDX, IDX); int res=len(sIDX);
            // Iterator's weights
            append(IW, chf(concat("../iw_", IDX)));
            // Color
            coord = chf(concat("../clr_", IDX));
            speed = chf(concat("../clrspeed_", IDX));
            append(CLR, speed*coord);
            append(ONEMINUS, 1-speed);
            // PRE BLUR
            append(PBWEIGHT, chf(concat("../preblurweight_" , IDX)));
            // VAR 01
            append(v1weight, chf(concat("../v1weight_", IDX)));
            if(v1weight[-1]!=0) append(v1type, atoi(chs(concat("../v1type_", IDX))));
            else resize(v1type, res);
            // VAR 02
            append(v2weight, chf(concat("../v2weight_", IDX)));
            if(v2weight[-1]!=0) append(v2type, atoi(chs(concat("../v2type_", IDX))));
            else resize(v2type, res);
            // VAR 03
            append(v3weight, chf(concat("../v3weight_", IDX)));
            if(v3weight[-1]!=0) append(v3type, atoi(chs(concat("../v3type_", IDX))));
            else resize(v3type, res);
            // VAR 04
            append(v4weight, chf(concat("../v4weight_", IDX)));
            if(v4weight[-1]!=0) append(v4type, atoi(chs(concat("../v4type_", IDX))));
            else resize(v4type, res);
            // POST VAR 01
            append(p1weight, chf(concat("../p1weight_", IDX)));
            if(p1weight[-1]!=0) append(p1type, atoi(chs(concat("../p1type_", IDX))));
            else resize(p1type, res);
            // Collect affine coefficients
            append(x, chu(concat("../x_", IDX)));
            append(y, chu(concat("../y_", IDX)));
            append(o, chu(concat("../o_", IDX)));
            // POST
            append(POSTL, chi(concat("../dopost_", IDX)));
            if(POSTL[-1]){
                append(px, chu(concat("../px_", IDX)));
                append(py, chu(concat("../py_", IDX)));
                append(po, chu(concat("../po_", IDX)));
                }
            else{ resize(px, res); resize(py, res); resize(po, res); }
        }
        // Collect GLOBAL TM
        if(SYS.TMG){
            // Translate
            gtr = chu("../ftr");
            // Rotate
            grt = chf("../frt");
            // Scale
            gsc = chu("../fsc");
            // Pivot
            //gpv = chv("../fpv");
        }
        if(SYS.FF){
            // FF VAR 01
            ffv1weight = chf("../ffv1weight");
            if(ffv1weight!=0) ffv1type = chi("../ffv1type");
            // FF VAR 02
            ffv2weight = chf("../ffv2weight");
            if(ffv2weight!=0) ffv2type = chi("../ffv2type");
            // FF VAR 03
            ffv3weight = chf("../ffv3weight");
            if(ffv3weight!=0) ffv3type = chi("../ffp1type");
            // // FF POST VAR 01
            ffp1weight = chf("../ffp1weight");
            if(ffp1weight!=0) ffp1type = chi("../ffp1type");
            // Collect FINAL FLAME TRANSFORM affine coefficients
            fx = chu("../_fx_2");
            fy = chu("../_fy_2");
            fo = chu("../_fo_2");
            // POST
            if(SYS.POSTF){
                pfx = chu("../_pfx_2");
                pfy = chu("../_pfy_2");
                pfo = chu("../_pfo_2");
            }
        }
    }
}

struct genomeParametrics{
    float   rings2_val[], bipolar_shift[], cell_size[], escher_beta[], popcorn2_c[], flux_spread[];
    vector  blob[], pie[], supershape[], supershape_n[], cpow[], lazysusan[], bwraps[];
    vector2 curl_c[], parabola[], fan2[], rectangles[], bent2[], lazysusanxyz[], modulus[], popcorn2[], separation[], separation_inside[], split[], splits[], waves2_scale[], waves2_freq[], curve_lenght[], curve_amp[], polynomial_pow[], polynomial_lc[], polynomial_sc[], julian[], juliascope[], radialblur[], disc2[], flower[], conic[], stripes[], whorl[], persp[], bwrapstwist[];
    vector4 ngon[], pdj_w[], oscope[], wedge[], wedgejulia[], wedgesph[], auger[], mobius_re[], mobius_im[];

    void genomeParametricsBuild(const string MODE, sIDX[]; const int GEMTYPE[]){

        if(max(GEMTYPE)>26){
            int iter_f = len(GEMTYPE);
            int TYPE, TYPES_1[], TYPES_2[];
            string PRX, IDX;
            TYPES_1 = {27, 28, 29, 30, 31, 32, 34, 35, 36, 37, 38, 47, 48, 49, 50, 51, 52, 53, 56, 57};
            TYPES_2 = {61, 63, 66, 67, 69, 71, 72, 73, 74, 75, 76, 77, 78, 79, 94, 95, 96, 97, 98, 99, 101};
            // FLOAT
            resize(rings2_val, iter_f); bipolar_shift=cell_size=escher_beta=popcorn2_c=flux_spread=rings2_val;
            // VECTOR
            resize(blob, iter_f);       pie=supershape=supershape_n=cpow=lazysusan=blob;
            // VECTOR2
            resize(curl_c, iter_f);     parabola=fan2=rectangles=bent2=lazysusanxyz=modulus=popcorn2=separation=separation_inside=split=splits=waves2_scale=waves2_freq=curve_lenght=curve_amp=polynomial_pow=polynomial_lc=polynomial_sc=julian=juliascope=radialblur=disc2=flower=conic=stripes=whorl=persp=bwrapstwist=curl_c;
            // VECTOR4
            resize(ngon, iter_f);       pdj_w=oscope=wedge=wedgejulia=wedgesph=auger=mobius_re=mobius_im=ngon;
            // The following will come handy if we add PRE/POST variations
            PRX="../";
            // iterate
            for(int i=0; i<iter_f; i++){
                TYPE=GEMTYPE[i]; IDX=sIDX[i];
                if(TYPE<27) continue;
                else if(find(TYPES_1, TYPE)>=0){
                    if(TYPE<38){
                        // 27 CURL
                        if(TYPE==27){ curl_c[i] = chu(concat(PRX, "curlc_", IDX)); continue; }
                        // 28 NGON
                        else if(TYPE==28){ ngon[i]  = chp(concat(PRX, "ngon_", IDX)); continue; }
                        // 29 PDJ
                        else if(TYPE==29){ pdj_w[i] = chp(concat(PRX, "pdjw_", IDX)); continue; }
                        // 30 BLOB
                        else if(TYPE==30){ blob[i]  = chv(concat(PRX, "blob_",  IDX)); continue; }
                        // 31 JuliaN
                        else if(TYPE==31){ julian[i] = chu(concat(PRX, "julian_", IDX)); continue; }
                        // 32 JuliaScope
                        else if(TYPE==32){ juliascope[i] = chu(concat(PRX, "juliascope_", IDX)); continue; }
                        // 34 FAN2
                        else if(TYPE==34){ fan2[i] = chu(concat(PRX, "fan2_", IDX)); continue; }
                        // 35 RINGS2
                        else if(TYPE==35){ rings2_val[i] = chf(concat(PRX, "rings2val_", IDX)); continue; }
                        // 36 RECTANGLES
                        else if(TYPE==36){ rectangles[i] = chu(concat(PRX, "rectangles_", IDX)); continue; }
                        // 37 RADIAL BLUR
                        else if(TYPE==37){ radialblur[i] = chu(concat(PRX, "radialblur_", IDX)); continue; }
                    }
                    else{
                        // 38 PIE
                        if(TYPE==38){ pie[i] = chv(concat(PRX, "pie_", IDX)); continue; }
                        // 47 DISC2
                        else if(TYPE==47){ disc2[i] = chu(concat(PRX, "disc2_", IDX)); continue; }
                        // 48 SUPERSHAPE
                        else if(TYPE==48){
                            supershape[i]   = chv(concat(PRX, "supershape_",  IDX));
                            supershape_n[i] = chv(concat(PRX, "supershapen_", IDX)); continue; }
                        // 49 FLOWER
                        else if(TYPE==49){ flower[i] = chu(concat(PRX, "flower_", IDX)); continue; }
                        // 50 CONIC
                        else if(TYPE==50){ conic[i] = chu(concat(PRX, "conic_", IDX)); continue; }
                        // 51 PARABOLA
                        else if(TYPE==51){ parabola[i] = chu(concat(PRX, "parabola_", IDX)); continue; }
                        // 52 BENT2
                        else if(TYPE==52){ bent2[i] = chu(concat(PRX, "bent2xy_", IDX)); continue; }
                        // 53 BIPOLAR
                        else if(TYPE==53){ bipolar_shift[i] = chf(concat(PRX, "bipolarshift_", IDX)); continue; }
                        // 56 CELL
                        else if(TYPE==56){ cell_size[i] = chf(concat(PRX, "cellsize_", IDX)); continue; }
                        // 57 CPOW
                        else if(TYPE==57){ cpow[i] = chv(concat(PRX, "cpow_", IDX)); continue; }
                    }
                }
                else if(find(TYPES_2, TYPE)>=0){
                    if(TYPE<77){
                        // 61 ESCHER
                        if(TYPE==61){ escher_beta[i] = chf(concat(PRX, "escherbeta_", IDX)); continue; }
                        // 63 LAZYSUSAN
                        else if(TYPE==63){
                            lazysusanxyz[i] = chu(concat(PRX, "lazysusanxyz_", IDX));
                            lazysusan[i]    = chu(concat(PRX, "lazysusan_", IDX)); continue; }
                        // 66 MODULUS
                        else if(TYPE==66){ modulus[i] = chu(concat(PRX, "modulusXYZ_", IDX)); continue; }
                        // 67 OSCOPE
                        else if(TYPE==67){ oscope[i] = chp(concat(PRX, "oscope_", IDX)); continue; }
                        // 69 POPCORN2
                        else if(TYPE==69){
                            popcorn2[i]   = chu(concat(PRX, "popcorn2xyz_", IDX));
                            popcorn2_c[i] = chf(concat(PRX, "popcorn2c_",   IDX)); continue; }
                        // 71 SEPARATION
                        else if(TYPE==71){
                            separation[i]        = chu(concat(PRX, "separationxyz_", IDX));
                            separation_inside[i] = chu(concat(PRX, "separationinsidexyz_", IDX)); continue; }
                        // 72 SPLIT
                        else if(TYPE==72){ split[i] = chu(concat(PRX, "splitxyz_", IDX)); continue; }
                        // 73 SPLITS
                        else if(TYPE==73){ splits[i] = chu(concat(PRX, "splitsxyz_", IDX)); continue; }
                        // 74 STRIPES
                        else if(TYPE==74){ stripes[i] = chu(concat(PRX, "stripes_", IDX)); continue; }
                        // 75 WEDGE
                        else if(TYPE==75){ wedge[i] = chp(concat(PRX, "wedge_", IDX)); continue; }
                        // 76 WEDGE JULIA
                        else if(TYPE==76){ wedgejulia[i] = chp(concat(PRX, "wedgejulia_", IDX)); continue; }
                    }
                    else{
                        // 77 WEDGE SPH
                        if(TYPE==77){ wedgesph[i] = chp(concat(PRX, "wedgesph_", IDX)); continue; }
                        // 78 WHORL
                        else if(TYPE==78){ whorl[i]  = chu(concat(PRX, "whorl_",  IDX)); continue; }
                        // 79 WAVES2
                        else if(TYPE==79){
                            waves2_scale[i] = chu(concat(PRX, "waves2scalexyz_", IDX));
                            waves2_freq[i]  = chu(concat(PRX, "waves2freqxyz_",  IDX)); continue; }
                        // 94 AUGER
                        else if(TYPE==94){ auger[i] = chp(concat(PRX, "auger_",   IDX)); continue; }
                        // 95 FLUX
                        else if(TYPE==95){ flux_spread[i] = chf(concat(PRX, "fluxspread_", IDX)); continue; }
                        // 96 MOBIUS
                        else if(TYPE==96){
                            mobius_re[i] = chp(concat(PRX, "mobiusre_", IDX));
                            mobius_im[i] = chp(concat(PRX, "mobiusim_", IDX)); continue; }
                        // 97 CURVE
                        else if(TYPE==97){
                            curve_lenght[i] = chu(concat(PRX, "curvexyzlenght_", IDX));
                            curve_amp[i]    = chu(concat(PRX, "curvexyzamp_",    IDX)); continue; }
                        // 98 PERSPECTIVE
                        else if(TYPE==98){ persp[i] = chu(concat(PRX, "persp_", IDX)); continue; }
                        // 99 BWRAPS
                        else if(TYPE==99){
                            bwraps[i] = chv(concat(PRX, "bwraps_", IDX));
                            bwrapstwist[i] = chu(concat(PRX, "bwrapstwist_", IDX)); continue; }
                        // 101 POLYNOMIAL
                        else if(TYPE==101){
                            polynomial_pow[i] = chu(concat(PRX, "polynomialpow_", IDX));
                            polynomial_lc[i]  = chu(concat(PRX, "polynomiallc_",  IDX));
                            polynomial_sc[i]  = chu(concat(PRX, "polynomialsc_",  IDX)); continue; }
                    }
                }
            }
        }
    }
}

#endif
