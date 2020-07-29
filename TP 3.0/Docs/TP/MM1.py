import random
import math
from os import system, name
import numpy as np

BUSY = 1
Q_LIMIT = 100
IDLE = 0
model = {
    "num_clientes_sistema": [],
    "next_event_type": 0,
    "num_custs_delayed": 0,
    "num_delays_required": 0,
    "num_events": 0,
    "num_in_q": 0,
    "server_status": 0,
    "area_num_in_q": 0.0,
    "area_server_status": 0.0,
    "mean_interarrival": 0.0,
    "mean_service": 0.0,
    "time": 0.0,
    "time_arrival": [] * (Q_LIMIT + 1),
    "time_last_event": 0.0,
    "time_next_event": [] * 3,
    "total_of_delays": 0.0,
    "tiempo2": [],
    "numero_clientes_cola": 0,
    "prob_n_clientes_cola": 0,
    "time_global": [],
    "opcionMenu": 0
}


def clearScreen():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def initialize():
    model["time"] = 0.0
    model["server_status"] = IDLE
    model["num_in_q"] = 0
    model["time_last_event"] = 0.0
    model["num_custs_delayed"] = 0
    model["total_of_delays"] = 0.0
    model["area_num_in_q"] = 0.0
    model["area_server_status"] = 0.0
    model["time_next_event"].insert(0, float(model["time"]+expon(model["mean_interarrival"])))
    model["time_next_event"].insert(1, float(1*10**(30)))
    model["num_clientes_sistema"] = []
    model["time_global"] = []


def timing():
    model["min_time_next_event"] = 1*10**(29)
    model["next_event_type"] = 0
    for i in range(model["num_events"]):
        if (model["time_next_event"][i] < model["min_time_next_event"]):
            model["min_time_next_event"] = model["time_next_event"][i]
            model["next_event_type"] = i+1
    if (model["next_event_type"] == 0):
        print("Event list empty at time "+str(model["time"]))
    model["time"] = model["min_time_next_event"]


def update_time_avg_stats():
    model["time_since_last_event"] = model["time"]-model["time_last_event"]
    model["time_last_event"] = model["time"]
    model["area_num_in_q"] = model["area_num_in_q"] + model["num_in_q"] * model["time_since_last_event"]
    model["area_server_status"] = model["area_server_status"] + model["server_status"] * model["time_since_last_event"]


def expon(mean):
    u = random.random()
    return -mean * math.log(u)


def arrive():
    model["time_next_event"][0] = model["time"] + expon(model["mean_interarrival"])
    if(model["server_status"] == BUSY):
        model["num_in_q"] += 1
        if(model["num_in_q"] > Q_LIMIT):
            print("Overflow of the array time_arrival at time: "+str(model["time"]))
        model["time_arrival"].insert(model["num_in_q"],model["time"])
        model["num_clientes_sistema"].append(model["num_in_q"]+1)
    else:
        model["delay"] = 0.0
        model["num_clientes_sistema"].append(model["num_in_q"])
        model["total_of_delays"] = model["total_of_delays"] + model["delay"]
        model["num_custs_delayed"] = model["num_custs_delayed"] + 1
        model["server_status"] = BUSY
        model["time_next_event"][1] = model["time"]+expon(model["mean_service"])
        model["tiempo2"].append(model["time_next_event"][1]-model["time"])
    model["time_global"].append(model["time"])


def depart():
    if(model["num_in_q"] == 0):
        model["server_status"] = IDLE
        model["time_next_event"][1] = 1.0E30
        model["num_clientes_sistema"].append(model["num_in_q"])

    else:
        model["num_in_q"] = model["num_in_q"] - 1
        model["num_clientes_sistema"].append(model["num_in_q"])
        model["delay"] = model["time"] - model["time_arrival"][0]
        model["total_of_delays"] = model["total_of_delays"] + model["delay"]
        model["num_custs_delayed"] = model["num_custs_delayed"] + 1
        model["time_next_event"].insert(2,model["time"] + expon(model["mean_service"]))
        model["tiempo2"].append(model["time_next_event"][1]-model["time_arrival"][0])
        for i in range(1, model["num_in_q"]):
            model["time_arrival"][i] = model["time_arrival"][i + 1]
    model["time_global"].append(model["time"])


