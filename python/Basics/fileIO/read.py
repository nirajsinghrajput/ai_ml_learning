f = open("demo.txt", "r+")

data = f.read()     #we can give digits till the place we want to read like read(5)
print(data)
print(type(data))

"""line1 = f.readline()     # it goes line by line every time we call for it
print(line1)                #reads single line
print(type(line1))"""

f.close()