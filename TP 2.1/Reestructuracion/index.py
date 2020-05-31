from tkinter import ttk
from tkinter import * 
from math import sqrt
from scipy import stats

import sqlite3
import random as rand
import numpy as np


class Index:
    def __init__(self, window):
        self.wind = window
        self.wind.title('Numeros Pseudoaleatorios')
        
        #Creando un Frame Container.
        frame = LabelFrame(self.wind, text = 'Ingrese una Semilla: ')
        frame.grid(row = 1, column  = 1, columnspan = 3, pady = 20)

        #Input Semilla
        Label(frame, text = '').grid(row = 0, column = 1)
        self.seed = Entry(frame)
        self.seed.focus()
        self.seed.grid(row = 2, column = 1)

        #Boton AddSeed
        ttk.Button(frame, text = "Ejecutar", command = self.Execute).grid(row = 3, columnspan = 2, sticky = W + E)

        #Mensaje Error
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 3, column = 1, columnspan = 1, sticky = W + E)

    def Execute(self):
        if self.Validation():
            index = 1000
            seed = self.seed.get()

            #Python Random Generator
            arrayRandom = self.GeneradorRandom(index, seed)            
            
            RandomParidadResult, RandomParidadFrec = self.Paridad(arrayRandom)
            RandomKsResult, RandomKsD, RandomKsDEstimada = self.KolmogorovSmirnov(arrayRandom)
            RandomChiCuadradoResult, RandomChiCuadradoSuma, RandomChiCuadradoValorTabla, RandomChiCuadradoFrecEstimada = self.ChiCuadrado(arrayRandom)
            RandomCorridaArribaAbajoResult, RandomCorridaArribaAbajoZ, RandomCorridaArribaAbajoMedia = self.CorridaArribaAbajo(arrayRandom)

            self.RandomWindow = Toplevel()             

            ##############################################
            # ---       Generador Random Paridad     --- #
            ##############################################

            Label(self.RandomWindow, text = 'Generador Random', font="Helvetica 14 bold", fg = "green", anchor = CENTER).grid(row = 0, column = 0)
            Label(self.RandomWindow, text = '___________________________________________________', fg='black').grid(row = 1, column = 0)
            Label(self.RandomWindow, text = 'Test de Paridad.', font="Helvetica 11 bold").grid(row = 2, column = 0, sticky = W)
            Label(self.RandomWindow, text = 'Resultado: ').grid(row = 3, column = 0, sticky = W)
            if RandomParidadResult: 
                Label(self.RandomWindow, text = str(RandomParidadResult), fg = 'green').grid(row = 3, column = 1, sticky = W)    
            else: 
                Label(self.RandomWindow, text = str(RandomParidadResult), fg = 'red').grid(row = 3, column = 1, sticky = W)
            Label(self.RandomWindow, text = 'Frecuencia: ').grid(row = 4, column = 0, sticky = W)
            Label(self.RandomWindow, text = RandomParidadFrec).grid(row = 4, column = 1, sticky = W)
            Label(self.RandomWindow, text = '___________________________________________________', fg='black').grid(row = 5, column = 0)

            ###############################################
            # --- Generador Random Kolmogorov Smirnov --- #
            ###############################################

            Label(self.RandomWindow, text = 'Test de Kolmogorov-Smirnov.', font="Helvetica 11 bold").grid(row = 6, column = 0, sticky = W)
            Label(self.RandomWindow, text = 'Resultado: ').grid(row = 8, column = 0, sticky = W)
            if RandomKsResult:
                Label(self.RandomWindow, text = str(RandomKsResult), fg = 'green').grid(row = 8, column = 1, sticky = W)
            else:
                Label(self.RandomWindow, text = str(RandomKsResult), fg = 'red').grid(row = 8, column = 1, sticky = W)
            Label(self.RandomWindow, text = 'D - Resultante: ').grid(row = 9, column = 0, sticky = W)
            Label(self.RandomWindow, text = RandomKsD).grid(row = 9, column = 1, sticky = W)
            Label(self.RandomWindow, text = 'D - Estimada: ').grid(row = 10, column = 0, sticky = W)
            Label(self.RandomWindow, text = RandomKsDEstimada).grid(row = 10, column = 1, sticky = W)
            Label(self.RandomWindow, text = '___________________________________________________', fg='black').grid(row = 11, column = 0)

            ###############################################
            # ---    Generador Random ChiCuadrado     --- #
            ###############################################

            Label(self.RandomWindow, text = 'Test de ChiCuadrado.', font="Helvetica 11 bold").grid(row = 12, column = 0, sticky = W)
            Label(self.RandomWindow, text = 'Resultado: ').grid(row = 13, column = 0, sticky = W)
            if RandomChiCuadradoResult:
                Label(self.RandomWindow, text = str(RandomChiCuadradoResult), fg = 'green').grid(row = 13, column = 1, sticky = W)
            else:
                Label(self.RandomWindow, text = str(RandomChiCuadradoResult), fg = 'red').grid(row = 13, column = 1, sticky = W)
            Label(self.RandomWindow, text = 'Valor Tabla: ').grid(row = 14, column = 0, sticky = W)
            Label(self.RandomWindow, text = RandomChiCuadradoValorTabla).grid(row = 14, column = 1, sticky = W)
            Label(self.RandomWindow, text = 'Suma de Frecuencias: ').grid(row = 15, column = 0, sticky = W)
            Label(self.RandomWindow, text = RandomChiCuadradoSuma).grid(row = 15, column = 1, sticky = W)
            Label(self.RandomWindow, text = '___________________________________________________', fg='black').grid(row = 16, column = 0)

            ###############################################
            #--  Generador Random Corrida Arriba Abajo -- #
            ###############################################

            Label(self.RandomWindow, text = 'Test Arriba Abajo de la Media.', font="Helvetica 11 bold").grid(row = 17, column = 0, sticky = W)
            Label(self.RandomWindow, text = 'Resultado: ').grid(row = 18, column = 0, sticky = W)
            if RandomChiCuadradoResult:
                Label(self.RandomWindow, text = str(RandomChiCuadradoResult), fg = 'green').grid(row = 18, column = 1, sticky = W)
            else:
                Label(self.RandomWindow, text = str(RandomChiCuadradoResult), fg = 'red').grid(row = 18, column = 1, sticky = W)
            Label(self.RandomWindow, text = 'Media: ').grid(row = 19, column = 0, sticky = W)
            Label(self.RandomWindow, text = RandomChiCuadradoValorTabla).grid(row = 19, column = 1, sticky = W)
            Label(self.RandomWindow, text = 'Z: ').grid(row = 20, column = 0, sticky = W)
            Label(self.RandomWindow, text = RandomChiCuadradoSuma).grid(row = 20, column = 1, sticky = W)
            Label(self.RandomWindow, text = '___________________________________________________', fg='black').grid(row = 21, column = 0)


            #NumPy Generator
            arrayNumPy = self.GeneradorNumPy(index, int(seed))
            
            #MiddleSquare Generator
            arrayMiddleSqr = self.GeneradorMiddleSquare(index, int(seed))

            #GCL Generator
            arrayGCL = self.GeneradorGCL(index, int(seed))

        else:
            self.message['text'] = '* Semilla Requerida'

    def Validation(self):
        return len(self.seed.get()) != 0


    #######################
    # --- Generadores --- #
    #######################

    def GeneradorRandom(self, index, seed):
        rand.SystemRandom(seed) 
        array = np.zeros(index) # Inicializo Array con 0s
        for i in range(index): 
            array[i] = rand.random()
        return array

    def GeneradorNumPy(self, index, seed):
        np.random.seed(seed)
        array = np.zeros(index) # Inicializo Array con 0s
        for i in range(index):
            array[i] = np.random.random()
        return array

    def GeneradorMiddleSquare(self, index, seed):
        def Generador():
            div=10000 #divisor de la x para que devuelva un valor entre 0 y 1
            x = seed
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
        
        array = []
        generador = Generador()
        for i in range(index):
            obs = float(next(generador))
            array.append(float(obs))
        return array

    def GeneradorGCL(self, index, seed):
        def Generador():
                # Parametros en GNU C Library
            a = 1103515245 # Multiplicador
            c = 12345 # Incremento
            m = 2**32 # Modulo   
            xi = seed
            while True:
                xf = (a * xi + c) % m
                xi = xf
                yield xf
        
        modulo = 2**32
        array = []
        generador = Generador()
        for _ in range(index):
            array.append(next(generador)/modulo)
        return array

    #######################
    # ---    Tests    --- #
    #######################

    def Paridad(self, results):
        n = len(results) # n = Cantidad de Numeros Pseudoaleatorios Generados
        pares = 0
    
        for i in results:
            iaux = str(i)
            pos = len(iaux)-1
            
            if int(iaux[pos]) % 2 == 0: 
                pares += 1
        
        frec = pares/n
        
        if frec >= 0.45 and frec <= 0.55:
            resultado = True
        else:
            resultado = False

        return resultado, frec

    def KolmogorovSmirnov(self, results):
        sort = sorted(results)
        d_max = []
        d_min = [] 
        d_estimada = (1.36)/sqrt(len(sort)) #1.36 (apéndice de tablas) / Tamaño Muestral


        for i in range(1, len(sort)+1):
            d_max.append((i/len(sort) - sort[i-1]))
            
            aux = (i-1)/len(sort)

            d_min.append(sort[i-1]-aux)

        D = max(max(d_max, d_min))

        if(d_estimada > D):
            resultado = True
        else:
            resultado = False

        return resultado, D, d_estimada

    def ChiCuadrado(self, results):
        valor_tabla = 16.9190 # con alpha 0.05 y grado de libertad 9
        frec_estimada = len(results)/10
        frecuencias = np.zeros(10)
        intervalos = np.zeros(10)
        #divido la results en 10 intervalos
        for i in range(0, len(results)):
            if(results[i]<0.1): intervalos[0] = intervalos[0] + 1
            elif(results[i]<0.2): intervalos[1] = intervalos[1] + 1
            elif(results[i]<0.3): intervalos[2] = intervalos[2] + 1
            elif(results[i]<0.4): intervalos[3] = intervalos[3] + 1
            elif(results[i]<0.5): intervalos[4] = intervalos[4] + 1
            elif(results[i]<0.6): intervalos[5] = intervalos[5] + 1
            elif(results[i]<0.7): intervalos[6] = intervalos[6] + 1
            elif(results[i]<0.8): intervalos[7] = intervalos[7] + 1
            elif(results[i]<0.9): intervalos[8] = intervalos[8] + 1
            else: intervalos[9] = intervalos[9] + 1

        for i in range(0, len(frecuencias)):
            frecuencias[i] = (intervalos[i]- frec_estimada)**2/frec_estimada

        suma = sum(frecuencias)

        if(suma<valor_tabla):
            resultado = True
        else:
            resultado = False

        return resultado, suma, valor_tabla, frec_estimada

    def CorridaArribaAbajo(self, results):
        listaOperadores = []
        N = len(results)
        n1 = 0
        n2 = 0
        b = 0
        mediaMuestra = np.average(results)
        mediaB = 0
        varianzaB = 0
        Z = 0
        for l in results:
            if l >= mediaMuestra:
                listaOperadores.append('+')
                n1 = n1 + 1 
            else:
                listaOperadores.append('-')
                n2 = n2 + 1
        for j in range(0,len(listaOperadores)-1):
            if listaOperadores[j] == '+':
                if listaOperadores[j] != listaOperadores[j+1]:
                    b = b + 1
            else:
                if listaOperadores[j] != listaOperadores[j+1]:
                    b = b + 1
        mediaB = ((2*n1*n2)/(n1+n2))+1
        varianzaB = (2*n1*n2*((2*n1*n2)-N))/(N*N*(N-1))
        Z = (b - mediaB)/(np.sqrt(varianzaB))
        #alfa = 0.05 , por lo tanto Z(1-(alfa/2)) = Z(0.025) = 1.96

        print("Z calculada: "+str(Z)+" , Z(0.025) = 1.96")
        print("¿|Z| < Z(0.025)?")

        if abs(Z)<1.96:
            print("Test aprobado. Se demuestra la Independecia, por lo tanto, la aleatoriedad también")
            print("")
            resultado = True
        else:
            print("Test desaprobado. Se rechaza la independencia")
            print("")
            resultado = False
        return resultado, Z, mediaMuestra

        

if __name__ == '__main__':
    window = Tk()
    window.geometry('220x180')
    application = Index(window)
    window.mainloop()  