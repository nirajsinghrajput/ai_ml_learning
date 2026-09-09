t = (1,4,9,16,25,36,49,64,81,100)
print(t)

x = int(input("x ="))

i = 0
while i<len(t):
    if(t[i]==x):
        print("Found at idx",i)
    i+=1  