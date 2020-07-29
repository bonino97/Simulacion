import random, math
from enum import Enum
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

def expon(mean):
    # Generate a U(0,1) random variable.
    u = random.random()

    # Return an exponential random variable with mean "mean".
    return - (1 / mean) * math.log(u)
    
class Stats():
    numbers_inq = []
    numbers_inserver = []
    numbers_insystem = []
    times_inq = []
    times_inserver = []
    times_insystem = []
    server_utilizations = []
    probabilities = []
    times_ended = [] 

class Queue:
    area_num_in_q = 0
    time_last_event = 0
    queue = []
    dictProbabilities = dict()
    dictProbabilitiesSystem = dict()

    @staticmethod
    def add(time):
        Queue.area_num_in_q += (time - Queue.time_last_event) * len(Queue.queue)

        #For queue
        try:
            Queue.dictProbabilities[len(Queue.queue)] += (time - Queue.time_last_event) 
        except:
            Queue.dictProbabilities[len(Queue.queue)] = (time - Queue.time_last_event)

        if len(Queue.queue) == 0: # 1 persona en el sistema
            try:
                Queue.dictProbabilitiesSystem[1] += (time - Server.time_last_update)         
            except:
                Queue.dictProbabilitiesSystem[1] = (time - Server.time_last_update)
        else:
            try:
                Queue.dictProbabilitiesSystem[len(Queue.queue) + 1] += (time - Queue.time_last_event)
            except:
                Queue.dictProbabilitiesSystem[len(Queue.queue) + 1] = (time - Queue.time_last_event)

        Queue.time_last_event = time
        Queue.queue.append(time)

    @staticmethod
    def remove():
        Queue.area_num_in_q += (Model.time - Queue.time_last_event) * len(Queue.queue)
        
        try:
            Queue.dictProbabilities[len(Queue.queue)] += (Model.time - Queue.time_last_event) 
        except:
            Queue.dictProbabilities[len(Queue.queue)] = (Model.time - Queue.time_last_event)
        
        try:
            Queue.dictProbabilitiesSystem[len(Queue.queue) + 1] += (Model.time - Queue.time_last_event)
        except:
            Queue.dictProbabilitiesSystem[len(Queue.queue) + 1] = (Model.time - Queue.time_last_event)

        Queue.time_last_event = Model.time
        
        return Queue.queue.pop(0)

class Server:
    area_num_in_server = 0
    time_last_update = 0
    state = False

    @staticmethod
    def changeState(state, time):
        if Server.state:
            Server.time_last_update = time
            Server.state = state
        else:
            try:
                Queue.dictProbabilitiesSystem[0] += (time - Server.time_last_update)         
            except:
                Queue.dictProbabilitiesSystem[0] = (time - Server.time_last_update)

            Server.time_last_update = time
            Server.state = state

class Model:
    time    = 0
    delays = 0
    arrayDelays = []
    arrayServerUsage = []
    server_time_usage = 0
    mu      = 1
    lamb    = mu * 1.25
    num_customers_delayed = 0    # Number of clients up to time x
    custs_delayed_required = 10000 # Maximum number of clients that pass through the system

    @staticmethod
    def clean():
        #Clean model
        Model.time = 0
        Model.delays = 0
        Model.arrayDelays = []
        Model.arrayServerUsage = []
        Model.server_time_usage = 0
        Model.num_customers_delayed = 0

        #Clean server
        Server.area_num_in_server = 0
        Server.time_last_update = 0
        Server.state = False

        #Clean queue
        Queue.area_num_in_q = 0
        Queue.time_last_event = 0
        Queue.queue = []
        Queue.dictProbabilities = dict()
        Queue.dictProbabilitiesSystem = dict()

        #Clean nextEvents
        NextEvents.arrive = expon(Model.lamb)
        NextEvents.departure =  Constants.Infinite 
        NextEvents.listEvents = []
        

class Constants():
    Infinite = 1 * (10 ** 30)

#Enums
class Events(Enum):
    ARRIVE = 1,
    DEPARTURE = 2

