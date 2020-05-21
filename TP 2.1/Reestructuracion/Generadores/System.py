import random as rand

class GeneradorSystem: 

    def muestra(self, n, seed):
        rand.SystemRandom(seed)
        array = np.zeros(n)
        for i in range(n):
            array[i] = rand.random()
        return array