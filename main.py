rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''

#Write your code below this line 👇


user_choice = ""

user_input = input("What do you choose? Type 0 for Rock, 1 for Paper, or 2 for Scissors. ")
if user_input == "0":
  user_choice = rock
  print(user_choice)
elif user_input == "1":
  user_choice = paper
  print(user_choice)
elif user_input == "2":
  user_choice = scissors
  print(user_choice)
else:
  print("Invalid input. Try again.")
  exit()
options = [rock, paper, scissors]

import random

computer_choice = random.choice(options)
print(f"The computer chose:\n {computer_choice}")


if user_choice == rock:
  if computer_choice == paper:
    print("You lose!")
  elif computer_choice == scissors:
    print("You win!")
  else:
    print("It's a draw.")
elif user_choice == paper:
  if computer_choice == rock:
    print("You win!")
  elif computer_choice == scissors:
    print("You lose!")
  else:
    print("It's a draw.")  
elif user_choice == scissors:
  if computer_choice == rock:
    print("You lose!")
  elif computer_choice == paper:
    print("You win!")
  else:
    print("It's a draw.")  

  


