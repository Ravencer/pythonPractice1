from abc import ABC, abstractmethod
from enum import Enum
from random import randint

class TaxiClass(Enum):
    economy = 1
    comfort = 2
    business = 3

class Passenger:
    def __init__(self, name, mobile, luggage):
        self.name = name
        self.mobile = mobile
        self.luggage = luggage
        self._distance = 1
    @property
    def distance(self):
        return self._distance
    @distance.setter
    def distance(self, value):
        if(value <= 0):
            raise ValueError("Distance must be greaten than 0!")
        self._distance = value

class Luggage:
    def __init__(self, weight):
        self.weight = weight
        self._size = [1, 1]
    @property
    def size(self):
        return self._size
    @size.setter
    def size(self, value):
        for el in range(len(value)):
            if(value[el] <= 0):
                raise ValueError("Size must be greater than 0!")
        if(len(value) == 2):
            self._size[0] = value[0]
            self._size[1] = value[1]
        else:
            raise IndexError("Two elements must be given!")
        
class Taxi(ABC):
    def __init__(self, driverName, taxiNumber, taxiModel):
        self.taxiNumber = taxiNumber
        self.taxiModel = taxiModel
        self.driverName = driverName
    @abstractmethod
    def computeCost(self, passengers):
        pass
    
class PassengerCar(Taxi):
    def __init__(self, driverName, taxiNumber, taxiModel, taxiClass, onDeal):
        super().__init__(driverName, taxiNumber, taxiModel)
        self.taxiClass = taxiClass
        self.onDeal = onDeal
    def computeCost(self, taxiCompany, passengers):
        distance = 0
        total = 0
        newPassengers = passengers
        passengersInTaxi = []
        for i in range(len(passengers)):
            if((passengers[i].luggage.size[0] < 40 and passengers[i].luggage.size[1] < 50 and passengers[i].luggage.weight < 50) and len(passengersInTaxi) < 4):
                passengersInTaxi.append(passengers[i])
                if distance < passengers[i].distance : distance = passengers[i].distance
        total = distance * 20 * self.taxiClass.value       
        print('За пассажирами:', end=" ")
        for i in range(len(passengersInTaxi)):
            print (passengersInTaxi[i].name, end=', ')
            newPassengers.remove(passengersInTaxi[i])
        print(' прибудет ' + self.driverName + ' на легковом такси ' + str(self.taxiClass.name) + ' ' + self.taxiNumber + ', ' + self.taxiModel + '. Рассчетная стоимость составит ' + str(total))
        self.onDeal = True
        taxiCompany.callTaxi(newPassengers)
    
class Truck(Taxi):
    def __init__(self, driverName, taxiNumber, taxiModel, onDeal, loaders = False):
        super().__init__(driverName, taxiNumber, taxiModel)
        self.onDeal = onDeal
    def computeCost(self, taxiCompany, passengers):
        loaders = input('Требуются ли грузчики? Y/N\n')
        if loaders == 'Y' : loaders = 1500 
        else : loaders = 0
        distance = 0
        total = 0
        newPassengers = passengers
        passengersInTaxi = []
        for i in range(len(passengers)):
            if((passengers[i].luggage.size[0] > 40 or passengers[i].luggage.size[1] > 50 or passengers[i].luggage.weight > 50) and len(passengersInTaxi) < 2):
                passengersInTaxi.append(passengers[i])
                if distance < passengers[i].distance : distance = passengers[i].distance
            elif(passengers[i] == passengers[len(passengers) - 1] and len(passengersInTaxi) < 2):
                passengersInTaxi.append(passengers[i])
                if distance < passengers[i].distance : distance = passengers[i].distance
        total = distance * 50 + loaders
        print('За пассажирами:', end=" ")
        for i in range(len(passengersInTaxi)):
            print (passengersInTaxi[i].name, end=', ')
            newPassengers.remove(passengersInTaxi[i])
        print(' прибудет ' + self.driverName + ' на грузовом такси ' + self.taxiNumber + ', ' + self.taxiModel + '. Рассчетная стоимость составит ' + str(total))
        self.onDeal = True
        taxiCompany.callTaxi(newPassengers)
        
        
class TaxiCompany:
    def __init__(self, companyName, taxiPark = []):
        self.companyName = companyName
        self.taxiPark = taxiPark
    def callTaxi(self, passengers):
        typeOfCar = ''
        if(len(passengers) > 0):
            for x in range(len(passengers)):
                if(passengers[x].luggage.size[0] > 40 or passengers[x].luggage.size[1] > 50 or passengers[x].luggage.weight > 50):
                    typeOfCar = Truck.__name__
                    break
                typeOfCar = PassengerCar.__name__
            for x in range(len(self.taxiPark)):
                if(type(self.taxiPark[x]).__name__ == typeOfCar and self.taxiPark[x].onDeal == False):
                    self.taxiPark[x].computeCost(self, passengers)
                    break
                
            
            
        

if __name__ == "__main__":
    passengerCar1 = PassengerCar('Ivan','T025NV', 'Volkswagen Polo', TaxiClass.comfort, False)
    truckCar1 = Truck('Vladislav', 'G302TG', 'GAZ-3302', False, False)
    passengerCar2 = PassengerCar('Nikolay', 'N231DF', 'Skoda Octavia', TaxiClass.business, False)
    truckCar2 = Truck('Dmitriy', 'T102DE', 'GAZ-3310', False, False)
    taxiCompany = TaxiCompany('Vezet', [passengerCar1, truckCar1, passengerCar2, truckCar2])
    companyStud = []
    while True:
        anw = input('1. Заказать такси \n 2. Завершить программу\n')
        match anw:
            case '1':
                while True:
                    name = input('Введите имя пассажира\n')
                    mobile = input('Введите номер телефона\n')
                    luggageWeight = int(input('Введите вес багажа\n'))
                    luggageSize = list(map(int, input('Введите размер багажа через запятую\n').split(',')))
                    distance = int(input('Введите расстояние от Красноярска в км.\n'))
                    newPass = Passenger(name, mobile, Luggage(luggageWeight))
                    newPass.luggage.size = luggageSize
                    newPass.distance = distance
                    companyStud.append(newPass)
                    ans = input('1. Продолжить заказ \n 2. Перейти к расчёту\n')
                    match ans:
                        case '1':
                            continue
                        case '2':
                            taxiCompany.callTaxi(companyStud)
                            break
                        case _:
                            break
            case '2':
                break
            case _:
                break
    