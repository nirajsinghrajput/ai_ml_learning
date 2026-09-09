class students:

    #obj attr > class attr

    college_name = "IIEST,Shibpur" #class attr

    blood_group = "NA" #class attr
    #doubt X

    #default constructors
    """def __init__(self):
        pass"""
    
    #parameterized constructor
    def __init__(self,name,marks,blood_group):
        self.name = name    #obj attr
        self.marks = marks
        self.blood_group = blood_group
        print("adding new student in Database..")

    def wlcm(self):
        print("welcom",self.name)

    @staticmethod    #decorator
    def college():
        print("IIEST,Shibpur")


s1 = students("Shivam",50,None)
print(s1.name, s1.marks, s1.blood_group)
s1.name = "Kammo"
s1.wlcm()
s1.college()

s2 = students("Niraj",100,"O-")
print(s2.name,s2.marks,s2.blood_group)
s2.wlcm()

print(students.college_name)

#del for deleting an attribute

print(s1)
del s1
print(s1)