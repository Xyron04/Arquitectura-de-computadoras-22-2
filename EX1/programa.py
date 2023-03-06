#Examen Parcial
#Alumno: Gerard Calderón Anyosa
#Código: 20190200
#bash bash_parcial.sh
from telnetlib import SUPPRESS_LOCAL_ECHO
import numpy as np
import ctypes
import time
from statistics import mean, median
import matplotlib.pyplot as plt

def filtro_mediana(sign, w):
    signc = []
    lc = sign+sign+sign
    ii = len(sign)
    for i in range(len(sign)):
        izq = i + ii - w//2
        der = i + ii + w//2
        signc.append(median(lc[izq:der+1]))
    return signc

def algoritmo_py(matriz_in, matriz_out, Imatriz_max, Imin_cs, Imax_cs, N):
    for i in range (0,N):
            matriz_out[i]= round((matriz_in[i])*(Imax_cs-Imin_cs)/Imatriz_max+Imin_cs)
        
if __name__ == '__main__':
    Imin_cs = 4
    Imax_cs = 10
    Imatriz_max = 15
    N = 4
    N_2 = N*N
    matriz = np.array([14,10,9,7,12,15,13,14,4,9,0,3,2,3,3,0], dtype = np.intc)
    matriz_in = np.reshape(matriz,(N,N))
    print(matriz_in)
    matriz_out_py = np.zeros_like(matriz)
    print("Salida en python")
    algoritmo_py(matriz, matriz_out_py, Imatriz_max, Imin_cs, Imax_cs, N_2)
    matriz_out_PY = np.reshape(matriz_out_py,(N,N))
    print(matriz_out_PY)


    #En C:
    lib = ctypes.CDLL('./lib_cs.so')
    lib.algoritmo_c.argtypes = [
        np.ctypeslib.ndpointer(dtype=np.intc),
        np.ctypeslib.ndpointer(dtype=np.intc),
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int
    ]

    matriz_out_c = np.zeros_like(matriz)
    lib.algoritmo_c(matriz, matriz_out_c, Imatriz_max, Imin_cs, Imax_cs, N_2)
    matriz_out_C = np.reshape(matriz_out_c,(N,N))
    print("Salida en C")
    print(matriz_out_C)

    #En ASM:
    matriz_out_asm = np.zeros_like(matriz)
    lib.contrast_asm.argtypes = [
        np.ctypeslib.ndpointer(dtype=np.intc),
        np.ctypeslib.ndpointer(dtype=np.intc),
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int
    ]
    lib.contrast_asm(matriz, matriz_out_asm, Imatriz_max, Imin_cs, Imax_cs, N_2)
    matriz_out_ASM = np.reshape(matriz_out_asm,(N,N))
    print("Salida en ASM")
    print(matriz_out_ASM)
