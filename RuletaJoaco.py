#! usr/bin/env python3
#_*_ coding: utf8 _*_

import random
import matplotlib.pyplot as plt
import numpy as np

def main():
    n = 0
    veces_ganadora = 0
    lista_numeros = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,35,35,36]
    numeros_muestra = []
    numeros_verdes = [0]
    numeros_rojos = [1,3,5,7,9,12,14,16,18,20,21,23,25,27,29,31,32,34,36]
    numeros_negros = [2,4,6,8,10,11,13,15,17,19,22,24,26,28,30,33,35]

    # RULETA
    numero_jugado = int(input('Numero a apostar: '))
    for i in range(0,1000):
        if numero_jugado in lista_numeros:
            print('\n')
            print('Jugada Nro {}'.format(i))
            numeros = random.randint(0,36)
            if numero_jugado == numeros:
                print ('Tiro Ganador')
                veces_ganadora += 1
            else:
                print('Tiro erroneo, numero ganador {}'.format(numeros))
            n += 1
            numeros_muestra.append(numeros)
    print('Usted gano {} veces. Numeros Ganadores: {}, cantidad de tiradas {}.'.format(veces_ganadora,numeros_muestra,n))

    # Graficos
    x = (0,10,100)
    y = np.sin(x)
    plt.plot(x,y)
    plt.show()
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
