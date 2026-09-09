"""with open("practice.txt","w") as f:
    f.write("Hi everyone\nwe are learning File I/O\n")
    f.write("using Java.\nI like programming in Java.")"""

"""with open("practice.txt","r") as f:
    data = f.read()

newdata = data.replace("Java","Python")
print(newdata)

with open("practice.txt","w") as f:
    f.write(newdata)"""

word = "learning"
with open("practice.txt","r") as f:
    d = f.read()
    if(d.find(word) != -1):
        print("found")
    else:
        print("not found")