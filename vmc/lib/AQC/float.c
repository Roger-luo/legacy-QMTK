#include <stdio.h>
#include <float.h>
#include <math.h>

float fsignif(float value, int digits)
{
    if (value == 0.0) // otherwise it will return 'nan' due to the log10() of zero
        return 0.0;

    float factor = powf(10.0, digits - ceilf(log10f(fabsf(value))));
    return roundf(value * factor) / factor;
}

int main(){
  printf("%.10lf\n", fsignif(123.456, 2));
}