# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
import matplotlib.pyplot as plt
import numpy as np

def GetStatisticalData(SelectedNumber, PossibleNumbers, CountSpins):
    Sum = 0
    Counter = 0
    Spins = []
    Averages = []
    Frecuencies = []
    Variances = []
    Detours = []

    #Start to throw the roulette
    for i in range(CountSpins):

        if i is 0:
            continue

        Number = random.randint(0, 36) #Get a number of Roulette
        Spins.append(Number) #Save throw

        #Calculation frecuency
        if SelectedNumber == Number:
            Counter += 1
            
        Frecuency = Counter / i
        Frecuencies.append(Frecuency)

        #Calculation average
        Sum += Number
        Average = Sum / i
        Averages.append(Average)

    #Calculation variance
    for i in range(1, len(Averages)):
        Counter = 0

        for j in range(1, len(Spins)):
            Counter += (Spins[j - 1]-Averages[i - 1])**2
            if i == j:
                if i != 1:
                    Variances.append(Counter / j - 1)
                else:
                    Variances.append(0)
                break

    #Calculation detour
    for i in range(len(Variances)):
            Detours.append(np.sqrt(Variances[i]))
    
    return Frecuencies, Averages, Variances, Detours
  
def GetEstimatedData(PossibleNumbers):
    EstimatedFrecuency = 0
    EstimatedAverage = 0
    EstimatedVariance = 0
    EstimatedDetour = 0

    #Estimated frecuency
    EstimatedFrecuency  = 1 / len(PossibleNumbers)

    #Estimated average
    EstimatedSum = sum(PossibleNumbers)
    EstimatedAverage = EstimatedSum / len(PossibleNumbers)

    #Estimated variance
    for i in PossibleNumbers:
        EstimatedVariance += ((i-EstimatedAverage)**2)/(len(PossibleNumbers)-1)

    #Estimated detous
    EstimatedDetour = np.sqrt(EstimatedVariance)

    return EstimatedFrecuency, EstimatedAverage, EstimatedVariance, EstimatedDetour

def Graphic(CountSpins, FrecuenciesIterations, AveragesIterations, VariancesIterations, DetoursIterations, EstimatedFrecuency, EstimatedAverage, EstimatedVariance, EstimatedDetour):
    Figure, Axs = plt.subplots(2, 2)
    Figure.canvas.set_window_title("Simulación de Ruleta: Análisis (de 0 a " + str(CountSpins) + " tiradas)")
    
    #Graphic of Frecuency
    for Frecuencies in FrecuenciesIterations:
        Axs[0, 0].plot(Frecuencies)

    Axs[0, 0].set_title("Frecuencia Relativa")
    Axs[0, 0].axhline(EstimatedFrecuency, color='red')
    plt.setp(Axs[0, 0], ylabel="fr(frecuencia del numero)")

    #Graphic of Average
    for Averages in AveragesIterations:
        Axs[0, 1].plot(Averages)

    Axs[0, 1].set_title('Valor Promedio')
    Axs[0, 1].axhline(EstimatedAverage, color='red')
    plt.setp(Axs[0, 1], ylabel="vp (valor promedio de las tiradas)")

    #Graphic of Average
    for Variances in VariancesIterations:
        Axs[1, 0].plot(Variances)

    Axs[1, 0].set_title('Varianza')
    Axs[1, 0].axhline(EstimatedVariance, color='red')
    plt.setp(Axs[1, 0], ylabel="vv (valor de la varianza)")

    #Graphic of Detours
    for Detours in DetoursIterations:
        Axs[1, 1].plot(Detours)

    Axs[1, 1].set_title('Desvío')
    Axs[1, 1].axhline(EstimatedDetour, color='red')
    plt.setp(Axs[1, 1], ylabel="vd (valor del desvio)")

    for ax in Figure.get_axes():
        ax.grid(True)
        plt.setp(ax, xlabel="Número de Tiradas")
    Figure.tight_layout()

    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__": 
    FrecuenciesIterations = []
    AveragesIterations = []
    VariancesIterations = []
    DetoursIterations = []

    PossibleNumbers = list(range(0, 37))
    SelectedNumber = int(input("Choose a number of roulette: "))
    CountSpins = int(input("Input count of spins: "))
    Iterations = int(input("Iterations for graphic: "))

    for i in range(Iterations):
        Frecuencies, Averages, Variances, Detours = GetStatisticalData(SelectedNumber, PossibleNumbers, CountSpins)

        FrecuenciesIterations.append(Frecuencies)
        AveragesIterations.append(Averages)
        VariancesIterations.append(Variances)
        DetoursIterations.append(Detours)

    EstimatedFrecuency, EstimatedAverage, EstimatedVariance, EstimatedDetour = GetEstimatedData(PossibleNumbers)


    Graphic(CountSpins, FrecuenciesIterations, AveragesIterations, VariancesIterations, DetoursIterations, EstimatedFrecuency, EstimatedAverage, EstimatedVariance, EstimatedDetour)