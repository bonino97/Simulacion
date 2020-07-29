import random, math
from enum import Enum

def expon(mean):
    # Generate a U(0,1) random variable.
    u = random.random()

    # Return an exponential random variable with mean "mean".
    return - (1 / mean) * math.log(u)

class Queue:
    area_num_in_q = 0
    time_last_event = 0
    queue = []
    dictProbabilities = dict()

    @staticmethod
    def add(time):
        Queue.area_num_in_q += (time - Queue.time_last_event) * len(Queue.queue)

        try:
            Queue.dictProbabilities[len(Queue.queue)] += (time - Queue.time_last_event) 
        except:
            Queue.dictProbabilities[len(Queue.queue)] = (time - Queue.time_last_event)
        
        Queue.time_last_event = time
        Queue.queue.append(time)


    @staticmethod
    def remove():
        Queue.area_num_in_q += (Model.time - Queue.time_last_event) * len(Queue.queue)
        
        try:
            Queue.dictProbabilities[len(Queue.queue)] += (Model.time - Queue.time_last_event) 
        except:
            Queue.dictProbabilities[len(Queue.queue)] = (Model.time - Queue.time_last_event)
        
        
        Queue.time_last_event = Model.time
        
        return Queue.queue.pop(0)

class Server:
    area_num_in_server = 0
    time_last_update = 0
    state = False

    @staticmethod
    def changeState(state, time):
        if Server.state:
            Server.area_num_in_server += (time - Server.time_last_update) * 1
            Server.time_last_update = time
            Server.state = state
        else:
            Server.time_last_update = time
            Server.state = state

class Model:
    time    = 0
    delays = 0
    server_time_usage = 0
    mu      = 1
    lamb    = mu * 0.25
    limit = 50
    denied = 0
    Overflow = False
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
        Model.Overflow = False

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
        if len(Queue.queue) > Model.limit:    #For a finite queue, check if we passed the queue limit
            Model.denied += 1
            Model.Overflow = True
            
        Queue.add(time_arrival)
    else:
        Server.changeState(True, Model.time)
        Model.num_customers_delayed += 1 # Customers arrives to server, one person more delayed

        newDeparture = Event(Events.DEPARTURE, Model.time + expon(Model.mu))
        Model.server_time_usage += newDeparture.time_event - Model.time
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
        
        #Create departure to arrive retireved
        newDeparture = Event(Events.DEPARTURE, Model.time + expon(Model.mu))
        NextEvents.addEvent(newDeparture)
        Model.server_time_usage += newDeparture.time_event - Model.time


def report():
    avg_clients_inq = round(Queue.area_num_in_q / Model.time, 2)
    avg_clients_inserver = round(Server.area_num_in_server / Model.time, 2)

    avg_time_inq = round(Model.delays / Model.num_customers_delayed,2)
    avg_time_inserver = round(Model.server_time_usage / Model.num_customers_delayed,2)

    print('Average number in queue: ' + str(avg_clients_inq)) # Promedio de clientes en cola.
    print('Average number in system: ' + str(avg_clients_inq + avg_clients_inserver)) # Promedio de clientes en el sistema.
    print('Average number in server: ' + str(avg_clients_inserver)) # Utilización del servidor
    print('Average delay in queue minutes: ' + str(avg_time_inq)) # Tiempo promedio en cola.
    print('Average time in server minutes: ' + str(avg_time_inserver)) # Tiempo promedio en el servidor
    print('Average time in system minutes: ' + str(avg_time_inq + avg_time_inserver)) # Tiempo promedio en el sistema
    print('Probability of n(1) clients in queue: ' + str(round(Queue.dictProbabilities[1] / Model.time, 4))) # Probabilidad de n clientes en cola.
    # Probabilidad de denegación de servicio (cola finita de tamaño: 0, 2, 5, 10, 50). -> Otro archivo

    

if __name__ == "__main__":
    for x in range(100):
        Model.clean()

        while((Model.num_customers_delayed < Model.custs_delayed_required) and not Model.Overflow):
            nextEvent = NextEvents.getNextEvent()
            Model.time = nextEvent[0] 

            if nextEvent[1] == Events.ARRIVE:
                arrive(nextEvent[0])

            elif nextEvent[1] == Events.DEPARTURE:
                departure(nextEvent[0])

        #report()
    print("Probability of overflows", Model.denied / 100)