import numpy as np
import random as rand

class GeneradorMiddleSquare:
    seed = 0
    def __init__(self, seed):
        self.seed = seed

    def gen(self, interval):
        lower, upper = interval[0], interval[1]
        x = self.seed
        if len(str(x)) > 4:
            x = x[:4]
        while len(str(x)) < 4:
            x = int(str(x)+"1")
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
            x = int(square[2] + square[3] + square[4] + square[5])
            yield x
    
    def muestra(self, n, interval):
        sample = []
        generadorsito = self.gen(interval)
        for i in range(n):
            observation = next(generadorsito)
            sample.append(int(observation))

        return sample

                
                

class GeneradorGCL:
    seed = 0

    def __init__(self, seed):
        self.seed = seed

    def gen(self, interval):
        lower, upper = interval[0], interval[1]
        # parameters as in GNU C Library
        a = 1103515245 #Multiplicador
        c = 12345 #Incremento
        m = 2**32 #Modulo   
        xi = self.seed
        while True:
            xf = (a * xi + c) % m
            xi = xf
            yield int((upper - lower) * (xf / (m - 1)) + lower)

    def muestra(self, n, interval):
        sample = []
        generadorsito = self.gen(interval)
        for i in range(n):
            observation = next(generadorsito)
            sample.append(int(observation))

        return sample