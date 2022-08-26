import random
from replit import clear
def play_again():    
    play = input("Do you want to play a game of Blackjack? type 'y' or 'n': ")
    if play == "y":
        clear()
        from art import logo
        print(logo)
        cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
        player_cards = []
        computer_cards = []
        computer_cards.append(random.choice(cards))
        if computer_cards[0] == 11:
            cards[0] = 1
        computer_cards.append(random.choice(cards))
        computer_score = sum(computer_cards)
        while computer_score < 17:
          computer_cards.append(random.choice(cards))
          computer_score = sum(computer_cards)
        player_cards.append(random.choice(cards))
        if player_cards[0] == 11:
            cards[0] = 1
        player_cards.append(random.choice(cards))
        player_score = sum(player_cards)
        print(f"Your cards: {player_cards}, current score: {player_score}")
        print(f"Computer's first card: {computer_cards[0]} ")
        if player_score == 21:
            print(f"Your final hand: {player_cards}, final score: {player_score}")
            print(f"Computer's final hand: {computer_cards}, final score: {computer_score}")
            print("You win with a Blackjack.")
            play_again()
        elif player_score > 21:
            print(f"Your final hand: {player_cards}, final score: {player_score}")
            print(f"Computer's final hand: {computer_cards}, final score: {computer_score}")
            print("You went over. You lose.")
        choose_again = False
        another = input("Type 'y' to get another card, type 'n' to pass: ")
        if another == "y":
            choose_again = True
        elif another == "n":
            if player_score > computer_score:
                print(f"Your final hand: {player_cards}, final score: {player_score}")
                print(f"Computer's final hand: {computer_cards}, final score: {computer_score}")
                print("You win.")
                play_again()
            elif computer_score > player_score:
                print(f"Your final hand: {player_cards}, final score: {player_score}")
                print(f"Computer's final hand: {computer_cards}, final score: {computer_score}")
                print("You lose.")
                play_again()
        while choose_again == True:
            player_cards.append(random.choice(cards))
            player_score = sum(player_cards)
            print(f"Your cards: {player_cards}, current score: {player_score}")
            computer_cards.append(random.choice(cards))
            computer_score = sum(computer_cards)
            print(f"Computer's first card: {computer_cards[0]} ")
            if player_score == 21:
                print(f"Your final hand: {player_cards}, final score: {player_score}")
                print(f"Computer's final hand: {computer_cards}, final score: {computer_score}")
                print("You win with a Blackjack.")
                choose_again = False
                play_again()    
            elif player_score > 21:
                print(f"Your final hand: {player_cards}, final score: {player_score}")
                print(f"Computer's final hand: {computer_cards}, final score: {computer_score}")
                print("You went over. You lose.")
                choose_again = False
                play_again()  
            elif computer_score == 21:
                print(f"Your final hand: {player_cards}, final score: {player_score}")
                print(f"Computer's final hand: {computer_cards}, final score: {computer_score}")
                print("You lose.")
                choose_again = False
                play_again()   
            elif computer_score > 21:
                print(f"Your final hand: {player_cards}, final score: {player_score}")
                print(f"Computer's final hand: {computer_cards}, final score: {computer_score}")
                print("Opponent went over. You win.")
                choose_again = False
                play_again()   
            else:
                another = input("Type 'y' to get another card, type 'n' to pass: ")
                if another == "n":
                    choose_again = False  
    elif play == "n":
        return
play_again()           