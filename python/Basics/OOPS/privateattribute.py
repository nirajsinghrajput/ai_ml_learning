class account:
    def __init__(self,acc_no,acc_pin,balance):
        self.acc_no = acc_no
        self.__acc_pin = acc_pin
        self.balance = balance

    def reset_pin(self):
        print("old pin :",self.__acc_pin)
        new = input("inter new pin :")
        self.__acc_pin = new
        print("new pin :",self.__acc_pin)


acc1 = account(987654321,3456,100000)
print(acc1.acc_no)
#print(acc1.__acc_pin)   #it'll not print as it is private attribute (__xxxx)
print(acc1.balance)
print(acc1.reset_pin())