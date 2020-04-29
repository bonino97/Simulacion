#! usr/bin/env python3
#_*_ coding: utf8 _*_

import random as rand
import matplotlib.pyplot as plt
import numpy as np

def graficos(numTiradas, frecuencias, promedios, varianzas, desvios, frecuenciaEstimada, promedioEstimado, varianzaEstimada, desvioEstimado):
    
    fig, axs = plt.subplots(2, 2)
    fig.canvas.set_window_title("Ruleta")
    
    # Frecuencia Relativa
    for frecuencia in frecuencias:
        axs[0, 0].plot(frecuencia)

    axs[0, 0].set_title("Frecuencia Relativa")
    axs[0, 0].axhline(frecuenciaEstimada, color='blue')
    plt.setp(axs[0, 0], ylabel="fr")

    # Promedio
    for promedio in promedios:
        axs[0, 1].plot(promedio)

    axs[0, 1].set_title('Valor Promedio')
    axs[0, 1].axhline(promedioEstimado, color='blue')
    plt.setp(axs[0, 1], ylabel="vp")

    # Varianza
    for varianza in varianzas:
        axs[1, 0].plot(varianza)

    axs[1, 0].set_title('Varianza')
    axs[1, 0].axhline(varianzaEstimada, color='blue')
    plt.setp(axs[1, 0], ylabel="vv")

    # Desvio
    for desvio in desvios:
        axs[1, 1].plot(desvio)

    axs[1, 1].set_title('Desvío')
    axs[1, 1].axhline(desvioEstimado, color='blue')
    plt.setp(axs[1, 1], ylabel="vd")

    for ax in fig.get_axes():
        ax.grid(True)
        plt.setp(ax, xlabel="Tiradas")
    fig.tight_layout()

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
    
    return frecuencias, promedios, varianzas, desvios
  

if __name__ == "__main__": 
    frecuencias = []
    promedios = []
    varianzas = []
    desvios = []
    numTiradas = 1000

    numPosibles = list(range(0, 36))
    numSeleccionado = int(input("Numero [0 a 36]: "))
    numTiradas = int(input("Tiradas: "))
    repGrafico = int(input("Jugadas: "))

    for i in range(repGrafico):
        frecuencia, promedio, varianza, desvio = datosEstadisticos(numSeleccionado, numPosibles, numTiradas)

        frecuencias.append(frecuencia)
        promedios.append(promedio)
        varianzas.append(varianza)
        desvios.append(desvio)

    frecuenciaEstimada, promedioEstimado, varianzaEstimada, desvioEstimado = datosEstimados(numPosibles)


    graficos(numTiradas, frecuencias, promedios, varianzas, desvios, frecuenciaEstimada, promedioEstimado, varianzaEstimada, desvioEstimado)