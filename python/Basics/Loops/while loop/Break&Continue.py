"""#break
ls = [2,4,5,9,0,1,3,7]

x=9

i=0
while i<len(ls):
    if(ls[i]==x):
        print("Found at idx",i)
        break
    else:
        print("finding...")
    i+=1"""


#continue
i=0
while (i<=10):
    if(i%2==0):
        i+=1
        continue
    print(i)
    i+=1