import numpy as np
from terminaltables import AsciiTable
from generadores import GeneradorGCL
from generadores import GeneradorMiddleSquare
from tests import *
from os import system, name
import random as rand

def clearScreen():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def muestraNumpy(n, seed):
    np.random.seed(seed)
    array = np.zeros(n)
    for i in range(n):
        array[i] = np.random.random()
    return array

def muestraPyRandom(n, seed):
    rand.SystemRandom(seed)
    array = np.zeros(n)
    for i in range(n):
        array[i] = rand.random()
    return array

def testear(muestra, tipo):
    table_data = [
        ['Test '+tipo, 'Resultado']
    ]
    print("Realizando tests para la muestra generada por "+tipo)
    print("Test de Kolmogorov Smirnov: ")
    result = kstest(muestra)
    table_data.append(["Kolmogorov Smirnov", result])
    print("Test de Chi Cuadrado: ")
    result = chiCuadrado(muestra)
    table_data.append(["Chi Cuadrado", result])
    print("Test de Rachas Arriba y Abajo de la Media:")
    result = rachasArribaAbajoMediaTest(muestra)
    table_data.append(["Rachas Arriba y Abajo de la Media", result])
    print("Test de Paridad:")
    result = testParidad(muestra)
    table_data.append(["Test de Paridad", result])

    table = AsciiTable(table_data)
    print(table.table)

if __name__ == "__main__":
    clearScreen()
    print("BIENVENIDO A LA SIMULACIÓN DE NÚMEROS PSEUDOALEATORIOS.")
    seed = int(float(input("Ingrese una semilla: ")))
    #Random(Python)
    muestra = muestraPyRandom(1000, seed)
    testear(muestra, "Random(Python)")
    #Numpy
    muestra = muestraNumpy(1000, seed)
    testear(muestra, "Numpy")
    #GCL
    muestra =  GeneradorGCL(seed).muestra(1000)
    testear(muestra, "Generador GCL")
    #Middle-Square
    muestra = GeneradorMiddleSquare(seed).muestra(1000)
    testear(muestra, "Generador Middle Square")


    