def report():
    print("Average delay in queue "+str(model["total_of_delays"]/model["num_custs_delayed"]))
    print("Average number in queue"+str(model["area_num_in_q"]/model["time"]))
    print("Average number in queue"+str(model["area_num_in_q"]/model["time"]))
    print("Server utilization "+str(model["area_server_status"]/model["time"]))
    print("Time simulation ended "+str(model["time"]))
    print("Promedio de clientes en el sistema: "+str((sum(model["num_clientes_sistema"]))/len(model["num_clientes_sistema"])))
    print("Tiempo Promedio en el sistema: "+str(sum(model["tiempo2"])/model["num_delays_required"]))
    model["prob_n_clientes_cola"] = ((1-(1/model["mean_interarrival"])/(1/model["mean_service"]))*((1/model["mean_interarrival"])/(1/model["mean_service"]))**int(model["numero_clientes_cola"]))
    print("La probabilidad de que haya: " + str(model["numero_clientes_cola"])+" clientes en cola es de:"+str(model["prob_n_clientes_cola"]))
 
 
def GraficaPromClientesSistemaMedia(arreglo):
    global numero_clientes_cola
    global media_gral
    global varianza_gral
    global desvio_gral
    global contador_gral
    global media_total_utlizacion_servidor
    global media_de_las_medias
    global tiempo_a_utilizar

  

    acum_clientes_sistema = np.cumsum(arreglo)

    num_clientes_sistema_media = []
    for i in range(len(arreglo)):
        num_clientes_sistema_media.append(acum_clientes_sistema[i]/(i+1))

    media_cli_sistema = []
    for i in range(len(arreglo)):
        media_cli_sistema.append(np.mean(arreglo))

    if (contador_gral == 1):
        
        for i in range(len(num_clientes_sistema_media)):
            media_de_las_medias.append(num_clientes_sistema_media[i]/10)
        tiempo_a_utilizar=model["time_global"]
    else:
        if(len(media_de_las_medias) >= len(num_clientes_sistema_media)):
            longitud = len(num_clientes_sistema_media)
            diferencia_long=len(media_de_las_medias)-len(num_clientes_sistema_media)

        else:
            longitud=len(media_de_las_medias)
            diferencia_long=0
        for i in range(longitud+diferencia_long):
            if (i)<longitud:
                media_de_las_medias[i] = media_de_las_medias[i]+(num_clientes_sistema_media[i])/10
            else:
                media_de_las_medias[i]=media_de_las_medias[i]+num_clientes_sistema_media[longitud-1]/10
  

    media_gral += np.mean(arreglo)

    plt.figure(1)
    plt.plot(time_global, num_clientes_sistema_media, color="orange")

   
    if (contador_gral == 10):

        if (model["opcionMenu"] == "5"):
            media_gral=media_gral/10
            plt.plot(tiempo_a_utilizar, media_de_las_medias,label="Media esperada de utilizacion del servidor en el sistema", color="blue")
        else:
            plt.plot(tiempo_a_utilizar, media_de_las_medias,label="Media esperada de clientes en el sistema", color="blue")
        plt.legend()
    plt.savefig("Utilizacion_Servidor_Media.png")



def GraficaPromTiempoSistemaMedia(arreglo):
    #global num_clientes_sistema

    global numero_clientes_cola
    global media_gral
    global varianza_gral
    global desvio_gral
    global contador_gral
    global media_de_las_medias

    acum_clientes_sistema = np.cumsum(arreglo)

    num_clientes_sistema_media = []
    for i in range(len(arreglo)):
        num_clientes_sistema_media.append(acum_clientes_sistema[i]/(i+1))

    media_cli_sistema = []
    for i in range(len(arreglo)):
        media_cli_sistema.append(np.mean(arreglo))

    media_gral += np.mean(arreglo)

    if (contador_gral == 1):
        for i in range(len(num_clientes_sistema_media)):
            media_de_las_medias.append(num_clientes_sistema_media[i]/10)
    else:
        for i in range(len(media_de_las_medias)):
            media_de_las_medias[i] = media_de_las_medias[i] + (num_clientes_sistema_media[i])/10

    plt.figure(1)
    plt.plot(num_clientes_sistema_media,color="black")
    if (contador_gral == 10):
        plt.plot(media_de_las_medias, label="Media esperada de tiempo", color="red")
        plt.legend()
    plt.savefig("Tiempos_Cola_Media.png")


def PastelUtilizacionServidor():
    global area_server_status
    global time
    global media_gral
    porcentajes = ((media_gral)*100, (1-media_gral)*100)
    nombres=("Porcentaje utilizado del servidor","Porcentaje no utilizado del servidor")
    plt.pie(porcentajes, labels=nombres, autopct="%0.1f %%")

    plt.savefig("Utilizacion_servidor.png")



