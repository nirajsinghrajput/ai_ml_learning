class employee :
    def __init__(self,role,dept,salary):
        self.role = role
        self.dept = dept
        self.salary = salary

    def showDetails(self):
        return print("role -",self.role,"dept -",self.dept ,"salary -",self.salary )
    
class engineer(employee):
    def __init__(self, name ,age):
        self.name = name
        self.age = age
        super().__init__("engineer", "IT", "75000")

e1 = employee("accountant","finance","60,000")
e1.showDetails()

eng1 = engineer("Shivam","20")
eng1.showDetails()