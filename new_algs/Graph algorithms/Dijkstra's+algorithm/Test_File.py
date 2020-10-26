from Final_v1 import *
from User import *

# Creates all Building Objects
olin = Building("Olin Hall")
duffield = Building("Duffield Hall")
phillips = Building("Phillips Hall")
gates = Building("Gates Hall")
upson = Building("Upson Hall")
statler = Building("Statler Hall")
health = Building("Cornell Health")
store = Building("Cornell Store")
day_hall = Building("Day Hall")
malott = Building("Malott Hall")
clark = Building("Clark Hall")
baker = Building("Baker Lab")
bethe = Building("Hans Bethe")


# Dictionary of Building Keys and its paths and distances to other Buildings
graph = {
    olin: [[duffield, 3], [health, 2], [store, 5]],
    duffield: [[phillips, 1], [olin, 3], [statler, 2]],
    phillips: [[duffield, 1], [gates, 2]],
    statler: [[gates, 1], [duffield, 2], [malott, 7], [day_hall, 4]],
    gates: [[phillips, 2], [statler, 1]],
    health: [[olin, 2]],
    store: [[olin, 5], [baker, 10], [day_hall, 2]],
    baker: [[store, 10], [day_hall, 9], [clark, 3]],
    clark: [[baker, 3], [malott, 2]],
    malott: [[clark, 2], [day_hall, 4], [statler, 7]],
    day_hall: [[malott, 4], [baker, 9], [store, 2], [statler, 4]]
}

# Creates a TransportNetwork Object
network = TransportNetwork(graph)

# Creates a Person and a demonstration of moveOptions is given
joe = Person("Joe", olin, 100)
joe.moveOptions(network, joe.location, clark)
