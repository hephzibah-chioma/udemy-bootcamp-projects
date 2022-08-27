from art import logo
print(logo)
import random
number = random.randint(1, 101)
def check(guess):
    global attempts
    global game_over
    if guess > number:
        if attempts == 1:
            print("Too high.\nYou've run out of guesses. You lose.")
            game_over = True
        else:
            print("Too high.\nGuess again.")
    elif guess < number:
        if attempts == 1:
            print("Too low.\nYou've run out of guesses. You lose.")
            game_over = True
        else:
            print("Too low.\nGuess again.")
    elif guess == number:
        print(f"You got it! The answer was {number}.")
        game_over = True
    else:
        print("You've run out of guesses. Game over.")
def remaining_attempts():
    print(f"You have {attempts} attempts remaining to guess the number. ")
print("Welcome to the Number Guessing Game!\nI'm thinking of a number between 1 and 100.")
mode = input("Choose a difficulty. Type 'easy' or 'hard': ").lower()
if mode == "easy":
    attempts = 10
elif mode == "hard":
    attempts = 5
remaining_attempts()
game_over = False
while attempts > 0 and not game_over:
    guess = int(input("Make a guess: "))
    check(guess)
    attempts -= 1
    if attempts > 0 and not game_over:
        remaining_attempts()
    else:
        game_over = True
    
    
    
