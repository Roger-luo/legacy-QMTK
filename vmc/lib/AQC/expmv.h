#ifndef AQC_EXPMV
#define AQC_EXPMV

#include "General.h"

// safety factors
#define EXPMV_GAMMA = 0.9
#define EXPMV_DELTA = 1.2
#define EXPMV_BTOL = 1e-7 // tolerance for "happy-breakdown"
#define EXPMV_MAXITER = 10 // max number of time-step refinements

float fnorm(char trans, long m, long n, float *A);
double dnorm(char trans, long m, long n, double *A);
float complex cnorm(char trans, long m, long n, float _Complex *A);
double complex znorm(char trans, long m, long n, double _Complex *A);

float fexpmv(char trans, long m, long n, float t, float *A, long lda, float *v, long incv, float *w, long incw, float tol, int m);
double dexpmv(char trans, long m, long n, double t, double *A, long lda, double *v, long incv, double *w, long incw, double tol, int m);
float _Complex cexpmv(char trans, long m, long n, float _Complex t, float _Complex *A, long lda, float _Complex *v, long incv, float _Complex *w, long incw, float _Complex tol, int m);
double _Complex zexpmv(char trans, long m, long n, double _Complex t, double _Complex *A, long lda, double _Complex *v, long incv, double _Complex *w, long incw, double _Complex tol, int m);



#endif