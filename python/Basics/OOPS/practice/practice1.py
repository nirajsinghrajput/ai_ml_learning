class Account:

    def __init__(self,balance,acc_no):
        self.balance = balance
        self.acc_no = acc_no
    
    def debit(self):
        x = int(input("enter debit ammount : "))
        self.balance -= x
        print("amount debited successfully")

    def credit(self,amount):
        self.balance += amount
        print("amount credited successfully")

    def pbalance(self):
        print("total amount in account : ",self.balance)

acc_holder1 = Account(10000,987654321)
acc_holder1.pbalance()
acc_holder1.debit()
acc_holder1.pbalance()
acc_holder1.credit(1000)
acc_holder1.pbalance()