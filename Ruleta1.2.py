#! usr/bin/env python3
#_*_ coding: utf8 _*_

import random as rand
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

def grafica_frecuencia(frecuencias):
    # Frecuencia Relativa
    for frecuencia in frecuencias:
        plt.plot(frecuencia)

    plt.title("Frecuencia Relativa")
    plt.axhline((47.4)/100,color='blue') #47.4% es el porcentaje de que salga o rojo o negro. (google)
    plt.ylabel('Fr')
    plt.xlabel('Tiradas')
    plt.legend()
    plt.grid()
    plt.show()

def grafica_cantidad_capital(capitales, tiradas):
    # Promedio
    for capital in capitales:
        for i in tiradas:
            plt.plot(i, capital)

    plt.title('Grafico de Capital')
    plt.axhline((47.4)/100, color='blue')
    plt.ylabel('Capital')
    plt.xlabel('Tiradas')
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

    frecuencias = []
    capitales = np.array([])

    capitales_grafico = np.array([])
    frecuencias_grafico = []


    if tipo_estrategia == 1:
        if tipo_capital == 1:
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
                frecuencia = n_ganador/tiradas
                np.append(capitales,capital)
                frecuencias.append(frecuencia)
            print("\x1b[0;36m"+'--------------------------------------------------------------------------------')
            print('Jugador: {}'.format(jugador+1))

            print("\x1b[0;36m"+'--------------------------------------------------------------------------------')
            print('\nGano {} de {} - Y posee un Capital de : {}'.format(n_ganador,tiradas-1,capital))
            print("\x1b[0;36m"+'--------------------------------------------------------------------------------')
            print('\nNegros: {} - Rojos: {} - Verdes: {}'.format(negros,rojos,verdes))
            print("\x1b[0;36m"+'--------------------------------------------------------------------------------')



        if tipo_capital == 2:

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
                frecuencia = n_ganador/cant_tiradas
                frecuencias.append(frecuencia)

            print("\x1b[0;36m"+'--------------------------------------------------------------------------------')
            print('Jugador: {}'.format(jugador+1))

            print("\x1b[0;36m"+'--------------------------------------------------------------------------------')
            print('\nGano {} de {}'.format(n_ganador,cant_tiradas))
            print("\x1b[0;36m"+'--------------------------------------------------------------------------------')
            print('\nNegros: {} - Rojos: {} - Verdes: {}'.format(negros,rojos,verdes))
            print("\x1b[0;36m"+'--------------------------------------------------------------------------------')

    if tipo_estrategia == 2:

        print("\x1b[3;32m"+'Jugador: {}'.format(jugador+1))
        apuesta_actual = int(input("\x1b[3;32m"+'Apuesta inicial: '))
        if tipo_capital == 1:
            while capital >= apuesta_actual and tiradas <= cant_tiradas and apuesta_actual > 1:
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
                    apuesta_actual = apuesta_actual - 1
                    n_ganador += 1
                    resultado = "Gano"
                else:
                    capital = capital - apuesta_actual
                    apuesta_actual = apuesta_actual + 1
                    resultado = "Perdio"
                tiradas += 1
                frecuencia = n_ganador/tiradas
                frecuencias.append(frecuencia)
                np.append(capitales,capital)

                print("\x1b[0;36m"+'--------------------------------------------------------------------------------')
                print('{} la {}° tirada - Posee un Capital de: {}'.format(resultado,tiradas-1,capital))
                #print('{} {} de {} - Y posee un Capital de: {}'.format(resultado,n_ganador,tiradas-1,capital))
                print("\x1b[0;36m"+'--------------------------------------------------------------------------------')

        if tipo_capital == 2:
            if apuesta_actual > 1:
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
                        apuesta_actual = apuesta_actual - 1
                        n_ganador += 1
                        #resultado = "Gano"
                    else:
                        apuesta_actual = apuesta_actual + 1
                        #resultado = "Perdio"
                    tiradas += 1
                    frecuencia = n_ganador/tiradas
                    frecuencias.append(frecuencia)
                    
                print(frecuencia)
                print("\x1b[0;36m"+'--------------------------------------------------------------------------------')
                print('Jugador: {}'.format(jugador+1))

                print("\x1b[0;36m"+'--------------------------------------------------------------------------------')
                print('\nGano {} de {}'.format(n_ganador,cant_tiradas))
                print("\x1b[0;36m"+'--------------------------------------------------------------------------------')
                print('\nNegros: {} - Rojos: {} - Verdes: {}'.format(negros,rojos,verdes))
                print("\x1b[0;36m"+'--------------------------------------------------------------------------------')


    capitales_grafico = np.append(capitales, capitales_grafico) # Historial de Capital por Tirada, para ver en el Grafico.
    frecuencias_grafico.append(frecuencias)
    grafica_frecuencia(frecuencias_grafico)
    grafica_cantidad_capital(capitales_grafico, tiradas) # Llamo al grafico.

def main():

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
        ruleta(cant_tiradas,tipo_estrategia, jugador, tipo_capital, capital)


if __name__ == '__main__':
    main()
