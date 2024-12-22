#ifndef __xaos_h__
#define __xaos_h__

/*  
 /  Tested on:  Houdini 19.x
 /              Houdini 19.5
 /              Houdini 20.x
 /              Houdini 20.5
 /
 /  Title:      FLAM3H. SideFX Houdini FLAM3: 2D
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
 /  Comment:    XAOS selection. Allow up to 20 iterators max.
 /
 /              This is being done to overcome a Houdini bug.
 /              Not ideal, as it could have been just a one line of code instead.
 /              
 /              I filed the bug to SideFX on the 10th of October 2022 
 /              [Bug ID# 124486], SideFX Support Ticket [SESI #128304]
 /              
*/



//int XAOS(int idx; const int res; const float XST[]){

// "res" is an INT but for some reasons this way is faster...
int XAOS(const int idx; const float res, XST[]){
 
    float u_rand = nrandom('twister');
    
    if(res<15){
        if(res==2){
            if(idx==0){ return sample_cdf((float[])XST[0:2], u_rand); }
            else{ return sample_cdf((float[])XST[2:4], u_rand); }
        }
        else if(res==3){
            if(idx==0){return sample_cdf((float[])XST[0:3], u_rand); }
            else if(idx==1){ return sample_cdf((float[])XST[3:6], u_rand); }
            else if(idx==2){ return sample_cdf((float[])XST[6:9], u_rand); }
        }
        else if(res==4){
            if(idx==0){ return sample_cdf((float[])XST[0:4], u_rand); }
            else if(idx==1){ return sample_cdf((float[])XST[4:8], u_rand); }
            else if(idx==2){ return sample_cdf((float[])XST[8:12], u_rand); }
            else if(idx==3){ return sample_cdf((float[])XST[12:16], u_rand); }
        }
        else if(res==5){
            if(idx==0){ return sample_cdf((float[])XST[0:5], u_rand); }
            else if(idx==1){ return sample_cdf((float[])XST[5:10], u_rand); }
            else if(idx==2){ return sample_cdf((float[])XST[10:15], u_rand); }
            else if(idx==3){ return sample_cdf((float[])XST[15:20], u_rand); }
            else if(idx==4){ return sample_cdf((float[])XST[20:25], u_rand); }
        }
        else if(res==6){
            if(idx==0){ return sample_cdf((float[])XST[0:6], u_rand); }
            else if(idx==1){ return sample_cdf((float[])XST[6:12], u_rand); }
            else if(idx==2){ return sample_cdf((float[])XST[12:18], u_rand); }
            else if(idx==3){ return sample_cdf((float[])XST[18:24], u_rand); }
            else if(idx==4){ return sample_cdf((float[])XST[24:30], u_rand); }
            else if(idx==5){ return sample_cdf((float[])XST[30:36], u_rand); }
        }
        else if(res==7){
            if(idx==0){ return sample_cdf((float[])XST[0:7], u_rand); }
            else if(idx==1){ return sample_cdf((float[])XST[7:14], u_rand); }
            else if(idx==2){ return sample_cdf((float[])XST[14:21], u_rand); }
            else if(idx==3){ return sample_cdf((float[])XST[21:28], u_rand); }
            else if(idx==4){ return sample_cdf((float[])XST[28:35], u_rand); }
            else if(idx==5){ return sample_cdf((float[])XST[35:42], u_rand); }
            else if(idx==6){ return sample_cdf((float[])XST[42:49], u_rand); }
        }
        else if(res==8){
            if(idx==0){ return sample_cdf((float[])XST[0:8], u_rand); }
            else if(idx==1){ return sample_cdf((float[])XST[8:16], u_rand); }
            else if(idx==2){ return sample_cdf((float[])XST[16:24], u_rand); }
            else if(idx==3){ return sample_cdf((float[])XST[24:32], u_rand); }
            else if(idx==4){ return sample_cdf((float[])XST[32:40], u_rand); }
            else if(idx==5){ return sample_cdf((float[])XST[40:48], u_rand); }
            else if(idx==6){ return sample_cdf((float[])XST[48:56], u_rand); }
            else if(idx==7){ return sample_cdf((float[])XST[56:64], u_rand); }
        }
        else if(res==9){
            if(idx==0){ return sample_cdf((float[])XST[0:9], u_rand); }
            else if(idx==1){ return sample_cdf((float[])XST[9:18], u_rand); }
            else if(idx==2){ return sample_cdf((float[])XST[18:27], u_rand); }
            else if(idx==3){ return sample_cdf((float[])XST[27:36], u_rand); }
            else if(idx==4){ return sample_cdf((float[])XST[36:45], u_rand); }
            else if(idx==5){ return sample_cdf((float[])XST[45:54], u_rand); }
            else if(idx==6){ return sample_cdf((float[])XST[54:63], u_rand); }
            else if(idx==7){ return sample_cdf((float[])XST[63:72], u_rand); }
            else if(idx==8){ return sample_cdf((float[])XST[72:81], u_rand); }
        }
        else if(res==10){
            if(idx==0){ return sample_cdf((float[])XST[0:10], u_rand); }
            else if(idx==1){ return sample_cdf((float[])XST[10:20], u_rand); }
            else if(idx==2){ return sample_cdf((float[])XST[20:30], u_rand); }
            else if(idx==3){ return sample_cdf((float[])XST[30:40], u_rand); }
            else if(idx==4){ return sample_cdf((float[])XST[40:50], u_rand); }
            else if(idx==5){ return sample_cdf((float[])XST[50:60], u_rand); }
            else if(idx==6){ return sample_cdf((float[])XST[60:70], u_rand); }
            else if(idx==7){ return sample_cdf((float[])XST[70:80], u_rand); }
            else if(idx==8){ return sample_cdf((float[])XST[80:90], u_rand); }
            else if(idx==9){ return sample_cdf((float[])XST[90:100], u_rand); }
        }
        else if(res==11){
            if(idx==0){ return sample_cdf((float[])XST[0:11], u_rand); }
            else if(idx==1){ return sample_cdf((float[])XST[11:22], u_rand); }
            else if(idx==2){ return sample_cdf((float[])XST[22:33], u_rand); }
            else if(idx==3){ return sample_cdf((float[])XST[33:44], u_rand); }
            else if(idx==4){ return sample_cdf((float[])XST[44:55], u_rand); }
            else if(idx==5){ return sample_cdf((float[])XST[55:66], u_rand); }
            else if(idx==6){ return sample_cdf((float[])XST[66:77], u_rand); }
            else if(idx==7){ return sample_cdf((float[])XST[77:88], u_rand); }
            else if(idx==8){ return sample_cdf((float[])XST[88:99], u_rand); }
            else if(idx==9){ return sample_cdf((float[])XST[99:110], u_rand); }
            else if(idx==10){ return sample_cdf((float[])XST[110:121], u_rand); }
        }
        else if(res==12){
            if(idx==0){ return sample_cdf((float[])XST[0:12], u_rand); }
            else if(idx==1){ return sample_cdf((float[])XST[12:24], u_rand); }
            else if(idx==2){ return sample_cdf((float[])XST[24:36], u_rand); }
            else if(idx==3){ return sample_cdf((float[])XST[36:48], u_rand); }
            else if(idx==4){ return sample_cdf((float[])XST[48:60], u_rand); }
            else if(idx==5){ return sample_cdf((float[])XST[60:72], u_rand); }
            else if(idx==6){ return sample_cdf((float[])XST[72:84], u_rand); }
            else if(idx==7){ return sample_cdf((float[])XST[84:96], u_rand); }
            else if(idx==8){ return sample_cdf((float[])XST[96:108], u_rand); }
            else if(idx==9){ return sample_cdf((float[])XST[108:120], u_rand); }
            else if(idx==10){ return sample_cdf((float[])XST[120:132], u_rand); }
            else if(idx==11){ return sample_cdf((float[])XST[132:144], u_rand); }
        }
        else if(res==13){
            if(idx==0){ return sample_cdf((float[])XST[0:13], u_rand); }
            else if(idx==1){ return sample_cdf((float[])XST[13:26], u_rand); }
            else if(idx==2){ return sample_cdf((float[])XST[26:39], u_rand); }
            else if(idx==3){ return sample_cdf((float[])XST[39:52], u_rand); }
            else if(idx==4){ return sample_cdf((float[])XST[52:65], u_rand); }
            else if(idx==5){ return sample_cdf((float[])XST[65:78], u_rand); }
            else if(idx==6){ return sample_cdf((float[])XST[78:91], u_rand); }
            else if(idx==7){ return sample_cdf((float[])XST[91:104], u_rand); }
            else if(idx==8){ return sample_cdf((float[])XST[104:117], u_rand); }
            else if(idx==9){ return sample_cdf((float[])XST[117:130], u_rand); }
            else if(idx==10){ return sample_cdf((float[])XST[130:143], u_rand); }
            else if(idx==11){ return sample_cdf((float[])XST[143:156], u_rand); }
            else if(idx==12){ return sample_cdf((float[])XST[156:169], u_rand); }
        }
        else if(res==14){
            if(idx<7){
                if(idx==0){ return sample_cdf((float[])XST[0:14], u_rand); }
                else if(idx==1){ return sample_cdf((float[])XST[14:28], u_rand); }
                else if(idx==2){ return sample_cdf((float[])XST[28:42], u_rand); }
                else if(idx==3){ return sample_cdf((float[])XST[42:56], u_rand); }
                else if(idx==4){ return sample_cdf((float[])XST[56:70], u_rand); }
                else if(idx==5){ return sample_cdf((float[])XST[70:84], u_rand); }
                else if(idx==6){ return sample_cdf((float[])XST[84:98], u_rand); }
            }
            else{
                if(idx==7){ return sample_cdf((float[])XST[98:112], u_rand); }
                else if(idx==8){ return sample_cdf((float[])XST[112:126], u_rand); }
                else if(idx==9){ return sample_cdf((float[])XST[126:140], u_rand); }
                else if(idx==10){ return sample_cdf((float[])XST[140:154], u_rand); }
                else if(idx==11){ return sample_cdf((float[])XST[154:168], u_rand); }
                else if(idx==12){ return sample_cdf((float[])XST[168:182], u_rand); }
                else if(idx==13){ return sample_cdf((float[])XST[182:196], u_rand); }
            }
        }
    }
    else if(res<21){
        if(res==15){
            if(idx<8){
                if(idx==0){ return sample_cdf((float[])XST[0:15], u_rand); }
                else if(idx==1){ return sample_cdf((float[])XST[15:30], u_rand); }
                else if(idx==2){ return sample_cdf((float[])XST[30:45], u_rand); }
                else if(idx==3){ return sample_cdf((float[])XST[45:60], u_rand); }
                else if(idx==4){ return sample_cdf((float[])XST[60:75], u_rand); }
                else if(idx==5){ return sample_cdf((float[])XST[75:90], u_rand); }
                else if(idx==6){ return sample_cdf((float[])XST[90:105], u_rand); }
                else if(idx==7){ return sample_cdf((float[])XST[105:120], u_rand); }
            }
            else{
                if(idx==8){ return sample_cdf((float[])XST[120:135], u_rand); }
                else if(idx==9){ return sample_cdf((float[])XST[135:150], u_rand); }
                else if(idx==10){ return sample_cdf((float[])XST[150:165], u_rand); }
                else if(idx==11){ return sample_cdf((float[])XST[165:180], u_rand); }
                else if(idx==12){ return sample_cdf((float[])XST[180:195], u_rand); }
                else if(idx==13){ return sample_cdf((float[])XST[195:210], u_rand); }
                else if(idx==14){ return sample_cdf((float[])XST[210:225], u_rand); }
            }
        }
        else if(res==16){
            if(idx<8){
                if(idx==0){ return sample_cdf((float[])XST[0:16], u_rand); }
                else if(idx==1){ return sample_cdf((float[])XST[16:32], u_rand); }
                else if(idx==2){ return sample_cdf((float[])XST[32:48], u_rand); }
                else if(idx==3){ return sample_cdf((float[])XST[48:64], u_rand); }
                else if(idx==4){ return sample_cdf((float[])XST[64:80], u_rand); }
                else if(idx==5){ return sample_cdf((float[])XST[80:96], u_rand); }
                else if(idx==6){ return sample_cdf((float[])XST[96:112], u_rand); }
                else if(idx==7){ return sample_cdf((float[])XST[112:128], u_rand); }
            }
            else{
                if(idx==8){ return sample_cdf((float[])XST[128:144], u_rand); }
                else if(idx==9){ return sample_cdf((float[])XST[144:160], u_rand); }
                else if(idx==10){ return sample_cdf((float[])XST[160:176], u_rand); }
                else if(idx==11){ return sample_cdf((float[])XST[176:192], u_rand); }
                else if(idx==12){ return sample_cdf((float[])XST[192:208], u_rand); }
                else if(idx==13){ return sample_cdf((float[])XST[208:224], u_rand); }
                else if(idx==14){ return sample_cdf((float[])XST[224:240], u_rand); }
                else if(idx==15){ return sample_cdf((float[])XST[240:256], u_rand); }
            }
        }
        else if(res==17){
            if(idx<9){
                if(idx==0){ return sample_cdf((float[])XST[0:17], u_rand); }
                else if(idx==1){ return sample_cdf((float[])XST[17:34], u_rand); }
                else if(idx==2){ return sample_cdf((float[])XST[34:51], u_rand); }
                else if(idx==3){ return sample_cdf((float[])XST[51:68], u_rand); }
                else if(idx==4){ return sample_cdf((float[])XST[68:85], u_rand); }
                else if(idx==5){ return sample_cdf((float[])XST[85:102], u_rand); }
                else if(idx==6){ return sample_cdf((float[])XST[102:119], u_rand); }
                else if(idx==7){ return sample_cdf((float[])XST[119:136], u_rand); }
                else if(idx==8){ return sample_cdf((float[])XST[136:153], u_rand); }
            }
            else{
                if(idx==9){ return sample_cdf((float[])XST[153:170], u_rand); }
                else if(idx==10){ return sample_cdf((float[])XST[170:187], u_rand); }
                else if(idx==11){ return sample_cdf((float[])XST[187:204], u_rand); }
                else if(idx==12){ return sample_cdf((float[])XST[204:221], u_rand); }
                else if(idx==13){ return sample_cdf((float[])XST[221:238], u_rand); }
                else if(idx==14){ return sample_cdf((float[])XST[238:255], u_rand); }
                else if(idx==15){ return sample_cdf((float[])XST[255:272], u_rand); }
                else if(idx==16){ return sample_cdf((float[])XST[272:289], u_rand); }
            }
        }
        else if(res==18){
            if(idx<9){
                if(idx==0){ return sample_cdf((float[])XST[0:18], u_rand); }
                else if(idx==1){ return sample_cdf((float[])XST[18:36], u_rand); }
                else if(idx==2){ return sample_cdf((float[])XST[36:54], u_rand); }
                else if(idx==3){ return sample_cdf((float[])XST[54:72], u_rand); }
                else if(idx==4){ return sample_cdf((float[])XST[72:90], u_rand); }
                else if(idx==5){ return sample_cdf((float[])XST[90:108], u_rand); }
                else if(idx==6){ return sample_cdf((float[])XST[108:126], u_rand); }
                else if(idx==7){ return sample_cdf((float[])XST[126:144], u_rand); }
                else if(idx==8){ return sample_cdf((float[])XST[144:162], u_rand); }
            }
            else{
                if(idx==9){ return sample_cdf((float[])XST[162:180], u_rand); }
                else if(idx==10){ return sample_cdf((float[])XST[180:198], u_rand); }
                else if(idx==11){ return sample_cdf((float[])XST[198:216], u_rand); }
                else if(idx==12){ return sample_cdf((float[])XST[216:234], u_rand); }
                else if(idx==13){ return sample_cdf((float[])XST[234:252], u_rand); }
                else if(idx==14){ return sample_cdf((float[])XST[252:270], u_rand); }
                else if(idx==15){ return sample_cdf((float[])XST[270:288], u_rand); }
                else if(idx==16){ return sample_cdf((float[])XST[288:306], u_rand); }
                else if(idx==17){ return sample_cdf((float[])XST[306:324], u_rand); }
            }
        }
        else if(res==19){
            if(idx<10){
                if(idx==0){ return sample_cdf((float[])XST[0:19], u_rand); }
                else if(idx==1){ return sample_cdf((float[])XST[19:38], u_rand); }
                else if(idx==2){ return sample_cdf((float[])XST[38:57], u_rand); }
                else if(idx==3){ return sample_cdf((float[])XST[57:76], u_rand); }
                else if(idx==4){ return sample_cdf((float[])XST[76:95], u_rand); }
                else if(idx==5){ return sample_cdf((float[])XST[95:114], u_rand); }
                else if(idx==6){ return sample_cdf((float[])XST[114:133], u_rand); }
                else if(idx==7){ return sample_cdf((float[])XST[133:152], u_rand); }
                else if(idx==8){ return sample_cdf((float[])XST[152:171], u_rand); }
                else if(idx==9){ return sample_cdf((float[])XST[171:190], u_rand); }
            }
            else{
                if(idx==10){ return sample_cdf((float[])XST[190:209], u_rand); }
                else if(idx==11){ return sample_cdf((float[])XST[209:228], u_rand); }
                else if(idx==12){ return sample_cdf((float[])XST[228:247], u_rand); }
                else if(idx==13){ return sample_cdf((float[])XST[247:266], u_rand); }
                else if(idx==14){ return sample_cdf((float[])XST[266:285], u_rand); }
                else if(idx==15){ return sample_cdf((float[])XST[285:304], u_rand); }
                else if(idx==16){ return sample_cdf((float[])XST[304:323], u_rand); }
                else if(idx==17){ return sample_cdf((float[])XST[323:342], u_rand); }
                else if(idx==18){ return sample_cdf((float[])XST[342:361], u_rand); }
            }
        }
        else if(res==20){
            if(idx<10){
                if(idx==0){ return sample_cdf((float[])XST[0:20], u_rand); }
                else if(idx==1){ return sample_cdf((float[])XST[20:40], u_rand); }
                else if(idx==2){ return sample_cdf((float[])XST[40:60], u_rand); }
                else if(idx==3){ return sample_cdf((float[])XST[60:80], u_rand); }
                else if(idx==4){ return sample_cdf((float[])XST[80:100], u_rand); }
                else if(idx==5){ return sample_cdf((float[])XST[100:120], u_rand); }
                else if(idx==6){ return sample_cdf((float[])XST[120:140], u_rand); }
                else if(idx==7){ return sample_cdf((float[])XST[140:160], u_rand); }
                else if(idx==8){ return sample_cdf((float[])XST[160:180], u_rand); }
                else if(idx==9){ return sample_cdf((float[])XST[180:200], u_rand); }
            }
            else{
                if(idx==10){ return sample_cdf((float[])XST[200:220], u_rand); }
                else if(idx==11){ return sample_cdf((float[])XST[220:240], u_rand); }
                else if(idx==12){ return sample_cdf((float[])XST[240:260], u_rand); }
                else if(idx==13){ return sample_cdf((float[])XST[260:280], u_rand); }
                else if(idx==14){ return sample_cdf((float[])XST[280:300], u_rand); }
                else if(idx==15){ return sample_cdf((float[])XST[300:320], u_rand); }
                else if(idx==16){ return sample_cdf((float[])XST[320:340], u_rand); }
                else if(idx==17){ return sample_cdf((float[])XST[340:360], u_rand); }
                else if(idx==18){ return sample_cdf((float[])XST[360:380], u_rand); }
                else if(idx==19){ return sample_cdf((float[])XST[380:400], u_rand); }
            }
        }
    }

    /*
    else{
        // The following is what it should have been if there was not a bug in Houdini.
        // [Bug ID# 124486], SideFX Support Ticket [SESI #128304]
        int sl=idx*(int)res; return sample_cdf((float[])XST[sl:sl+(int)res], u_rand);
    }
    */

    return idx;

}



#endif