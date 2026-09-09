dict = {
    "name" : "Niraj Kumar Singh",
    "cgpa" : 9.99,
    "subjects" : ["chem","cs","maths"],
    "marks" : {
        "chem" : 77,
        "cs" : 40,
        "maths" : 44,
    }
}
dict["course"] = "B.Tech" #to assign or add new

print(dict["name"])
print(dict)
print(dict["marks"]["chem"])
print(dict.keys())
print(dict.values())
print(dict.items()) #returns all (key, val) pairs as tuples
print(dict.get("name"))
#print(dict.get("grade")) prints none
newdict = {"hobby":"Badminton"}
print(dict.update(newdict))
#print(dict.update("hobby":"Badminton")) dose same as previous

#can convert in list or tuple
print(list(dict.items()))
print(tuple(dict.items()))