#Classes
class Event():
    time_event = 0
    type_event = Events.ARRIVE  
    
    def __init__(self, type_event, time_event):
        self.type_event = type_event
        self.time_event = time_event 

class NextEvents:
    arrive = expon(Model.lamb)
    departure =  Constants.Infinite # In start, we don't have any departure
    listEvents = [Event(Events.ARRIVE, arrive)]

    @staticmethod
    def getNextEvent():
        #If event arrive is before the departure
        if NextEvents.arrive < NextEvents.departure:
            return (NextEvents.arrive, Events.ARRIVE)
        else:
            return (NextEvents.departure, Events.DEPARTURE)

    @staticmethod
    def addEvent(event):        
        if event.type_event == Events.ARRIVE:
            NextEvents.arrive = event.time_event

        elif event.type_event == Events.DEPARTURE:
            NextEvents.departure = event.time_event
        
        NextEvents.listEvents.append(event)

def arrive(time_arrival):
    
    newArrival = Event(Events.ARRIVE, Model.time + expon(Model.lamb))
    NextEvents.addEvent(newArrival)
    
    if Server.state:
        #Para cola finita, tenemos que validar que la cola no llegue a un maximo estableciado en esta parte.
        Queue.add(time_arrival)
    else:
        Server.changeState(True, Model.time)
        Model.num_customers_delayed += 1 # Customers arrives to server, one person more delayed

        newDeparture = Event(Events.DEPARTURE, Model.time + expon(Model.mu))
        Model.server_time_usage += newDeparture.time_event - Model.time
        Model.arrayServerUsage.append(newDeparture.time_event - Model.time)
        NextEvents.addEvent(newDeparture)
        

def departure(time_departure):
    if len(Queue.queue) == 0:
        Server.changeState(False, Model.time) # free server
        NextEvents.departure = Constants.Infinite
    
    else:
        #Get first arrive of queue and remove from it
        time_cust_arrival = Queue.remove() #Return first position of queue and remove it
        Model.num_customers_delayed += 1
        Model.delays += Model.time - time_cust_arrival
        Model.arrayDelays.append(Model.time - time_cust_arrival)
        #Create departure to arrive retireved
        newDeparture = Event(Events.DEPARTURE, Model.time + expon(Model.mu))
        NextEvents.addEvent(newDeparture)
        Model.server_time_usage += newDeparture.time_event - Model.time
        Model.arrayServerUsage.append(newDeparture.time_event - Model.time)

def draw(server_utilization):
    #Time histograms
    fig, axs = plt.subplots(3, 2)

    axs[0,0].hist(Model.arrayDelays, bins = 30)
    axs[0,0].set_ylabel('Frecuencia')
    axs[0,0].set_xlabel('Tiempo')
    axs[0,0].set_title('Tiempo en cola')    
    
    axs[0,1].hist(Model.arrayServerUsage, bins = 30)
    axs[0,1].set_ylabel('Frecuencia')
    axs[0,1].set_xlabel('Tiempo')
    axs[0,1].set_title('Tiempo en servidor')


    #Stacked chart
    # Data
    r = [0]
    total = 0
    cumulativeProbabilities = []
    array = []

    #Cumulative probability
    for key in Queue.dictProbabilitiesSystem.keys():
        total += Queue.dictProbabilitiesSystem[key]
        cumulativeProbabilities.append(total)
    
    #We only keep the first values
    array += cumulativeProbabilities[0:5]
    array.append(cumulativeProbabilities[-1])

    for index, a in enumerate(array[::-1]):
        aux = (len(array) - index) - 1 if a != array[-1] else "+" + str(len(array))
        axs[1,1].bar(" ", a, width = 0.5, label=f"{aux} Clientes en sistema")
    
    axs[1,1].set_ylabel('Tiempo')
    axs[1,1].legend()

    # Grafico de barras -> Probabilities in queue
    objects = Queue.dictProbabilities.keys()
    y_pos = np.arange(len(objects))
    performance = list(map(lambda x: x / Model.time, Queue.dictProbabilities.values()))
    
    axs[1,0].bar(y_pos, performance, align='center', alpha=0.5)
    axs[1,0].set_xticks(y_pos, objects)
    axs[1,0].set_ylabel('Probabilidad de n')
    axs[1,0].set_xlabel('Clientes')

    # Diagrama de torta -> Server utilization
    labels = 'Utilizado', 'Libre'
    sizes = [server_utilization, 1 - server_utilization]
    colors = ['gold', 'yellowgreen']
    # Plot
    axs[2,0].pie(sizes, labels=labels, colors=colors,
    autopct='%1.1f%%', shadow=True, startangle=140)

    plt.show()

