#ifndef AQC_EXPMV
#define AQC_EXPMV

#include "expmv.h"

TH_EXTERNC void dscal_(int *n, double *a, double *x, int *incx);
TH_EXTERNC void sscal_(int *n, float *a, float *x, int *incx);

TH_EXTERNC void dcopy_(int *n, double *x, int *incx, double *y, int *incy);
TH_EXTERNC void scopy_(int *n, float *x, int *incx, float *y, int *incy);

TH_EXTERNC void daxpy_(int *n, double *a, double *x, int *incx, double *y,
                       int *incy);
TH_EXTERNC void saxpy_(int *n, float *a, float *x, int *incx, float *y,
                       int *incy);

TH_EXTERNC double ddot_(int *n, double *x, int *incx, double *y, int *incy);
TH_EXTERNC ffloat sdot_(int *n, float *x, int *incx, float *y, int *incy);
TH_EXTERNC void dgemv_(char *trans, int *m, int *n, double *alpha, double *a,
                       int *lda, double *x, int *incx, double *beta, double *y,
                       int *incy);
TH_EXTERNC void sgemv_(char *trans, int *m, int *n, float *alpha, float *a,
                       int *lda, float *x, int *incx, float *beta, float *y,
                       int *incy);

/*
copied from stackoverflow:

https://stackoverflow.com/questions/13094224/a-c-routine-to-round-a-float-to-n-significant-digits

*/

float fsignif(float value, int digits)
{
    if (value == 0.0) // otherwise it will return 'nan' due to the log10() of zero
        return 0.0;

    float factor = powf(10.0, digits - ceilf(log10f(fabsf(value))));
    return roundf(value * factor) / factor;
}

void fcopy(int n, float *dest, float *src, int inc)
{
  int i;
  for(i=0;i<n;i++)
  {
    dest[i * inc_d] = src[i * inc_s];
  }
}

float fnorm(char trans, long m, long n, float *A);
double dnorm(char trans, long m, long n, double *A);
float complex cnorm(char trans, long m, long n, float _Complex *A);
double complex znorm(char trans, long m, long n, double _Complex *A);


// exp(t * A) v
float fexpmv(
  char trans, // trans: 'T', 'N'
  long n, // size of square matrix A
  float t,
  float *A,
  long lda, // leading dim of A
  float *v,
  long incv,
  float *w,
  long incw,
  float tol, // tolerance
  int threshold // krylov subspace threshold, should set to 30
){
  int i, mx, keylov_size, inc;
  float anorm, beta, r, fact, tau, beta_;

  inc = 1;
  keylov_size = MIN(threshold, n); // size of Krylov subspace

  anorm = fnorm_inf(tran, n, n, A);
  rndoff = anorm * FLT_EPSILON;

  // estimate first time-step and round to two significant digits
  beta = norm(n, v, incv);
  r = 1.0/keylov_size;
  fact = powf((keylov_size+1)/expf(1.), keylov_size+1);
  fact *= sqrt(2.*M_PI*(keylov_size+1));
  tau = (1./anorm)*((fact*tol)/(4.*beta*anorm))^r;
  tau = fsignif(tau, 2);

  // storage for Krylov subspace vectors
  float **vm = (float **)malloc((keylov_size+1) * sizeof(float *));
  for(i=0;i<m+1;i++)
  {
    vm[i] = (float *)calloc(n, sizeof(float)); // similar(w)
  }

  float *hm = (float *)calloc((keylov_size+2) * (keylov_size+2), sizeof(float));

  tf = fabsf(t);
  tsgn = SIGN(t);
  tk = 0.0f; // float zero

  // copy!(w, v)
  scopy_(&n, w, &inc, v, &inc);
  float *p = (float *)calloc(n, sizeof(float));
  mx = keylov_size;

  while(tk < tf) {
    tau = MIN(tf-tk, tau);

    // Arnoldi procedure
    // vm[1] = v/beta
    scopy_(&n, vm[1], &inc, w, &inc);
    beta_ = 1.0/beta;
    sscal_(&n, &beta_, vm[1], &inc);

    mx = keylov_size;
    for(j=0;j< keylov_size;j++)
    {
      // gemv(A, vm[j])
      
    }
  }
}

#endif