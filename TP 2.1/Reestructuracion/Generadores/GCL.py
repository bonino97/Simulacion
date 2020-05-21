import numpy as np
import random as rand

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