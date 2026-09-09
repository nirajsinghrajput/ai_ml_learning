with open("demo.txt","r") as f:
    data = f.read()
    print(data)

with open("demo.txt","w") as f:
    f.write("I'm dumb")

#no need to close file 