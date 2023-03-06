;contrast_simd

global contrast_simd
    section .text

;rdi <- matriz_in[0] int 32
;rsi <- matriz_out[0] int 32
;rdx <- Imatriz_max, Imin_cs, Imax_cs  
;rcx <- help simd mul
;r8 <- help simd resta
;r9 <- N
;void algoritmo_c(int *matriz_in, int *matriz_out, int Imatriz_max, int Imin_cs, int Imax_cs, int N){
;    for (int i=0; i<N; i++){
;            double help = ((double)Imax_cs-(double)Imin_cs)/(double)Imatriz_max;
;            matriz_out[i]= round(matriz_in[i]*help +Imin_cs));
;    }
;}
contrast_simd:
    xorpd xmm0, xmm0
    xorpd xmm1, xmm1
    xorpd xmm2, xmm2
    xorpd xmm3, xmm3
    mov r12, 16
    cvtsi2ss xmm2, [rdx]  ;Imatriz_max
    cvtsi2ss xmm0, [rdx+4]   ;Imax
    cvtsi2ss xmm1, [rdx+8]  ;Imin
      
    subss xmm0, xmm1
    divss xmm0, xmm2 ; help (float)
    movss [rcx], xmm0
    movss [rcx+4], xmm0
    movss [rcx+8], xmm0
    movss [rcx+12], xmm0
    xorpd xmm0, xmm0
    movups xmm0, [rcx]    ; mover 4 floats desde rcx al registro xmm0
    mov r10, 0
    movss [r8], xmm1
    movss [r8+4], xmm1
    movss [r8+8], xmm1
    movss [r8+12], xmm1
    xorpd xmm1, xmm1
    movups xmm1, [r8] 

bucle_i:
    xorpd xmm3, xmm3
    movups xmm3, [rdi]
    add rdi, r12
    cvtdq2ps xmm3,xmm3  ;convierto 4 floats
    mulps xmm3, xmm0    ;matriz_in[i] * help
    addps xmm3, xmm1    ;+Imin
    xorpd xmm4, xmm4
    CVTPS2DQ xmm4, xmm3 ;round     
    movups [rsi], xmm4    ;guardo en matriz_out
    add rsi, r12   
    add r10, 1
    sub r9, 4
    jnz bucle_i

fin: 
    ret

;nasm -f elf64 simdprueba_asm.asm -o simdprueba_asm.o -g
;gcc -c -fpic prueba_c.c -o prueba_c.o
;gcc prueba_asm.o prueba_c.o simdprueba_asm.o -o prueba_c_asm -lm -g
;gdb ./prueba_c_asm
;set disassembly-flavor
;info registers r12 r13 r14 r15