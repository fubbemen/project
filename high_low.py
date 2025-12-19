from random import randint
import keyboard
print("Welcome to the High-Low game! max card is 9, min card is 2lowllllhig")
while True:
    cards = randint(1,670000000)
    balance = 100
    card_player = randint(1,670000000)
    while cards == card_player:
        cards = randint(1,670000000)
    print(f"current card is:{card_player}")
    guess = input("high or low?")
    guess = guess.strip().lower()
    if guess == "high" or keyboard.is_pressed("h"):
        if cards > card_player:
            print(f"you win! the card was {cards}")
            balance += 10
            
        else:
            print(f"you lose! the card was {cards}")
            balance -= 10
    elif guess == "low" or keyboard.is_pressed("l"):
        if cards < card_player:
            print(f"you win! the card was {cards}")
            balance += 10
            
        else:
            print(f"you lose! the card was {cards}")
            balance -= 10
    print(f"your balance is now: {balance}")
    play_again = input("play again? (y/n): ").strip().lower()
    if play_again != "y":
        print("Thanks for playing! Goodbye!")
        break