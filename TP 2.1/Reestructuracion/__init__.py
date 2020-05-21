import numpy as np
import random as rand

from Generadores.GCL.GeneradorGCL import GeneradorGCL

from Generadores.MiddleSquare import GeneradorMiddleSquare
from Generadores.NumPy import GeneradorNumPy
from Generadores.System import GeneradorSystem 

from Tests import *

from os import system, name
from terminaltables import AsciiTable


def ClearScreen():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

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
    ClearScreen()
    print("BIENVENIDO A LA SIMULACIÓN DE NÚMEROS PSEUDOALEATORIOS.")
    seed = int(float(input("Ingrese una semilla: ")))
    
    #Random(Python)
    muestra = GeneradorSystem(seed).muestra(1000)
    testear(muestra, "Random(Python)")
    #Numpy
    muestra = GeneradorNumPy(seed).muestra(1000)
    testear(muestra, "Numpy")
    #GCL
    muestra =  GeneradorGCL(seed).muestra(1000)
    testear(muestra, "Generador GCL")
    #Middle-Square
    muestra = GeneradorMiddleSquare(seed).muestra(1000)
    testear(muestra, "Generador Middle Square")


    