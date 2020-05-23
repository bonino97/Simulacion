from math import sqrt
import numpy as np
import collections


class ChiCuadrado:
    
    def Test(self, muestra):
        valorTabla = 16.9190 # con alpha 0.05 y grado de libertad 9
        freq_esperada = len(muestra)/10
        frecuencias = np.zeros(10)
        intervalos = np.zeros(10)
        #divido la muestra en 10 intervalos
        for i in range(0, len(muestra)):
            if(muestra[i]<0.1): intervalos[0] = intervalos[0] + 1
            elif(muestra[i]<0.2): intervalos[1] = intervalos[1] + 1
            elif(muestra[i]<0.3): intervalos[2] = intervalos[2] + 1
            elif(muestra[i]<0.4): intervalos[3] = intervalos[3] + 1
            elif(muestra[i]<0.5): intervalos[4] = intervalos[4] + 1
            elif(muestra[i]<0.6): intervalos[5] = intervalos[5] + 1
            elif(muestra[i]<0.7): intervalos[6] = intervalos[6] + 1
            elif(muestra[i]<0.8): intervalos[7] = intervalos[7] + 1
            elif(muestra[i]<0.9): intervalos[8] = intervalos[8] + 1
            else: intervalos[9] = intervalos[9] + 1

        for i in range(0, len(frecuencias)):
            frecuencias[i] = (intervalos[i]- freq_esperada)**2/freq_esperada

        suma = sum(frecuencias)

        print("Suma de frecuencias: "+str(suma)+ " , frecuencia esperada: "+str(freq_esperada)+" , valor en la tabla(alpha=0.05, grado libertad=9): 16.9190")
        print("¿Suma de frecuencias < valor en tabla?")

        if(suma<valorTabla):
            print("Test aprobado. Muestra uniforme")
            print("")
            return True
        else:
            print("Test desaprobado. No implica que no sea uniforme")
            print("")
            return False