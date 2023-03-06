;parcial_asm

global contrast_asm
    section .text

;rdi <- matriz_in[0] int 32
;rsi <- matriz_out[0] int 32
;rdx <- Imatriz_max
;rcx <- Imin_cs
;r8 <-  Imax_cs
;r9 <- N

;void algoritmo_c(int *matriz_in, int *matriz_out, int Imatriz_max, int Imin_cs, int Imax_cs, int N){
;    for (int i=0; i<N; i++){
;            double help = ((double)Imax_cs-(double)Imin_cs)/(double)Imatriz_max;
;            matriz_out[i]= round(ceil((matriz_in[i])*help +Imin_cs));
;    }
;}
contrast_asm:
    xorpd xmm0, xmm0
    xorpd xmm1, xmm1
    xorpd xmm2, xmm2
    cvtsi2ss xmm0, r8   ;Imax
    cvtsi2ss xmm1, rcx  ;Imin
    cvtsi2ss xmm2, rdx  ;Imatriz_max   
    subss xmm0, xmm1
    divss xmm0, xmm2 ; help (float)
    mov r10, 0
    
bucle_i:
    xorpd xmm2, xmm2
    mov r15d, DWORD[rdi+4*r10]
    cvtsi2ss xmm2, r15  ;matriz_in[i] float
    mulss xmm2, xmm0    ;matriz_in[i] * help
    addss xmm2, xmm1    ;+Imin
    cvtss2si eax, xmm2 ;round    
    mov [rsi+4*r10], eax    ;guardo en matriz_out
    add r10, 1
    dec r9
    jnz bucle_i
fin: 
    ret

;nasm -f elf64 contrast_asm.asm -o contrast_asm.o