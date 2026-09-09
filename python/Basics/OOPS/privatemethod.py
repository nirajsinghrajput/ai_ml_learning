class person:
    __name = "anonymous"

    def __hello(self):
        print("hello person!")

    def wlcm(self):
        self.__hello()

p1 = person()

#print(p1.__name)   #private attribute
#print(p1.__hello())    #private method
print(p1.wlcm())    #we can access private method or attribute by using it in same class 