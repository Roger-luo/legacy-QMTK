#include <stdio.h>
#include <stdlib.h>
#include <complex.h>

typedef struct State
{
  double _Complex *amp;
  long *size;
  long nDimension;
  long nparticle;
};

extern State *State_new(void);
extern State *State_newWithSize(long nparticle);
extern State *State_newWithAmp(double _Complex *amp, long *size, long nDimension, long nparticle);
extern State *State_newWithAmp1D(double _Complex *amp, long nparticle);
extern State *State_newWithAmp2D(double _Complex *amp, long nparticle);
