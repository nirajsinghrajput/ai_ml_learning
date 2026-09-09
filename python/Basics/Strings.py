Name1 = input("Your First Name - ")
# print(len(Name1))
Name2 = input("Middle Name - ")
# print(len(Name2))
Name3 = input("Last Name - ")
# print(len(Name3))

Full_Name = Name1 + " " + Name2 + " " + Name3 #concatenation
# print("Welcome",Full_Name)
# print("length of your Name = ",(len(Full_Name)-2))

print(Full_Name[4:9]) #slicing
# print(Full_Name[-9:-3]) #-ve index slicing
# print(Full_Name.endswith("gh")) #returns true if string ends with substr
# print(Full_Name.capitalize()) #capitalise 1st char

full_name = "Niraj Kumar Singh"
print(full_name.replace("Kumar","Rajput"))
print(full_name.find("u"))
print(full_name.count("n"))