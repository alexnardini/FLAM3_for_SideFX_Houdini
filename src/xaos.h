#ifndef __xaos_h__
#define __xaos_h__

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
 /  Name:       XAOS "CVEX"
 /
 /  Comment:    XAOS selection.
*/



int XAOS(int idx; const float XST[], res){

    //if(res==1) 
    if(res==2){
        if(idx==0){ idx=sample_cdf((float[])XST[0:2], nrandom('twister')); return idx; }
        else{ idx=sample_cdf((float[])XST[2:4], nrandom('twister')); return idx; }
    }
    else if(res==3){
        if(idx==0){return sample_cdf((float[])XST[0:3], nrandom('twister')); }
        else if(idx==1){ return sample_cdf((float[])XST[3:6], nrandom('twister')); }
        else if(idx==2){ return sample_cdf((float[])XST[6:9], nrandom('twister')); }
    }
    else if(res==4){
        if(idx==0){ return sample_cdf((float[])XST[0:4], nrandom('twister')); }
        else if(idx==1){ return sample_cdf((float[])XST[4:8], nrandom('twister')); }
        else if(idx==2){ return sample_cdf((float[])XST[8:12], nrandom('twister')); }
        else if(idx==3){ return sample_cdf((float[])XST[12:16], nrandom('twister')); }
    }
    else if(res==5){
        if(idx==0){ return sample_cdf((float[])XST[0:5], nrandom('twister')); }
        else if(idx==1){ return sample_cdf((float[])XST[5:10], nrandom('twister')); }
        else if(idx==2){ return sample_cdf((float[])XST[10:15], nrandom('twister')); }
        else if(idx==3){ return sample_cdf((float[])XST[15:20], nrandom('twister')); }
        else if(idx==4){ return sample_cdf((float[])XST[20:25], nrandom('twister')); }
    }
    else if(res==6){
        if(idx==0){ idx=sample_cdf((float[])XST[0:6], nrandom('twister')); }
        else if(idx==1){ return sample_cdf((float[])XST[6:12], nrandom('twister')); }
        else if(idx==2){ return sample_cdf((float[])XST[12:18], nrandom('twister')); }
        else if(idx==3){ return sample_cdf((float[])XST[18:24], nrandom('twister')); }
        else if(idx==4){ return sample_cdf((float[])XST[24:30], nrandom('twister')); }
        else if(idx==5){ return sample_cdf((float[])XST[30:36], nrandom('twister')); }
    }
    else if(res==7){
        if(idx==0){ return sample_cdf((float[])XST[0:7], nrandom('twister')); }
        else if(idx==1){ return sample_cdf((float[])XST[7:14], nrandom('twister')); }
        else if(idx==2){ return sample_cdf((float[])XST[14:21], nrandom('twister')); }
        else if(idx==3){ return sample_cdf((float[])XST[21:28], nrandom('twister')); }
        else if(idx==4){ return sample_cdf((float[])XST[28:35], nrandom('twister')); }
        else if(idx==5){ return sample_cdf((float[])XST[35:42], nrandom('twister')); }
        else if(idx==6){ return sample_cdf((float[])XST[42:49], nrandom('twister')); }
    }
    else if(res==8){
        if(idx==0){ return sample_cdf((float[])XST[0:8], nrandom('twister')); }
        else if(idx==1){ return sample_cdf((float[])XST[8:16], nrandom('twister')); }
        else if(idx==2){ return sample_cdf((float[])XST[16:24], nrandom('twister')); }
        else if(idx==3){ return sample_cdf((float[])XST[24:32], nrandom('twister')); }
        else if(idx==4){ return sample_cdf((float[])XST[32:40], nrandom('twister')); }
        else if(idx==5){ return sample_cdf((float[])XST[40:48], nrandom('twister')); }
        else if(idx==6){ return sample_cdf((float[])XST[48:56], nrandom('twister')); }
        else if(idx==7){ return sample_cdf((float[])XST[56:64], nrandom('twister')); }
    }
    else if(res==9){
        if(idx==0){ return sample_cdf((float[])XST[0:9], nrandom('twister')); }
        else if(idx==1){ return sample_cdf((float[])XST[9:18], nrandom('twister')); }
        else if(idx==2){ return sample_cdf((float[])XST[18:27], nrandom('twister')); }
        else if(idx==3){ return sample_cdf((float[])XST[27:36], nrandom('twister')); }
        else if(idx==4){ return sample_cdf((float[])XST[36:45], nrandom('twister')); }
        else if(idx==5){ return sample_cdf((float[])XST[45:54], nrandom('twister')); }
        else if(idx==6){ return sample_cdf((float[])XST[54:63], nrandom('twister')); }
        else if(idx==7){ return sample_cdf((float[])XST[63:72], nrandom('twister')); }
        else if(idx==8){ return sample_cdf((float[])XST[72:81], nrandom('twister')); }
    }
    else if(res==10){
        if(idx==0){ return sample_cdf((float[])XST[0:10], nrandom('twister')); }
        else if(idx==1){ return sample_cdf((float[])XST[10:20], nrandom('twister')); }
        else if(idx==2){ return sample_cdf((float[])XST[20:30], nrandom('twister')); }
        else if(idx==3){ return sample_cdf((float[])XST[30:40], nrandom('twister')); }
        else if(idx==4){ return sample_cdf((float[])XST[40:50], nrandom('twister')); }
        else if(idx==5){ return sample_cdf((float[])XST[50:60], nrandom('twister')); }
        else if(idx==6){ return sample_cdf((float[])XST[60:70], nrandom('twister')); }
        else if(idx==7){ return sample_cdf((float[])XST[70:80], nrandom('twister')); }
        else if(idx==8){ return sample_cdf((float[])XST[80:90], nrandom('twister')); }
        else if(idx==9){ return sample_cdf((float[])XST[90:100], nrandom('twister')); }
    }

    return idx;

}



#endif