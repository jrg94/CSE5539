/*
   Auditory Peripheral Model (First developed at Univ. of Sheffield; Adapted by
   DeLiang Wang, June 1999). The program computes the following functions:
   Correlogram
   Outer Middle Ear
   Middle Ear
   Meddis hair cell model
 */

#include <stdio.h>
#include <math.h>
#include <stdlib.h>

/* booleans */

#ifndef TRUE
#define TRUE 1
#endif
#ifndef FALSE
#define FALSE 0
#endif

/* auditory filterbank constants */

#define MAX_CHANNEL         128                   /* maxmimum number of filters */
#define BW_CORRECTION       1.019           /* ERB bandwidth correction 4th order */
#define SAMPLING_FREQUENCY  16000           /* Hz */
#define MAX_DELAY     200       /* corresponds to 62.5 Hz */
#define MAX_WINDOW      320       /* use a window of 20 ms */
#define MAX_BUFFER_SIZE     MAX_DELAY+MAX_WINDOW  /* buffer size */
#define OFFSET        160       /* compute acg every 10 ms */

/* hair cell constants from Meddis 1988 paper */

#define MED_Y 5.05
#define MED_G 2000.0
#define MED_L 2500.0
#define MED_R 6580.0
#define MED_X 66.31
#define MED_A 3.0
#define MED_B 300.0
#define MED_H 48000.0
#define MED_M 1.0

/* outer/middle ear */

#define MIDDLE_EAR_SIZE 29
#define DB 60.0

/* frequency scale definitions from Moore and Glasberg 1990 */

#define erb(f) (24.7*(4.37e-3*(f)+1.0))
#define hzToERBrate(f) (21.4*log10(4.37e-3*(f)+1.0))
#define ERBrateToHz(f) ((pow(10.0,((f)/21.4))-1.0)/4.37e-3)
#define sqr(x) ((x)*(x))

typedef struct {
        double cf, bw, criticalRate, z, gain, expCoeff;
        double midEarCoeff;
        double p0, p1, p2, p3, p4;
        double q0, q1, q2, q3, q4;
        double u0, u1;
        double v0, v1;
        double c,q,w;
        double rate;
        double buffer[MAX_BUFFER_SIZE];
        int ptr;
} channel;

/* function prototypes */

void help(void);
/* UNIX help */

void blip(void);
/* write dots on stderr */

void initHairCells(void);
/* initialise the meddis hair cell parameters */

void initOuterMiddleEar(void);
/* set parameters of equal-loudness functions */

float DBtoAmplitude(float dB);
/* convert dB to amplitude */

float loudnessLevelInPhons(float dB, float freq);
/* compute loudness level */

void initChannels(int lowerCF, int upperCF, int numChannels);
/* initialise filterbank channels */

void updateCochlea(channel *c, float sigval, int tim);
/* process one sample of the input though the cochlea */

int msToSamples(float ms);
/* converts time in ms to samples at srate */

/* global variables */

channel cochlea[MAX_CHANNEL];

double acg[MAX_DELAY][MAX_CHANNEL];

float t, dt, twoPi, twoPiT, vmin, k, l;
short verboseOutput=FALSE;
double ymdt, xdt, ydt, lplusrdt, rdt, gdt, hdt;

/* outer/middle ear stuff */

float f[MIDDLE_EAR_SIZE];
float af[MIDDLE_EAR_SIZE];
float bf[MIDDLE_EAR_SIZE];
float tf[MIDDLE_EAR_SIZE];

/* function declarations */

void help(void)
{
        fprintf(stderr,"-l int  lowest filter centre frequency (Hz) (500)\n");
        fprintf(stderr,"-u int  highest filter centre frequency (Hz) (2000)\n");
        fprintf(stderr,"-n int  number of channels (32)\n");
        fprintf(stderr,"-a string name of left input file\n");
        fprintf(stderr,"-b string name of right input file\n");
        fprintf(stderr,"-d float buffer decay time in ms (20.0)\n");
        fprintf(stderr,"-v bool verbose output (FALSE)\n");
}

void blip(void)
{
        static int count=0;

        fprintf(stderr,".");
        count+=1;
        if (count>32) count=0;
}

