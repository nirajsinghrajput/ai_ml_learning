class car:

    colour = "Black"

    @staticmethod
    def start():
        print("car started...")

    @staticmethod
    def stop():
        print("car stopped...")


class toyota(car):
    
    def __init__(self,name):
        self.name = name

class highlender(toyota):

    def __init__(self,model):
        self.model = model


car1 = toyota("fortuner")
car2 = toyota("hylux")

car3 = highlender("petrol")

print(car1.name)
print(car1.colour)
print(car1.start())
print(car1.stop())
print(car2.name)
print(car2.colour)
print(car2.start())
print(car2.stop())
print(car3.model)
print(car3.colour)