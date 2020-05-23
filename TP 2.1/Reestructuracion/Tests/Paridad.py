from math import sqrt
import numpy as np
import collections

class Paridad: 

    def Test(self, muestra):
        n = len(muestra)
        x = 0
        for m in muestra:
            mstr = str(m)
            pos = len(mstr)-1
            if int(mstr[pos]) % 2 == 0:
                x = x + 1
        frecuencia = x/n

        print("frec: "+ str(frecuencia) + " , rango aceptación: 0.45 - 0.55")
        print("¿frecuencia dentro del rango de aceptación?")

        if frecuencia >=0.45 and frecuencia <= 0.55:
            print("Test aprobado. Muestra aleatoria, las frecuencias de las paridades se encuentran en el rango de aceptación")
            print("")
            return True
        else: 
            print("Test desaprobado. Muestra con números mayormente de una paridad notablemente")
            print("")
            return False