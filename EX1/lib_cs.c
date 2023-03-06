#include<math.h>
#include <stdio.h>
//lib_cs.c Gerard Calderón
extern void contrast_asm(int *matriz_in, int *matriz_out, int Imatriz_max, int Imin_cs, int Imax_cs, int N);
extern void contrast_simd(int *matriz_in, int *matriz_out, int *def_values, float *help_SIMD_mul, float *help_SIMD_resta, int N);

void algoritmo_c(int *matriz_in, int *matriz_out, int Imatriz_max, int Imin_cs, int Imax_cs, int N){
    double help = ((double)Imax_cs-(double)Imin_cs)/(double)Imatriz_max;
    for (int i=0; i<N; i++){
            matriz_out[i]= round((matriz_in[i])*help +Imin_cs);
    }
}

//Sin ASM
//gcc -c -fpic lib_cs.c -o lib_cs.o
//gcc -shared lib_cs.o -o lib_cs.so

//Con ASM
//gcc -c -fpic lib_cs.c -o lib_cs.o
//gcc -shared lib_cs.o contrast_asm.o -o lib_cs.so