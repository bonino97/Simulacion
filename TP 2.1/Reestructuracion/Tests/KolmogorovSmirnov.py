from math import sqrt
import numpy as np
import collections

class KolmogorovSmirnov:

    def Test(self, muestra):
        muestra = sorted(muestra)
        d_plus = []
        d_minus = []
        D_esperada = 1.36/sqrt(len(muestra)) # Generalización de fórmula de una tabla

        for i in range(1, len(muestra)+1):
            x= i/len(muestra) - muestra[i-1]
            d_plus.append(x)

        for i in range(1, len(muestra) + 1): 
            y =(i-1)/len(muestra)
            y =muestra[i-1]-y 
            d_minus.append(y)

        # Calculate max(D+, D-) 
        D = max(max(d_plus, d_minus)) 

        print("D calculada: "+ str(D) + " , D esperada : " + str(D_esperada))
        print("¿D calculadans < D esperada?")

        if(D<D_esperada):
            print("Test aprobado. Muestra uniforme")
            print("")
            return True
        else:
            print("Test desaprobado. No implica que no sea uniforme")
            print("")
            return False