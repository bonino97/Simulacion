import numpy as np
import random as rand

from os import system, name
from terminaltables import AsciiTable

from Generadores.GCL import GeneradorGCL
from Generadores.MiddleSquare import GeneradorMiddleSquare
from Generadores.NumPy import GeneradorNumPy
from Generadores.System import GeneradorSystem 

from Tests.ChiCuadrado import ChiCuadrado
from Tests.KolmogorovSmirnov import KolmogorovSmirnov
from Tests.Paridad import Paridad

def ClearScreen():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def Testear(muestra, tipo):
    
    DataTable = [
        ['Test ' + tipo, 'Resultado']
    ]

    print("Realizando tests para la muestra generada por " + tipo)

    print("Test de Kolmogorov Smirnov: ")
    result = KolmogorovSmirnov.Test(muestra)
    DataTable.append(["Kolmogorov Smirnov", result])

    print("Test de Chi Cuadrado: ")
    result = ChiCuadrado.Test(muestra)
    DataTable.append(["Chi Cuadrado", result])

    print("Test de Paridad:")
    result = Paridad.Test(muestra)
    DataTable.append(["Test de Paridad", result])

    table = AsciiTable(DataTable)
    print(table.table)

if __name__ == "__main__":

    ClearScreen()

    print("BIENVENIDO A LA SIMULACIÓN DE NÚMEROS PSEUDOALEATORIOS.")
    seed = int(float(input("Ingrese una semilla: ")))
    
    #Random(Python)
    muestra = GeneradorSystem().muestra(1000, seed)
    Testear(muestra, "Generador Random(Python)")

    #Numpy
    muestra = GeneradorNumPy().muestra(1000, seed)
    Testear(muestra, "Generador Numpy")

    #GCL
    muestra = GeneradorGCL(seed).muestra(1000)
    Testear(muestra, "Generador GCL")

    #Middle-Square
    muestra = GeneradorMiddleSquare(seed).muestra(1000)
    Testear(muestra, "Generador MiddleSquare")


    