void initHairCells(void)
{
        ymdt=MED_Y*MED_M*dt;
        fprintf(stderr,"ymdt=%f\n",ymdt);
        xdt=MED_X*dt;
        fprintf(stderr,"xdt=%f\n",xdt);
        ydt=MED_Y*dt;
        fprintf(stderr,"ydt=%f\n",ydt);
        lplusrdt=(MED_L+MED_R)*dt;
        fprintf(stderr,"lplusrdt=%f\n", lplusrdt);
        rdt=MED_R*dt;
        fprintf(stderr,"rdt=%f\n",rdt);
        gdt=MED_G*dt;
        fprintf(stderr,"gdt=%f\n",gdt);
        hdt=MED_H; /* should be multiplied by ts really */
        fprintf(stderr,"hdt=%f\n",hdt);
}

void initOuterMiddleEar(void)
/*
   parameters of equal-loudness functions from BS3383,"Normal equal-loudness level
   contours for pure tones under free-field listening conditions", table 1.
   f is the tone frequency
   af and bf are frequency-dependent coefficients
   tf is the threshold sound pressure level of the tone, in dBs
 */
{
        f[0]=20.0;     af[0]=2.347;  bf[0]=0.00561;   tf[0]=74.3;
        f[1]=25.0;     af[1]=2.190;  bf[1]=0.00527;   tf[1]=65.0;
        f[2]=31.5;     af[2]=2.050;  bf[2]=0.00481;   tf[2]=56.3;
        f[3]=40.0;     af[3]=1.879;  bf[3]=0.00404;   tf[3]=48.4;
        f[4]=50.0;     af[4]=1.724;  bf[4]=0.00383;   tf[4]=41.7;
        f[5]=63.0;     af[5]=1.579;  bf[5]=0.00286;   tf[5]=35.5;
        f[6]=80.0;     af[6]=1.512;  bf[6]=0.00259;   tf[6]=29.8;
        f[7]=100.0;    af[7]=1.466;  bf[7]=0.00257;   tf[7]=25.1;
        f[8]=125.0;    af[8]=1.426;  bf[8]=0.00256;   tf[8]=20.7;
        f[9]=160.0;    af[9]=1.394;  bf[9]=0.00255;   tf[9]=16.8;
        f[10]=200.0;   af[10]=1.372; bf[10]=0.00254;  tf[10]=13.8;
        f[11]=250.0;   af[11]=1.344; bf[11]=0.00248;  tf[11]=11.2;
        f[12]=315.0;   af[12]=1.304; bf[12]=0.00229;  tf[12]=8.9;
        f[13]=400.0;   af[13]=1.256; bf[13]=0.00201;  tf[13]=7.2;
        f[14]=500.0;   af[14]=1.203; bf[14]=0.00162;  tf[14]=6.0;
        f[15]=630.0;   af[15]=1.135; bf[15]=0.00111;  tf[15]=5.0;
        f[16]=800.0;   af[16]=1.062; bf[16]=0.00052;  tf[16]=4.4;
        f[17]=1000.0;  af[17]=1.000; bf[17]=0.00000;  tf[17]=4.2;
        f[18]=1250.0;  af[18]=0.967; bf[18]=-0.00039; tf[18]=3.7;
        f[19]=1600.0;  af[19]=0.943; bf[19]=-0.00067; tf[19]=2.6;
        f[20]=2000.0;  af[20]=0.932; bf[20]=-0.00092; tf[20]=1.0;
        f[21]=2500.0;  af[21]=0.933; bf[21]=-0.00105; tf[21]=-1.2;
        f[22]=3150.0;  af[22]=0.937; bf[22]=-0.00104; tf[22]=-3.6;
        f[23]=4000.0;  af[23]=0.952; bf[23]=-0.00088; tf[23]=-3.9;
        f[24]=5000.0;  af[24]=0.974; bf[24]=-0.00055; tf[24]=-1.1;
        f[25]=6300.0;  af[25]=1.027; bf[25]=0.00000;  tf[25]=6.6;
        f[26]=8000.0;  af[26]=1.135; bf[26]=0.00089;  tf[26]=15.3;
        f[27]=10000.0; af[27]=1.266; bf[27]=0.00211;  tf[27]=16.4;
        f[28]=12500.0; af[28]=1.501; bf[28]=0.00488;  tf[28]=11.6;
}

float DBtoAmplitude(float dB)
{
        return pow(10.0,(dB/20.0));
}

