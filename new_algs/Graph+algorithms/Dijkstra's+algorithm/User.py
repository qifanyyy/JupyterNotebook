from abc import ABC, abstractmethod
# from Final_v1 import *
# from Test_Final import *

class Vehicles(ABC):
    # abstract method
    def arrival(self, distance):  # Time it will arrive
        pass

    def waitingTime(self, time):  # Time until transportation arrives
        pass

    def testCondition(self):  # N/A
        pass

    def cost(self, distance):  # Cost of Transportation
        pass


class Car(Vehicles):
    def speed(self, distance):
        # The car has a speed value that is 5
        return .5 * distance

    def waitingTime(self, time):
        # Getting a car is instant
        return 0

    def testCondition(self):
        pass

    def cost(self, distance):
        return 0


class Bus(Vehicles):
    def speed(self, distance):
        # The bus has a speed value that is 4
        return .6 * distance

    def waitingTime(self, time):
        time = time % 60
        if time <= 30:
            return 30 - time
        else:
            return 60 - time

    def testCondition(self):
        pass

    def cost(self, distance):
        return 1.25


class Bike(Vehicles):
    def speed(self, distance):
        # The car has a speed value that is 2.5
        if distance < 10:
            return .25 * distance
        else:
            return .7 * distance

    def waitingTime(self, time):
        # Getting a bike is instant
        return 0

    def testCondition(self):
        pass

    def cost(self, distance):
        return 0


class Taxi(Vehicles):
    def speed(self, distance):
        # The taxi car has a speed value that is 5
        return .5 * distance

    def waitingTime(self, time=None):
        # Getting a taxi is always 8 min
        return 8

    def testCondition(self):
        pass

    def cost(self, distance):
        return .25 * distance


class Person:
    # The person class has a name, location, money, and a perception of time
    def __init__(self, name, location, money):
        self.name = name
        self.time = 310  # 5:10am
        self.hour = 0
        self.minute = 0
        self.location = location
        self.money = money

    """
        Displays options of travel
        @param network: graph to search through
        @param start: Building to start at
        @param finish: Building to get to
        return none
        """
    def moveOptions(self, network, start, finish, car=Car(), taxi=Taxi(), bus=Bus(), bike=Bike()):
        d, path = network.path_from_to(start, finish)
        print("\nThe shortest possible path is: " + network.return_path(path) + "and the distance is " +
              str(round(d * (.05/15), 3)) + " miles \n")
        carSpeed = car.speed(d)
        print("If you use a car, it will take " + str(round(carSpeed, 1)) + " minutes to arrive")
        taxiSpeed = taxi.speed(d)
        taxiCost = taxi.cost(d)
        print("If you use a Taxi, it will take " + str(round(taxiSpeed, 1)) + " minutes to arrive and it will cost " +
              str(round(taxiCost, 2)) + " dollars (Taxi can arrive in " + str(taxi.waitingTime()) + " minutes)")
        busSpeed = bus.speed(d)
        busCost = bus.cost(d)
        print("If you use a Bus, it will take " + str(round(busSpeed, 1)) + " minutes to arrive and it will cost " +
              str(busCost) + " dollars (Next bus arrives in " + str(bus.waitingTime(self.time)) + " minutes)")
        bikeSpeed = bike.speed(d)
        print("If you use a Bike, it will take " + str(round(bikeSpeed, 1)) + " minutes to arrive")

    def carmove(self, destination, distance):
        car = Car()
        self.money -= car.cost(distance)
        self.location = destination
        self.time += car.speed(distance)

    def taximove(self, destination, distance):
            taxi = Taxi()
            self.money -= taxi.cost(distance)
            self.location = destination
            self.time += taxi.speed(distance)

    def busmove(self, destination, distance):
            bus = Bus()
            self.money -= bus.cost(distance)
            self.location = destination
            self.time += bus.speed(distance)

    def bikemove(self, destination, distance):
            bike = Bike()
            self.money -= bike.cost(distance)
            self.location = destination
            self.time += bike.speed(distance)

