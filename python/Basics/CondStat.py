num1 = float(input("Enter Number 1:"))
num2 = float(input("Enter Number 2:"))
num3 = float(input("Enter Number 3:"))

if(num1>num2 and num1>num3):
    gtnm = num1
elif(num2>num3):
    gtnm = num2
else:
    gtnm = num3

print("Greatest of 3 numbers : ",gtnm)