#En SIMD:
    matriz_out_simd = np.zeros_like(matriz)
    lib.contrast_simd.argtypes = [
        np.ctypeslib.ndpointer(dtype=np.intc),
        np.ctypeslib.ndpointer(dtype=np.intc),
        np.ctypeslib.ndpointer(dtype=np.intc),
        np.ctypeslib.ndpointer(dtype=np.intc),
        np.ctypeslib.ndpointer(dtype=np.intc),
        ctypes.c_int
    ]
    def_values = np.array([Imatriz_max, Imax_cs, Imin_cs], dtype=np.intc)
    help_SIMD_mul = np.zeros((4,), dtype=np.intc)
    help_SIMD_resta = np.zeros((4,), dtype=np.intc)
    lib.contrast_simd(matriz_in, matriz_out_simd, def_values, help_SIMD_mul, help_SIMD_resta, N)
    matriz_out_SIMD = np.reshape(matriz_out_asm,(N,N))
    print("Salida en SIMD")
    print(matriz_out_SIMD)
    
    print("\n Prueba de rendimiento:")
    #prueba de rendimiento:
    tcontrast_py =[]
    tcontrast_c = []
    tcontrast_asm = []
    tcontrast_simd = []
    ns = [4,16,64,256,1024]
    veces = 15

    for n in ns:
        tcontrasti_py = []
        tcontrasti_c = []
        tcontrasti_asm = []
        tcontrasti_simd = []
        for j in range(veces):
            tam = n**2
            matriz_prueba = np.random.randint(Imatriz_max, size = tam, dtype = np.intc)
            out_prueba_c = np.zeros_like(matriz_prueba)
            out_prueba_py = np.zeros_like(matriz_prueba)
            out_prueba_asm = np.zeros_like(matriz_prueba)
            out_prueba_simd = np.zeros_like(matriz_prueba)
            def_values_prueba = np.array([Imatriz_max, Imax_cs, Imin_cs], dtype=np.intc)
            help_SIMD_mul_prueba = np.zeros((4,), dtype=np.intc)
            help_SIMD_resta_prueba = np.zeros((4,), dtype=np.intc)

            #tiempo Py
            t = time.time()
            algoritmo_py(matriz_prueba, out_prueba_py, Imatriz_max, Imin_cs, Imax_cs, tam)
            tcontrasti_py.append(time.time() - t)
            
            #tiempo C
            t = time.time()
            lib.algoritmo_c(matriz_prueba, out_prueba_c, Imatriz_max, Imin_cs, Imax_cs, tam)
            tcontrasti_c.append(time.time() - t)

            #tiempo ASM
            t = time.time()
            lib.contrast_asm(matriz_prueba, out_prueba_asm, Imatriz_max, Imin_cs, Imax_cs, tam)
            tcontrasti_asm.append(time.time() - t)

            #tiempo SIMD
            t = time.time()
            lib.contrast_simd(matriz_prueba, out_prueba_simd, def_values, help_SIMD_mul, help_SIMD_resta, tam)
            tcontrasti_simd.append(time.time() - t)
            
        tcontrast_py.append(mean(filtro_mediana(tcontrasti_py,9)))
        tcontrast_c.append(mean(filtro_mediana(tcontrasti_c,9)))
        tcontrast_asm.append(mean(filtro_mediana(tcontrasti_asm,9)))
        tcontrast_simd.append(mean(filtro_mediana(tcontrasti_simd,9)))

    plt.plot(ns, tcontrast_py, 'r-o', label='Tiempo Python')
    plt.plot(ns, tcontrast_c, 'g-o', label='Tiempo C')
    plt.plot(ns, tcontrast_asm, 'c-o', label='Tiempo ASM')
    plt.plot(ns, tcontrast_simd, 'y-o', label='Tiempo SIMD')
    plt.title('Efectos arquitectura')
    plt.xlabel('tamagno')
    plt.ylabel('tiempo promedio')
    plt.legend()
    plt.show() 
    plt.savefig("Tiempo.png")
    
    plt.close()

    
    Sup_C = [i/j for i,j in zip (tcontrast_py,tcontrast_c)]
    Sup_ASM = [i/j for i,j in zip (tcontrast_py,tcontrast_asm)]
    Sup_SIMD = [i/j for i,j in zip (tcontrast_py,tcontrast_simd)]

    plt.plot(ns, Sup_C, 'b-o', label='Su_C')
    plt.plot(ns, Sup_ASM, 'r-+', label='Su_ASM')
    plt.plot(ns, Sup_SIMD, 'g-o', label='Su_SIMD')
    plt.title('speedup por tamagno')
    plt.xlabel('tamagno')
    plt.ylabel('speedup')
    plt.legend()
    plt.show()
    plt.savefig("Speed_up.png")

    print("tiempo_py")
    print(tcontrast_py)
    print("tiempo_c")
    print(tcontrast_c)
    print("tiempo_asm")
    print(tcontrast_asm)
    print("tiempo_simd")
    print(tcontrast_simd)
    
    