def report(flag):
    #Average clients in queue and server
    avg_clients_inq = round(Queue.area_num_in_q / Model.time, 2)
    avg_clients_inserver = round(Model.server_time_usage / Model.time, 2)#Server.area_num_in_server

    #Average time in queue and server
    avg_time_inq = round(Model.delays / Model.num_customers_delayed,2)
    avg_time_inserver = round(Model.server_time_usage / Model.num_customers_delayed,2)


    print('Simulation ended', Model.time)
    Stats.times_ended.append(Model.time)
    
    print('Average number in queue: ' + str(avg_clients_inq)) # Promedio de clientes en cola.
    Stats.numbers_inq.append(avg_clients_inq)
    
    print('Average number in system: ' + str(avg_clients_inq + avg_clients_inserver)) # Promedio de clientes en el sistema.
    Stats.numbers_insystem.append(avg_clients_inq + avg_clients_inserver)
    
    print('Average number in server: ' + str(avg_clients_inserver)) # Utilización del servidor
    Stats.numbers_inserver.append(avg_clients_inserver)
    
    print('Average delay in queue minutes: ' + str(avg_time_inq)) # Tiempo promedio en cola.
    Stats.times_inq.append(avg_time_inq)
    
    print('Average time in server minutes: ' + str(avg_time_inserver)) # Tiempo promedio en el servidor
    Stats.times_inserver.append(avg_time_inserver)
    
    print('Average time in system minutes: ' + str(avg_time_inq + avg_time_inserver)) # Tiempo promedio en el sistema
    Stats.times_insystem.append(avg_time_inq + avg_time_inserver)
    
    print('Probability of n(1) clients in queue: ' + str(round(Queue.dictProbabilities[1] / Model.time, 4))) # Probabilidad de n clientes en cola.
    Stats.probabilities.append(round(Queue.dictProbabilities[1] / Model.time, 4))
    
    # Probabilidad de denegación de servicio (cola finita de tamaño: 0, 2, 5, 10, 50). -> Otro archivo
    if flag:
        draw( avg_clients_inserver )
    
def finalReport():
    print('Average of times the simulation ended": ', round(sum(Stats.times_ended) / len(Stats.times_ended), 2))
    print('Average of "Average number in queue": ', round(sum(Stats.numbers_inq) / len(Stats.numbers_inq), 2))
    print('Average of "Average number in system": ', round(sum(Stats.numbers_insystem) / len(Stats.numbers_insystem), 2))
    print('Average of "Average server utilization": ', round(sum(Stats.numbers_inserver) / len(Stats.numbers_inserver), 2))
    print('Average of "Average delay in queue minutes": ', round(sum(Stats.times_inq) / len(Stats.times_inq), 2))
    print('Average of "Average time in server', round(sum(Stats.times_inserver)/len(Stats.times_inserver),2)) 
    print('Average of "Average time in system minutes": ', round(sum(Stats.times_insystem) / len(Stats.times_insystem),2))
    print('Average of "probability of n(1) clients in queue": ', round(sum(Stats.probabilities)/len(Stats.probabilities),2))

if __name__ == "__main__":
    for x in range(10):
        while(Model.num_customers_delayed < Model.custs_delayed_required):
            nextEvent = NextEvents.getNextEvent()
            Model.time = nextEvent[0] 

            if nextEvent[1] == Events.ARRIVE:
                arrive(nextEvent[0])

            elif nextEvent[1] == Events.DEPARTURE:
                departure(nextEvent[0])
            Server.area_num_in_server += (Model.time - Server.time_last_update) * (1 if Server.state else 0)
        report(True if x == 0 else False)
        Model.clean()
        
    finalReport()
        