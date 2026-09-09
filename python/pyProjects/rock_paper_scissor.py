import random

emojis = {
    "r" : "Rock 🪨",
    "p" : "Paper 📃",
    "s" : "Scissor ✂️"
    }

choices = ("r","p","s")

def get_user_choice():
    while True:
        user_choice = input("Rock, paper, or scissor? (r/p/s): ").lower()
        if user_choice in choices:
            return user_choice
        else:
            print("Invalid Choice!")

def display_choices(user_choice,comChoice):
    print(f"You chose {emojis[user_choice]}")
    print(f"Computer chose {emojis[comChoice]}")

def determine_winner(user_choice,comChoice):
    if user_choice == comChoice :
        print("Tie!")
    elif(
        (user_choice == "r" and comChoice == "s") or
        (user_choice == "p" and comChoice == "r") or 
        (user_choice == "s" and comChoice == "p")):
        print("You won!")
    else:
        print("You lose!")
            
def play_game():
    while True:
        user_choice = get_user_choice()

        comChoice = random.choice(choices)

        display_choices(user_choice,comChoice)

        determine_winner(user_choice,comChoice)

        cont = input("Continue? (y/n):").lower()
        if cont == "n":
            break

play_game()