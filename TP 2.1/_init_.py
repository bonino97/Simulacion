import numpy as np
from generadores import GeneradorGCL
from generadores import GeneradorMiddleSquare
from os import system, name

def clearScreen():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def muestraNumpy(n, seed, rango):
    np.random.seed(seed)
    array = np.zeros(n, dtype=int)
    for i in range(n):
        array[i] = np.random.randint(rango[0], rango[1])
    return array

if __name__ == "__main__":
    clearScreen()
    rango = [1, 50]
    print("BIENVENIDO A LA SIMULACIÓN DE NÚMEROS PSEUDOALEATORIOS.")
    seed = int(float(input("Ingrese una semilla: ")))
    print("A continuación generaremos números aleatorioos con esa semilla, comparando dos métodos con el generador de Numpy")
    #Numpy
    print("Comparando 3 muestras del generador de Numpy con la misma semilla")
    print(muestraNumpy(5, seed, rango))
    print(muestraNumpy(5, seed, rango))
    print(muestraNumpy(5, seed, rango))
    #GCL
    print("Comparando 3 muestras del generador de GCL con la misma semilla")
    generadorGCL = GeneradorGCL(seed)
    print(generadorGCL.muestra(5, rango))
    print(generadorGCL.muestra(5, rango))
    print(generadorGCL.muestra(5, rango))
    #Middle-Square
    print("Comparando 3 muestras del generador de medios del cuadrado con la misma semilla")
    generadorMQ = GeneradorMiddleSquare(seed)
    print(generadorMQ.muestra(5, rango))
    print(generadorMQ.muestra(5, rango))
    print(generadorMQ.muestra(5, rango))
