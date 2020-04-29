#! usr/bin/env python3
#_*_ coding: utf8 _*_

import random as rand
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

def grafica_frecuencia(frecuencias,frecuenciaEstimada):
    # Frecuencia Relativa
    for frecuencia in frecuencias:
        plt.plot(frecuencia)

    plt.title("Frecuencia Relativa")
    plt.axhline(frecuenciaEstimada, color='blue')
    plt.ylabel('Fr')
    plt.xlabel('Tiradas')
    plt.legend()
    plt.grid()
    plt.show()

def grafica_promedio(promedios,promedioEstimado):
    # Promedio
    for promedio in promedios:
        plt.plot(promedio)

    plt.title('Valor Promedio')
    plt.axhline(promedioEstimado, color='blue')
    plt.ylabel('Valor')
    plt.xlabel('Tiros')
    plt.legend()
    plt.grid()
    plt.show()

def retorna_color(lista):

def ruleta(cant_jugadores,cant_tiradas,tipo_estrategia):
    print('''
        Seleccione tipo de capital:
        1 - Acotado
        2 - Infinito
        ''')
    tipo_capital = int(input())
    if tipo_capital == 1:
        capital = int(input('Ingrese el capital inicial'))
    elif tipo_capital == 2:
        capital = 999999999
    tiradas = 1
    n_ganador = 0
    if tipo_estrategia == 1 and tipo_capital == 1:
        apuesta_actual = 1
        while capital >= apuesta_actual and tiradas <= cant_tiradas:
            color_random = rand.randint(0,1)
            color_jugado = rand.randint(0,1)
            if color_jugado == color_random:
                capital = capital + apuesta_actual
                apuesta_actual = 1
                n_ganador += 1
            else:
                capital = capital - apuesta_actual
                apuesta_actual = apuesta_actual * 2
            tiradas += 1
        print('Gano {} de {} - capital: {}'.format(n_ganador,tiradas,capital))

    if tipo_estrategia == 1 and tipo_capital == 2:
        for i in range(0,cant_tiradas):
            color_random = rand.randint(0,1)
            color_jugado = rand.randint(0,1)
            if color_jugado == color_random:
                apuesta_actual = 1
                n_ganador += 1
            else:
                apuesta_actual = apuesta_actual * 2
        print('Gano {} de {}'.format(n_ganador,cant_tiradas))


def main():
    n = 0
    veces_ganadora = 0
    lista_numeros = list(range(0,36))
    numeros_muestra = []

    # RULETA
    cant_tiradas = int (input('Cantidad de Tiradas: '))
    cant_jugadores = int(input('Cantidad de Jugadores: '))
    print('''
        Seleccione la estrategia:
        1 - Martingala
        2 - d’Alembert
    ''')
    tipo_estrategia = int(input())
    if tipo_estrategia == 1:
        ruleta(cant_jugadores,cant_tiradas,tipo_estrategia)
    if tipo_estrategia == 2:
        #d_alembert()
        pass

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()



if __name__ == "__main__":
    main()
