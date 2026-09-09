class person:
    name = "anonymous"

    """def changeName(self,name):
        self.name = "Niraj" #creats a new object with name "Niraj"
        person.name = "Niraj"   #changes name of class
        self.__class__.name = "Rahul"   #changes name of class
    """
    
    @classmethod
    def changeName(cls,name):
        cls.name = name


p1 = person()
p1.changeName("Niraj")
print(p1.name)
print(person.name)