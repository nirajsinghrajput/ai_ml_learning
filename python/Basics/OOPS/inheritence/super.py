class Car:
    def __init__(self,type):
        self.type = type

    @staticmethod
    def start():
        print("car started..")

    @staticmethod
    def stop():
        print("car stopped..")

class ToyotaCar(Car):
    def __init__(self, name,type):
        super().__init__(type)
        super().start()
        self.name = name

car1 = ToyotaCar("hilux","petrol")
print(car1.type)