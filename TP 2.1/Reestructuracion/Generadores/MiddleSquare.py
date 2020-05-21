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