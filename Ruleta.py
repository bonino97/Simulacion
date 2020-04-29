#! usr/bin/env python3
#_*_ coding: utf8 _*_

import random as rand
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

def grafica_frecuencia(frecuencias,frecuenciaEstimada):
    # Frecuencia Relativa
    for frecuencia in frecuencias:
        plt.plot(frecuencia)

    plt.title("Frecuencia Relativa")
    plt.axhline(frecuenciaEstimada, color='blue')
    plt.ylabel('Fr')
    plt.xlabel('Tiradas')
    plt.legend()
    plt.grid()
    plt.show()

def grafica_promedio(promedios,promedioEstimado):
    # Promedio
    for promedio in promedios:
        plt.plot(promedio)

    plt.title('Valor Promedio')
    plt.axhline(promedioEstimado, color='blue')
    plt.ylabel('Valor')
    plt.xlabel('Tiros')
    plt.legend()
    plt.grid()
    plt.show()

def grafica_desvio(desvios,desvioEstimado):
    # Desvio
    for desvio in desvios:
        plt.plot(desvio)

    plt.title('Desvío')
    plt.axhline(desvioEstimado, color='blue')
    plt.ylabel('vd')
    plt.xlabel('Tiros')
    plt.legend()
    plt.grid()
    plt.show()

def grafica_varianza(varianzas,varianzaEstimada):
    # Varianza
    for varianza in varianzas:
        plt.plot(varianza)

    plt.title('Varianza')
    plt.axhline(varianzaEstimada, color='blue')
    plt.ylabel('vr')
    plt.xlabel('Tiros')
    plt.legend()
    plt.grid()
    plt.show()

def grafica_moda(modas):
    # Moda
    for moda in modas:
        plt.stem(moda)

    plt.title('Moda')
    plt.ylabel('valor')
    plt.xlabel('Tiros')
    plt.legend()
    plt.grid()
    plt.show()


def datosEstimados(numPosibles):

    frecuenciaEstimada = 0
    promedioEstimado = 0
    varianzaEstimada = 0
    desvioEstimado = 0

    # Frecuencia Estimada

    frecuenciaEstimada  = 1 / len(numPosibles)

    # Promedio Estimado

    suma = sum(numPosibles)

    promedioEstimado = suma / len(numPosibles)

    # Varianza Estimada

    for i in numPosibles:

        varianzaEstimada += ((i-varianzaEstimada)**2)/(len(numPosibles)-1)

    # Desvio Estimado

    desvioEstimado = np.sqrt(varianzaEstimada)

    return frecuenciaEstimada, promedioEstimado, varianzaEstimada, desvioEstimado


def datosEstadisticos(numSeleccionado, numPosibles, numTiradas):

    spins = []
    promedios = []
    frecuencias = []
    varianzas = []
    desvios = []
    modas = []
    varianza_nueva = []
    suma = 0
    contRul = 0
    promedio = 0

    for i in range(numTiradas):

        if i is 0:
            continue

        # Numeros de la ruleta.
        numRuleta = rand.randint(0, 36) # Genero numero aleatorio.
        spins.append(numRuleta) # Guardo Tiro.


        if numSeleccionado == numRuleta:
            contRul += 1
            
        frecuencia = contRul / i
        frecuencias.append(frecuencia)

        suma += numRuleta
        promedio = suma / i # Suma / Indice de tiradas.
        promedios.append(promedio) # Guardo promedio


    # Calculo varianza.
    for i in range(1, len(promedios)):
        contVar = 0

        for j in range(1, len(spins)):
            contVar += (spins[j-1] - promedios[i-1])  ** 2
            if i == j:
                if i != 1:
                    varianzas.append(contVar / j - 1)
                else:
                    varianzas.append(0)
                break

    # Calcular desvio
    for i in range(len(varianzas)):
        desvios.append(np.sqrt(varianzas[i]))

    # Moda
    modas = stats.mode(spins)
    
    return frecuencias, promedios, varianzas, desvios,modas,spins
  

if __name__ == "__main__": 
    frecuencias = []
    promedios = []
    varianzas = []
    desvios = []
    modas = []
    resultados = []

    numPosibles = list(range(0, 36))
    numSeleccionado = int(input("Numero [0 a 36]: "))
    numTiradas = int(input("Tiradas: "))
    repGrafico = int(input("Jugadas: "))

    for i in range(repGrafico):
        frecuencia, promedio, varianza, desvio, moda,spins = datosEstadisticos(numSeleccionado, numPosibles, numTiradas)

        frecuencias.append(frecuencia)
        promedios.append(promedio)
        varianzas.append(varianza)
        desvios.append(desvio)
        modas.append(moda)
        resultados.append(spins)

    frecuenciaEstimada, promedioEstimado, varianzaEstimada, desvioEstimado = datosEstimados(numPosibles)
    grafica_desvio(desvios,desvioEstimado)
    grafica_frecuencia(frecuencias,frecuenciaEstimada)
    grafica_promedio(promedios,promedioEstimado)
    grafica_varianza(varianzas,varianzaEstimada)
#    grafica_moda(modas)
