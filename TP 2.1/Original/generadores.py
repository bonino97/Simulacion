import numpy as np
import random as rand

class GeneradorMiddleSquare:
    seed = 0
    def __init__(self, seed):
        self.seed = seed

    def gen(self):
        div=10000 #divisor de la x para que devuelva un valor entre 0 y 1
        x = self.seed
        while True:
            square = x * x
            if len(str(square)) < 8:
                need = 8 - len(str(square))
                addZero = ""
                for j in range(0,need):
                    addZero = str(0) + addZero
                square = addZero + str(square)  
            else: 
                square = str(square)
            x = float(square[2] + square[3] + square[4] + square[5])
            yield x/div
    
    def muestra(self, n):
        sample = []
        generadorsito = self.gen()
        for i in range(n):
            observation = float(next(generadorsito))
            sample.append(float(observation))

        return sample

                
                

class GeneradorGCL:
    seed = 0

    def __init__(self, seed):
        self.seed = seed

    def gen(self):
        # parameters as in GNU C Library
        a = 1103515245 #Multiplicador
        c = 12345 #Incremento
        m = 2**32 #Modulo   
        xi = self.seed
        while True:
            xf = (a * xi + c) % m
            xi = xf
            yield xf

    def muestra(self, n):
        #lower, upper = interval[0], interval[1]
        m = 2**32
        sample = []
        generadorsito = self.gen()
        for _ in range(n):
            sample.append(next(generadorsito)/m)
            #observation = int((upper - lower) * (next(generadorsito) / (m - 1)) + lower)
            #sample.append(int(observation))

        return sample