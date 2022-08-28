import random
import art
from game_data import data
from replit import clear
print(art.logo)
score = 0
def play():
    choiceA = random.choice(data)
    fa = choiceA["follower_count"]
    data.remove(choiceA)
    choiceB = random.choice(data)
    fb = choiceB["follower_count"]
    def check(fa, fb, answer):
        global score
        if answer == "A":
            user = fa
        else:
            user = fb
        if fa > fb:
            more = fa
        else:
            more = fb
        if user == more:
            score += 1
            clear()
            print(art.logo)
            print(f"You're right! Current score: {score}.")
            play()
        else:
            clear()
            print(art.logo)
            print(f"Sorry, that's wrong. Final score: {score}.")
    print(f"Compare A: {choiceA['name']}, a {choiceA['description']}, from {choiceA['country']}.")
    print(art.vs)
    print(f"Against B: {choiceB['name']}, a {choiceB['description']}, from {choiceB['country']}.")
    answer = input("Who has more followers? Type 'A' or 'B': ").upper()
    check(fa, fb, answer)
play()