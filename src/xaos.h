#ifndef __xaos_h__
#define __xaos_h__

/*  
 /  Title:      SideFX Houdini FLAM3: 2D
 /  Author:     Alessandro Nardini
 /  date:       December 2022, Last revised December 2022
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
 /              Allow up to 20 iterators max.
 /              This is being done to overcome a Houdini bug in the array slice function
 /              as it does not always produce correct results when a variable inside the chaos game loop
 /              is being updated and used as index for the array slice start and end position each iteration.
 /              so I'm slicing it manually here based on iterators number, for a max of up to 20 iterators.
 /              
 /              Not ideal, as it could have been just a one line of code instead.
 /              
 /              I filed the bug to SideFX on the 10th of October 2022 
 /              [Bug ID# 124486], SideFX Support Ticket [SESI #128304]
 /              
 /              ...never heard back from them.
*/



//int XAOS(int idx; const int res; const float XST[]){

// "res" is an INT but for some reasons this way is faster...
int XAOS(int idx; const float res, XST[]){
 
    if(res<15){
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
        else if(res==11){
            if(idx==0){ return sample_cdf((float[])XST[0:11], nrandom('twister')); }
            else if(idx==1){ return sample_cdf((float[])XST[11:22], nrandom('twister')); }
            else if(idx==2){ return sample_cdf((float[])XST[22:33], nrandom('twister')); }
            else if(idx==3){ return sample_cdf((float[])XST[33:44], nrandom('twister')); }
            else if(idx==4){ return sample_cdf((float[])XST[44:55], nrandom('twister')); }
            else if(idx==5){ return sample_cdf((float[])XST[55:66], nrandom('twister')); }
            else if(idx==6){ return sample_cdf((float[])XST[66:77], nrandom('twister')); }
            else if(idx==7){ return sample_cdf((float[])XST[77:88], nrandom('twister')); }
            else if(idx==8){ return sample_cdf((float[])XST[88:99], nrandom('twister')); }
            else if(idx==9){ return sample_cdf((float[])XST[99:110], nrandom('twister')); }
            else if(idx==10){ return sample_cdf((float[])XST[110:121], nrandom('twister')); }
        }
        else if(res==12){
            if(idx==0){ return sample_cdf((float[])XST[0:12], nrandom('twister')); }
            else if(idx==1){ return sample_cdf((float[])XST[12:24], nrandom('twister')); }
            else if(idx==2){ return sample_cdf((float[])XST[24:36], nrandom('twister')); }
            else if(idx==3){ return sample_cdf((float[])XST[36:48], nrandom('twister')); }
            else if(idx==4){ return sample_cdf((float[])XST[48:60], nrandom('twister')); }
            else if(idx==5){ return sample_cdf((float[])XST[60:72], nrandom('twister')); }
            else if(idx==6){ return sample_cdf((float[])XST[72:84], nrandom('twister')); }
            else if(idx==7){ return sample_cdf((float[])XST[84:96], nrandom('twister')); }
            else if(idx==8){ return sample_cdf((float[])XST[96:108], nrandom('twister')); }
            else if(idx==9){ return sample_cdf((float[])XST[108:120], nrandom('twister')); }
            else if(idx==10){ return sample_cdf((float[])XST[120:132], nrandom('twister')); }
            else if(idx==11){ return sample_cdf((float[])XST[132:144], nrandom('twister')); }
        }
        else if(res==13){
            if(idx==0){ return sample_cdf((float[])XST[0:13], nrandom('twister')); }
            else if(idx==1){ return sample_cdf((float[])XST[13:26], nrandom('twister')); }
            else if(idx==2){ return sample_cdf((float[])XST[26:39], nrandom('twister')); }
            else if(idx==3){ return sample_cdf((float[])XST[39:52], nrandom('twister')); }
            else if(idx==4){ return sample_cdf((float[])XST[52:65], nrandom('twister')); }
            else if(idx==5){ return sample_cdf((float[])XST[65:78], nrandom('twister')); }
            else if(idx==6){ return sample_cdf((float[])XST[78:91], nrandom('twister')); }
            else if(idx==7){ return sample_cdf((float[])XST[91:104], nrandom('twister')); }
            else if(idx==8){ return sample_cdf((float[])XST[104:117], nrandom('twister')); }
            else if(idx==9){ return sample_cdf((float[])XST[117:130], nrandom('twister')); }
            else if(idx==10){ return sample_cdf((float[])XST[130:143], nrandom('twister')); }
            else if(idx==11){ return sample_cdf((float[])XST[143:156], nrandom('twister')); }
            else if(idx==12){ return sample_cdf((float[])XST[156:169], nrandom('twister')); }
        }
        else if(res==14){
            if(idx<7){
                if(idx==0){ return sample_cdf((float[])XST[0:14], nrandom('twister')); }
                else if(idx==1){ return sample_cdf((float[])XST[14:28], nrandom('twister')); }
                else if(idx==2){ return sample_cdf((float[])XST[28:42], nrandom('twister')); }
                else if(idx==3){ return sample_cdf((float[])XST[42:56], nrandom('twister')); }
                else if(idx==4){ return sample_cdf((float[])XST[56:70], nrandom('twister')); }
                else if(idx==5){ return sample_cdf((float[])XST[70:84], nrandom('twister')); }
                else if(idx==6){ return sample_cdf((float[])XST[84:98], nrandom('twister')); }
            }
            else{
                if(idx==7){ return sample_cdf((float[])XST[98:112], nrandom('twister')); }
                else if(idx==8){ return sample_cdf((float[])XST[112:126], nrandom('twister')); }
                else if(idx==9){ return sample_cdf((float[])XST[126:140], nrandom('twister')); }
                else if(idx==10){ return sample_cdf((float[])XST[140:154], nrandom('twister')); }
                else if(idx==11){ return sample_cdf((float[])XST[154:168], nrandom('twister')); }
                else if(idx==12){ return sample_cdf((float[])XST[168:182], nrandom('twister')); }
                else if(idx==13){ return sample_cdf((float[])XST[182:196], nrandom('twister')); }
            }
        }
    }
    else if(res<21){
        if(res==15){
            if(idx<8){
                if(idx==0){ return sample_cdf((float[])XST[0:15], nrandom('twister')); }
                else if(idx==1){ return sample_cdf((float[])XST[15:30], nrandom('twister')); }
                else if(idx==2){ return sample_cdf((float[])XST[30:45], nrandom('twister')); }
                else if(idx==3){ return sample_cdf((float[])XST[45:60], nrandom('twister')); }
                else if(idx==4){ return sample_cdf((float[])XST[60:75], nrandom('twister')); }
                else if(idx==5){ return sample_cdf((float[])XST[75:90], nrandom('twister')); }
                else if(idx==6){ return sample_cdf((float[])XST[90:105], nrandom('twister')); }
                else if(idx==7){ return sample_cdf((float[])XST[105:120], nrandom('twister')); }
            }
            else{
                if(idx==8){ return sample_cdf((float[])XST[120:135], nrandom('twister')); }
                else if(idx==9){ return sample_cdf((float[])XST[135:150], nrandom('twister')); }
                else if(idx==10){ return sample_cdf((float[])XST[150:165], nrandom('twister')); }
                else if(idx==11){ return sample_cdf((float[])XST[165:180], nrandom('twister')); }
                else if(idx==12){ return sample_cdf((float[])XST[180:195], nrandom('twister')); }
                else if(idx==13){ return sample_cdf((float[])XST[195:210], nrandom('twister')); }
                else if(idx==14){ return sample_cdf((float[])XST[210:225], nrandom('twister')); }
            }
        }
        else if(res==16){
            if(idx<8){
                if(idx==0){ return sample_cdf((float[])XST[0:16], nrandom('twister')); }
                else if(idx==1){ return sample_cdf((float[])XST[16:32], nrandom('twister')); }
                else if(idx==2){ return sample_cdf((float[])XST[32:48], nrandom('twister')); }
                else if(idx==3){ return sample_cdf((float[])XST[48:64], nrandom('twister')); }
                else if(idx==4){ return sample_cdf((float[])XST[64:80], nrandom('twister')); }
                else if(idx==5){ return sample_cdf((float[])XST[80:96], nrandom('twister')); }
                else if(idx==6){ return sample_cdf((float[])XST[96:112], nrandom('twister')); }
                else if(idx==7){ return sample_cdf((float[])XST[112:128], nrandom('twister')); }
            }
            else{
                if(idx==8){ return sample_cdf((float[])XST[128:144], nrandom('twister')); }
                else if(idx==9){ return sample_cdf((float[])XST[144:160], nrandom('twister')); }
                else if(idx==10){ return sample_cdf((float[])XST[160:176], nrandom('twister')); }
                else if(idx==11){ return sample_cdf((float[])XST[176:192], nrandom('twister')); }
                else if(idx==12){ return sample_cdf((float[])XST[192:208], nrandom('twister')); }
                else if(idx==13){ return sample_cdf((float[])XST[208:224], nrandom('twister')); }
                else if(idx==14){ return sample_cdf((float[])XST[224:240], nrandom('twister')); }
                else if(idx==15){ return sample_cdf((float[])XST[240:256], nrandom('twister')); }
            }
        }
        else if(res==17){
            if(idx<9){
                if(idx==0){ return sample_cdf((float[])XST[0:17], nrandom('twister')); }
                else if(idx==1){ return sample_cdf((float[])XST[17:34], nrandom('twister')); }
                else if(idx==2){ return sample_cdf((float[])XST[34:51], nrandom('twister')); }
                else if(idx==3){ return sample_cdf((float[])XST[51:68], nrandom('twister')); }
                else if(idx==4){ return sample_cdf((float[])XST[68:85], nrandom('twister')); }
                else if(idx==5){ return sample_cdf((float[])XST[85:102], nrandom('twister')); }
                else if(idx==6){ return sample_cdf((float[])XST[102:119], nrandom('twister')); }
                else if(idx==7){ return sample_cdf((float[])XST[119:136], nrandom('twister')); }
                else if(idx==8){ return sample_cdf((float[])XST[136:153], nrandom('twister')); }
            }
            else{
                if(idx==9){ return sample_cdf((float[])XST[153:170], nrandom('twister')); }
                else if(idx==10){ return sample_cdf((float[])XST[170:187], nrandom('twister')); }
                else if(idx==11){ return sample_cdf((float[])XST[187:204], nrandom('twister')); }
                else if(idx==12){ return sample_cdf((float[])XST[204:221], nrandom('twister')); }
                else if(idx==13){ return sample_cdf((float[])XST[221:238], nrandom('twister')); }
                else if(idx==14){ return sample_cdf((float[])XST[238:255], nrandom('twister')); }
                else if(idx==15){ return sample_cdf((float[])XST[255:272], nrandom('twister')); }
                else if(idx==16){ return sample_cdf((float[])XST[272:289], nrandom('twister')); }
            }
        }
        else if(res==18){
            if(idx<9){
                if(idx==0){ return sample_cdf((float[])XST[0:18], nrandom('twister')); }
                else if(idx==1){ return sample_cdf((float[])XST[18:36], nrandom('twister')); }
                else if(idx==2){ return sample_cdf((float[])XST[36:54], nrandom('twister')); }
                else if(idx==3){ return sample_cdf((float[])XST[54:72], nrandom('twister')); }
                else if(idx==4){ return sample_cdf((float[])XST[72:90], nrandom('twister')); }
                else if(idx==5){ return sample_cdf((float[])XST[90:108], nrandom('twister')); }
                else if(idx==6){ return sample_cdf((float[])XST[108:126], nrandom('twister')); }
                else if(idx==7){ return sample_cdf((float[])XST[126:144], nrandom('twister')); }
                else if(idx==8){ return sample_cdf((float[])XST[144:162], nrandom('twister')); }
            }
            else{
                if(idx==9){ return sample_cdf((float[])XST[162:180], nrandom('twister')); }
                else if(idx==10){ return sample_cdf((float[])XST[180:198], nrandom('twister')); }
                else if(idx==11){ return sample_cdf((float[])XST[198:216], nrandom('twister')); }
                else if(idx==12){ return sample_cdf((float[])XST[216:234], nrandom('twister')); }
                else if(idx==13){ return sample_cdf((float[])XST[234:252], nrandom('twister')); }
                else if(idx==14){ return sample_cdf((float[])XST[252:270], nrandom('twister')); }
                else if(idx==15){ return sample_cdf((float[])XST[270:288], nrandom('twister')); }
                else if(idx==16){ return sample_cdf((float[])XST[288:306], nrandom('twister')); }
                else if(idx==17){ return sample_cdf((float[])XST[306:324], nrandom('twister')); }
            }
        }
        else if(res==19){
            if(idx<10){
                if(idx==0){ return sample_cdf((float[])XST[0:19], nrandom('twister')); }
                else if(idx==1){ return sample_cdf((float[])XST[19:38], nrandom('twister')); }
                else if(idx==2){ return sample_cdf((float[])XST[38:57], nrandom('twister')); }
                else if(idx==3){ return sample_cdf((float[])XST[57:76], nrandom('twister')); }
                else if(idx==4){ return sample_cdf((float[])XST[76:95], nrandom('twister')); }
                else if(idx==5){ return sample_cdf((float[])XST[95:114], nrandom('twister')); }
                else if(idx==6){ return sample_cdf((float[])XST[114:133], nrandom('twister')); }
                else if(idx==7){ return sample_cdf((float[])XST[133:152], nrandom('twister')); }
                else if(idx==8){ return sample_cdf((float[])XST[152:171], nrandom('twister')); }
                else if(idx==9){ return sample_cdf((float[])XST[171:190], nrandom('twister')); }
            }
            else{
                if(idx==10){ return sample_cdf((float[])XST[190:209], nrandom('twister')); }
                else if(idx==11){ return sample_cdf((float[])XST[209:228], nrandom('twister')); }
                else if(idx==12){ return sample_cdf((float[])XST[228:247], nrandom('twister')); }
                else if(idx==13){ return sample_cdf((float[])XST[247:266], nrandom('twister')); }
                else if(idx==14){ return sample_cdf((float[])XST[266:285], nrandom('twister')); }
                else if(idx==15){ return sample_cdf((float[])XST[285:304], nrandom('twister')); }
                else if(idx==16){ return sample_cdf((float[])XST[304:323], nrandom('twister')); }
                else if(idx==17){ return sample_cdf((float[])XST[323:342], nrandom('twister')); }
                else if(idx==18){ return sample_cdf((float[])XST[342:361], nrandom('twister')); }
            }
        }
        else if(res==20){
            if(idx<10){
                if(idx==0){ return sample_cdf((float[])XST[0:20], nrandom('twister')); }
                else if(idx==1){ return sample_cdf((float[])XST[20:40], nrandom('twister')); }
                else if(idx==2){ return sample_cdf((float[])XST[40:60], nrandom('twister')); }
                else if(idx==3){ return sample_cdf((float[])XST[60:80], nrandom('twister')); }
                else if(idx==4){ return sample_cdf((float[])XST[80:100], nrandom('twister')); }
                else if(idx==5){ return sample_cdf((float[])XST[100:120], nrandom('twister')); }
                else if(idx==6){ return sample_cdf((float[])XST[120:140], nrandom('twister')); }
                else if(idx==7){ return sample_cdf((float[])XST[140:160], nrandom('twister')); }
                else if(idx==8){ return sample_cdf((float[])XST[160:180], nrandom('twister')); }
                else if(idx==9){ return sample_cdf((float[])XST[180:200], nrandom('twister')); }
            }
            else{
                if(idx==10){ return sample_cdf((float[])XST[200:220], nrandom('twister')); }
                else if(idx==11){ return sample_cdf((float[])XST[220:240], nrandom('twister')); }
                else if(idx==12){ return sample_cdf((float[])XST[240:260], nrandom('twister')); }
                else if(idx==13){ return sample_cdf((float[])XST[260:280], nrandom('twister')); }
                else if(idx==14){ return sample_cdf((float[])XST[280:300], nrandom('twister')); }
                else if(idx==15){ return sample_cdf((float[])XST[300:320], nrandom('twister')); }
                else if(idx==16){ return sample_cdf((float[])XST[320:340], nrandom('twister')); }
                else if(idx==17){ return sample_cdf((float[])XST[340:360], nrandom('twister')); }
                else if(idx==18){ return sample_cdf((float[])XST[360:380], nrandom('twister')); }
                else if(idx==19){ return sample_cdf((float[])XST[380:400], nrandom('twister')); }
            }
        }
    }

    /*
    else{
        // The following is what it should have been if there was not a bug in Houdini.
        // [Bug ID# 124486], SideFX Support Ticket [SESI #128304]
        int sl=idx*res; return sample_cdf((float[])XST[sl:sl+res], nrandom('twister'));
    }
    */

    return idx;

}



#endif