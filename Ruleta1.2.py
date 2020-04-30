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

def retorna_color(valor):
    rojos = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
    negros = [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35] 
    
    if valor in rojos:
        return 0
    if valor in negros:
        return 1
    if valor == 0: 
        return 2


def ruleta(cant_tiradas,tipo_estrategia, jugador, tipo_capital, capital):

    tiradas = 1
    apuesta_actual = 1
    n_ganador = 0
    
    rojos = 0
    negros = 0
    verdes = 0

    if tipo_estrategia == 1 and tipo_capital == 1:

        while capital >= apuesta_actual and tiradas <= cant_tiradas:

            color_random = retorna_color(rand.randint(0,36))
            color_jugado = rand.randint(0,1) # 0:Rojo - 1:Negro

            if color_random == 0: 
                rojos += 1
            elif color_random == 1:
                negros += 1
            else: 
                verdes += 1

            if color_jugado == color_random:

                capital = capital + apuesta_actual
                apuesta_actual = 1
                n_ganador += 1

            else:

                capital = capital - apuesta_actual
                apuesta_actual = apuesta_actual * 2

            tiradas += 1

        print("\x1b[0;36m"+'--------------------------------------------------------------------------------')
        print('Jugador: {}'.format(jugador+1))
        
        print("\x1b[0;36m"+'--------------------------------------------------------------------------------')
        print('\nGano {} de {} - Y posee un Capital de : {}'.format(n_ganador,tiradas-1,capital))
        print("\x1b[0;36m"+'--------------------------------------------------------------------------------')
        print('\nNegros: {} - Rojos: {} - Verdes: {}'.format(negros,rojos,verdes))
        print("\x1b[0;36m"+'--------------------------------------------------------------------------------')

    if tipo_estrategia == 1 and tipo_capital == 2:

        for i in range(0,cant_tiradas):
            
            color_random = retorna_color(rand.randint(0,36))
            color_jugado = rand.randint(0,1) # 0:Rojo - 1:Negro

            if color_random == 0: 
                rojos += 1
            elif color_random == 1:
                negros += 1
            else: 
                verdes += 1

            if color_jugado == color_random:
                apuesta_actual = 1
                n_ganador += 1
            else:
                apuesta_actual = apuesta_actual * 2

            tiradas+=1

            
        print("\x1b[0;36m"+'--------------------------------------------------------------------------------')
        print('Gano {} de {}'.format(n_ganador,cant_tiradas))
        print("\x1b[0;36m"+'--------------------------------------------------------------------------------')
        print('Negros: {} - Rojos: {} - Verdes: {}'.format(negros,rojos,verdes))
        print("\x1b[0;36m"+'--------------------------------------------------------------------------------')

    if tipo_estrategia == 2:

        print("\x1b[0;36m"+'--------------------------------------------------------------------------------')
        print('Jugador: {}'.format(jugador+1))

        if tipo_capital == 1:
            apuesta_actual = int(input("\x1b[3;32m"+'Apuesta inicial: '))
            while capital >= apuesta_actual and tiradas <= cant_tiradas and apuesta_actual > 1:
                color_random = rand.randint(0,1)
                color_jugado = rand.randint(0,1)
                if color_jugado == color_random:
                    capital = capital + apuesta_actual
                    apuesta_actual = apuesta_actual - 1
                    n_ganador += 1
                    gano = True
                else:
                    capital = capital - apuesta_actual
                    apuesta_actual = apuesta_actual + 1
                    gano = False
                tiradas += 1

                if gano:
                    resultado = "Gano"
                else: 
                    resultado = "Perdio"



                print("\x1b[0;36m"+'--------------------------------------------------------------------------------')
                print('{} la {}° tirada - Posee un Capital de: {}'.format(resultado,tiradas-1,capital))
                #print('{} {} de {} - Y posee un Capital de: {}'.format(resultado,n_ganador,tiradas-1,capital))
                print("\x1b[0;36m"+'--------------------------------------------------------------------------------')

        if tipo_capital == 2:
            if apuesta_actual > 1:
                for i in range(0,cant_tiradas):
                    color_random = rand.randint(0,1)
                    color_jugado = rand.randint(0,1)
                    if color_jugado == color_random:
                        apuesta_actual = apuesta_actual - 1
                        n_ganador += 1
                    else:
                        apuesta_actual = apuesta_actual + 1

                print('Gano {} de {}'.format(n_ganador,cant_tiradas-1))

def main():
    n = 0
    veces_ganadora = 0
    lista_numeros = list(range(0,36))
    numeros_muestra = []

    # RULETA
    cant_tiradas = int (input("\x1b[3;33m"+'Cantidad de Tiradas: '))
    print("\x1b[0;33m"+'--------------------------------------------------------------------------------')
    cant_jugadores = int(input("\x1b[3;33m"+'Cantidad de Jugadores: '))
    print("\x1b[1;31m"+
'''
~ESTRATEGIAS~

1 - Martingala
2 - d’Alembert

''')

    tipo_estrategia = int(input("\x1b[3;31m"+'Seleccione la estrategia: '))

    print("\x1b[1;32m"+'''

~TIPOS DE CAPITAL~ 

1 - Acotado
2 - Infinito

''')

    tipo_capital = int(input("\x1b[3;32m"+'Seleccione tipo de capital: '))
    if tipo_capital == 1:
        capital = int(input("\x1b[3;32m"+'Ingrese el capital inicial: '))
    elif tipo_capital == 2:
        capital = 0

    for jugador in range(0,cant_jugadores):

        if tipo_estrategia == 1:
            ruleta(cant_tiradas,tipo_estrategia, jugador, tipo_capital, capital)
        if tipo_estrategia == 2:
            ruleta(cant_tiradas,tipo_estrategia, jugador, tipo_capital, capital)

if __name__ == '__main__':
    main()
