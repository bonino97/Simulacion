import numpy as np


class GeneradorNumPy: 
    
    def muestra(self, n, seed):
        np.random.seed(seed)
        array = np.zeros(n)
        for i in range(n):
            array[i] = np.random.random()
        return array