def PastelProbabilidadClienteCola():
    global area_server_status
    global time
    global media_total_utlizacion_servidor
    global prob_n_clientes_cola
    global numero_clientes_cola
    
    if prob_n_clientes_cola>0:
        porcentajes = ((prob_n_clientes_cola)*100, (1-prob_n_clientes_cola)*100)
    else:
        porcentajes=(0,100)
    nombres = ("Probabilidad que haya: " + str(numero_clientes_cola)+" clientes en cola",
               "Probabilidad que NO haya: " + str(numero_clientes_cola)+" clientes en cola")
    plt.pie(porcentajes, labels=nombres, autopct="%0.1f %%")

    plt.savefig("Prob_n_clientes.png")

def menu():
    print(" ")
    print("MENÚ PRINCIPAL - Seleccione una opción")
    print("1 - Promedio de clientes en el sistema")
    print("2 - Promedio de clientes en cola")
    print("3 - Tiempo promedio en sistema")
    print("4 - Tiempo promedio en cola")
    print("5 - Utilización del servidor")
    print("6 - Probabilidad de n clientes en cola")
    print("0 - Salir")


while True:
    global opcionMenu
    os.system('cls')    

    menu()

    opcionMenu = input("Ingrese su opcion:  ")
    print(" ")

    if opcionMenu == "1":
        contador_gral=0
        media_gral = 0
        varianza_gral=0
        desvio_gral=0
        media_de_las_medias=[]
        varianza_de_las_varianzas=[]
        desvio_de__desvios=[]
        for i in range(10):
            contador_gral+=1
            MainProgram()
            GraficaPromClientesSistemaMedia(num_clientes_sistema)
            plt.title("Media de clientes en el sistema")
            plt.xlabel("Tiempo(segundos)")  # título del eje x
            plt.ylabel("Valor de la media de clientes en sistema")

            GraficaPromClientesSistemaVarianza(num_clientes_sistema)
            plt.title("Varianza de los clientes en el sistema")
            plt.xlabel("Tiempo(segundos)")  # título del eje x
            plt.ylabel("Valor de la varianza de clientes en sistema")
            
            GraficaPromClientesSistemaDesvio(num_clientes_sistema)
            plt.title("Desviacion de los clientes en el sistema")
            plt.xlabel("Tiempo(segundos)")  # título del eje x
            plt.ylabel("Valor de la desviacion de clientes en sistema")
        plt.show()
        
        input("Pulsa una tecla para continuar")
    elif opcionMenu == "2":
        contador_gral = 0
        media_gral = 0
        varianza_gral = 0
        desvio_gral = 0
        media_de_las_medias = []
        varianza_de_las_varianzas = []
        desvio_de__desvios = []
        for i in range(10):

            contador_gral += 1
            MainProgram()
            GraficaPromClientesSistemaMedia(area_num_in_q_total)
            plt.title("Media de clientes en cola")
            plt.xlabel("Tiempo(segundos)") 
            plt.ylabel("Valor de la media de clientes en cola")

            GraficaPromClientesSistemaVarianza(area_num_in_q_total)
            plt.title("Varianza de los clientes en cola")
            plt.xlabel("Tiempo(segundos)")  
            plt.ylabel("Valor de la varianza de clientes en cola")

            GraficaPromClientesSistemaDesvio(area_num_in_q_total)
            plt.title("Desviacion de los clientes en cola")
            plt.xlabel("Tiempo(segundos)")  
            plt.ylabel("Valor de la desviacion de clientes en cola")
        plt.show()


        input("Pulsa una tecla para continuar")


    elif opcionMenu == "3":
        
        contador_gral = 0
        media_gral = 0
        varianza_gral=0
        desvio_gral=0
        media_de_las_medias = []
        varianza_de_las_varianzas = []
        desvio_de__desvios = []
        for i in range(10):
            contador_gral+=1
            MainProgram()
            GraficaPromTiempoSistemaMedia(tiempo_2)
            plt.title("Media de los tiempos en el sistema")
            plt.xlabel("Numero de Cliente")  # título del eje x
            plt.ylabel("Valor de la media de tiempo en sistema")

            GraficaPromTiempoSistemaVarianza(tiempo_2)
            plt.title("Varianza de los tiempos en el sistema")
            plt.xlabel("Numero de Cliente")  # título del eje x
            plt.ylabel("Valor de la varianza de tiempo en sistema")
            
            GraficaPromTiempoSistemaDesvio(tiempo_2)
            plt.title("Desviacion de los tiempos en el sistema")
            plt.xlabel("Numero de Cliente")  # título del eje x
            plt.ylabel("Valor de la desviación de tiempo en sistema")
        plt.show()


        input("Pulsa una tecla para continuar")
    elif opcionMenu == "4":

        contador_gral = 0
        media_gral = 0
        varianza_gral = 0
        desvio_gral = 0
        media_de_las_medias = []
        varianza_de_las_varianzas = []
        desvio_de__desvios = []
        for i in range(10):
            contador_gral += 1
            MainProgram()
            GraficaPromTiempoSistemaMedia(ListaDemoras)
            plt.title("Media de los tiempos en cola")
            plt.xlabel("Numero de Cliente")  # título del eje x
            plt.ylabel("Valor de la media de tiempo en cola")

            GraficaPromTiempoSistemaVarianza(ListaDemoras)
            plt.title("Varianza de los tiempos en cola")
            plt.xlabel("Numero de Cliente")  # título del eje x
            plt.ylabel("Valor de la varianza de tiempo en cola")

            GraficaPromTiempoSistemaDesvio(ListaDemoras)
            plt.title("Desviacion de los tiempos en cola")
            plt.xlabel("Numero de Cliente")  # título del eje x
            plt.ylabel("Valor de la desviacion de tiempo en cola")
        plt.show()


        input("Pulsa una tecla para continuar")
    elif opcionMenu == "5":
        contador_gral = 0
        media_gral = 0
        varianza_gral = 0
        desvio_gral = 0
        media_total_utlizacion_servidor=0
        media_de_las_medias = []
        varianza_de_las_varianzas = []
        desvio_de__desvios = []
        for i in range(10):
            contador_gral += 1
            MainProgram()
            GraficaPromClientesSistemaMedia(utilizacion_servidor_total)
            plt.title("Media de utilización del servidor")
            plt.xlabel("Tiempo(segundos)")  # título del eje x
            plt.ylabel("Valor de la media de utilización del servidor")

            GraficaPromClientesSistemaVarianza(utilizacion_servidor_total)
            plt.title("Varianza de utilización del servidor")
            plt.xlabel("Tiempo(segundos)")  # título del eje x
            plt.ylabel("Valor de la varianza de utilización del servidor")

            GraficaPromClientesSistemaDesvio(utilizacion_servidor_total)
            plt.title("Desviacion de utilización del servidor")
            plt.xlabel("Tiempo(segundos)")  # título del eje x
            plt.ylabel("Valor de la desviación utilización del servidor")
        
        plt.figure(4)
        PastelUtilizacionServidor()
        plt.title("Porcentaje total del tiempo que el servidor se encuentra ocupado ")
        plt.show()

        input("Pulsa una tecla para continuar")

    elif opcionMenu == "6":
        numero_clientes_cola = input("Ingresar numero de clientes en cola : ")

        prob_n_clientes_cola = ((1-(1/mean_interarrival)/(1/mean_service)) *((1/mean_interarrival)/(1/mean_service))**int(numero_clientes_cola))
        if prob_n_clientes_cola<0:
            prob_n_clientes_cola=0
        print("La probabilidad de que haya: " + str(numero_clientes_cola) +" clientes en cola es de: "+str(prob_n_clientes_cola))
        
        PastelProbabilidadClienteCola()

        plt.show()
        input("Pulsa una tecla para continuar")
    elif opcionMenu == "0":
        break
    else:
        print(" ")
        input("No has pulsado ninguna opción correcta... \n Pulsa una tecla para continuar")

if __name__ == "__main__":
    clearScreen()
    model["num_events"] = 2
    model["mean_interarrival"] = float(
        abs(int(input("Mean Interarrival time(Minutes): "))))
    model["mean_service"] = float(abs((int(input("Mean Service Time(Minutes): ")))))
    model["num_delays_required"] = abs(int(input("Number of Customers: ")))
    model["numero_clientes_cola"] = abs(int(input("Número de clientes en Cola: ")))
    initialize()
    while model["num_custs_delayed"] < model["num_delays_required"]:
        timing()
        update_time_avg_stats()
        if model["next_event_type"] == 1:
            arrive()
        elif model["next_event_type"] == 2:
            depart()
    report()
    menu()