float loudnessLevelInPhons(float dB, float freq)
/*
   Uses linear interpolation of the look-up tables to compute the loudness level,
   in phons, of a pure tone of frequency freq using the reference curve for sound
   pressure level dB.
   The equation is taken from section 4 of BS3383.
 */
{
        int i=0;
        float afy, bfy, tfy;

        if ((freq<20.0) | (freq>12500.0)) {
                fprintf(stderr,"Can't compute a outer/middle ear gain for that frequency\n");
                exit(0);
        }
        while (f[i] < freq) i++;
        afy=af[i-1]+(freq-f[i-1])*(af[i]-af[i-1])/(f[i]-f[i-1]);
        bfy=bf[i-1]+(freq-f[i-1])*(bf[i]-bf[i-1])/(f[i]-f[i-1]);
        tfy=tf[i-1]+(freq-f[i-1])*(tf[i]-tf[i-1])/(f[i]-f[i-1]);
        return 4.2+afy*(dB-tfy)/(1.0+bfy*(dB-tfy));
}

void initChannels(int lowerCF, int upperCF, int numChannels)
{
        float lowerERB, upperERB, spaceERB, kt;
        channel c;
        int chan, i;

        dt = 1.0/(float)SAMPLING_FREQUENCY;
        twoPi = 2.0*M_PI;
        twoPiT = 2.0*M_PI*dt;

        lowerERB = hzToERBrate(lowerCF);
        upperERB = hzToERBrate(upperCF);

        if (numChannels > 1)
                spaceERB = (upperERB-lowerERB)/(numChannels-1);
        else
                spaceERB = 0.0;

        for (chan=0; chan<numChannels; chan++) {
                c.criticalRate = lowerERB+chan*spaceERB;
                c.cf = ERBrateToHz(c.criticalRate);
                c.midEarCoeff=DBtoAmplitude(loudnessLevelInPhons(DB,c.cf)-DB);
                c.bw = erb(c.cf)*BW_CORRECTION;
                c.z = exp(-twoPiT*c.bw);
                c.expCoeff = c.cf*twoPiT;
                c.gain = c.midEarCoeff*sqr(sqr(2*M_PI*c.bw*dt))/3.0;
                if (verboseOutput) {
                        fprintf(stderr,"cf=%1.4f:\n",c.cf);
                        fprintf(stderr,"   criticalRate=%1.4f  midEarCoeff=%1.4f  bw=%1.4f  gain=%1.4f\n",c.criticalRate,c.midEarCoeff,c.bw,c.gain);
                }
                c.p0 = 0.0; c.p1 = 0.0; c.p2 = 0.0; c.p3 = 0.0; c.p4 = 0.0;
                c.q0 = 0.0; c.q1 = 0.0; c.q2 = 0.0; c.q3 = 0.0; c.q4 = 0.0;
                c.u0 = 0.0; c.u1 = 0.0;
                c.v0 = 0.0; c.v1 = 0.0;
                kt=MED_G*MED_A/(MED_A+MED_B);
                c.c=MED_M*MED_Y*kt/(MED_L*kt+MED_Y*(MED_L+MED_R));
                c.q=c.c*(MED_L+MED_R)/kt;
                c.w=c.c*MED_R/MED_X;
                for (i = 0; i < MAX_BUFFER_SIZE; i++)
                        c.buffer[i]=0.0;
                c.ptr=MAX_BUFFER_SIZE-1;
                cochlea[chan]=c;
        }
}

