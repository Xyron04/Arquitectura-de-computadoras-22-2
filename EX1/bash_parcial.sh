#!/bin/bash #
nasm -f elf64 contrast_simd.asm -o contrast_simd.o
nasm -f elf64 contrast_asm.asm -o contrast_asm.o
gcc -c -fpic lib_cs.c -o lib_cs.o
gcc -shared lib_cs.o contrast_asm.o contrast_simd.o -o lib_cs.so
python3 programa.py