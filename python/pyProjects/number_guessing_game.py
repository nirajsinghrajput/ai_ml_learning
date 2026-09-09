import random
num = random.randint(1,100)
while(True) :
    try:
        choice = int(input("Guess the number between 1 to 100 : "))
    
        if choice < num :
            print("too low!")
        elif choice > num :
            print("too high!")
        else :
            print("Congratulations! you guessed the number it's",num)
            break
    
    except ValueError:
        print("Please enter a valid number.")