void updateCochlea(channel *c, float sigval, int tim)
{
        double zz, bm, hc, pow, amp;
        double replenish, eject, reuptakeandloss, reuptake, reprocess, kt;

        zz = c->z;
        c->p0 = sigval*cos(c->expCoeff*tim)+zz*(4*c->p1-zz*(6*c->p2-zz*(4*c->p3-zz*c->p4)));
        c->q0 =-sigval*sin(c->expCoeff*tim)+zz*(4*c->q1-zz*(6*c->q2-zz*(4*c->q3-zz*c->q4)));
        c->u0 = zz*(c->p1+zz*(4*c->p2+zz*c->p3));
        c->v0 = zz*(c->q1+zz*(4*c->q2+zz*c->q3));
        bm = (c->u0*cos(c->expCoeff*tim)-c->v0*sin(c->expCoeff*tim))*c->gain;
        pow = sqr(c->u0)+sqr(c->v0);
        amp=sqrt(pow)*c->gain;

        /* hair cell */

        if ((bm+MED_A)>0.0)
                kt=gdt*(bm+MED_A)/(bm+MED_A+MED_B);
        else
                kt=0.0;
        if (c->q<MED_M )
                replenish=ymdt-ydt*c->q;
        else
                replenish=0.0;
        eject=kt*c->q;
        reuptakeandloss=lplusrdt*c->c;
        reuptake=rdt*c->c;
        reprocess=xdt*c->w;
        c->q+=replenish-eject+reprocess;
        if (c->q<0.0)
                c->q=0.0;
        c->c+=eject-reuptakeandloss;
        if (c->c<0.0)
                c->c=0.0;
        c->w+=reuptake-reprocess;
        if (c->w<0.0)
                c->w=0.0;
        hc = hdt*c->c;

        /* filter coefficients */

        c->p4 = c->p3; c->p3 = c->p2; c->p2 = c->p1; c->p1 = c->p0;
        c->q4 = c->q3; c->q3 = c->q2; c->q2 = c->q1; c->q1 = c->q0;
        c->u1 = c->u0; c->v1 = c->v0;

        c->ptr++;
        if (c->ptr==MAX_BUFFER_SIZE) c->ptr=0;
        c->buffer[c->ptr]=hc;
}

double getBufferVal(channel *c, int i)
{
        int idx;
        idx=(c->ptr-i);
        if (idx<0) idx+=MAX_BUFFER_SIZE;
        return c->buffer[idx];
}

int msToSamples(float ms)
{
        return (int)((float)SAMPLING_FREQUENCY*ms/1000.0);
}

/*------------------------------------------------------*/
/* Main program */
/*------------------------------------------------------*/

void main (int argc, char **argv)
{
        int opt;
        extern char *optarg;
        int ok = TRUE;
        int chan,tim;
        int numChannels=128;
        int lowerCF=80;
        int upperCF=5000;
        double nerveVal;
        float sigVal;
        FILE *ofp;
        char fname[30];
        int frame, win, delay;
        int cat;

        while ((opt=getopt(argc,argv,"Hl:u:n:v")) != EOF) {
                switch(opt) {
                case 'H': help(); ok=FALSE; break;
                case 'l': lowerCF = atoi(optarg); break;
                case 'u': upperCF = atoi(optarg); break;
                case 'n': numChannels = atoi(optarg); break;
                case 'v': verboseOutput = TRUE; break;
                case '?': ok = FALSE;
                }
        }

        if (ok == FALSE) {
                exit(0);
        }

        initOuterMiddleEar();
        initChannels(lowerCF, upperCF, numChannels);
        initHairCells();

        /* do the filtering */

        tim=0; frame=0;
        while (scanf("%f", &sigVal) != EOF) {
                for (chan=0; chan<numChannels; chan++) {
                        updateCochlea(&cochlea[chan],sigVal,tim);
                }
                tim++;
                if ((tim % OFFSET) == 0) {
                        fprintf(stderr, "computing correlogram at T=%d\n", tim);
                        for (chan=0; chan<numChannels; chan++) {
                                for (delay=0; delay<MAX_DELAY; delay++) {
                                        acg[delay][chan]=0.0;
                                        for (win=0; win<MAX_WINDOW; win++) {
                                                acg[delay][chan] += getBufferVal(&cochlea[chan],win)*getBufferVal(&cochlea[chan],win+delay);
                                        }
                                }
                        }
                        sprintf(fname, "ACG.%03d", frame);
                        frame++;
                        fprintf(stderr, "%s\n", fname);
                        ofp = fopen(fname,"w");
                        if (ofp == NULL) {
                                fprintf(stderr, "could not open file %s\n", fname);
                                exit(0);
                        }
                        fprintf(ofp, "%d %d\n", MAX_DELAY, numChannels);
                        for (chan = 0; chan < numChannels; chan++) {
                                for (delay=0; delay<MAX_DELAY; delay++) {
                                        fprintf(ofp,"%1.2f\n",acg[delay][chan]/(MAX_WINDOW*50.0));
                                }
                        }
                        fclose(ofp);
                }
        }

        fprintf(stderr,"Done. Processed %d samples.\n",tim);
}
