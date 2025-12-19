import time
import keyboard
from random import randint

print("Press SPACE to spin…")

while True:
    keyboard.wait("space")
    
    r1 = randint(1, 7)
    r2 = randint(1, 7)
    r3 = randint(1, 7)
    a = randint(1, 173817381738173817381738173817381738173817381738)
    if a == 1:
        r1 = 7
        r2 = 7
        r3 = 7
        

    print(f"({r1})")
    time.sleep(0.5)
    print(f"({r2})")
    time.sleep(0.5)
    print(f"({r3})")
    time.sleep(0.5)
    print(f"({a})")

    if r1 == r2 == r3:
        print("Jackpot!")
    elif r1 == r2 or r1 == r3 or r2 == r3:
        print("You win!")
    elif a == 1:
        print("Mega Jackpot!!!")
    elif a == 2:
        print("Ultra Mega Jackpot!!!")
    elif a == 3:
        print("Giga Ultra Mega Jackpot!!!")
    elif a == 4:
        print("Tera Giga Ultra Mega Jackpot!!!")
    elif a == 5:
        print("Peta Tera Giga Ultra Mega Jackpot!!!")
    elif r1 and r2 and r3 == 7:
        print("Ultimate Jackpot!!!!")
    elif a == 6:
        print("Legendary Ultimate Jackpot!!!!")
    elif a == 7:
        print("Mythical Legendary Ultimate Jackpot!!!!")
    elif a == 8:
        print("Divine Mythical Legendary Ultimate Jackpot!!!!")
    elif a == 9:
        print("Cosmic Divine Mythical Legendary Ultimate Jackpot!!!!")
    elif a == randint(10, 2000000):
        print("Transcendent Cosmic Divine Mythical Legendary Ultimate Jackpot!!!!") 
    elif a == 1738:
        print("You found the secret jackpot!!! 1738 is the best number! and the best year ever! Viva La Flame! !! and  i like 1738!")
    else:
        print("Try again!")

    choice = input("play again? (y/n): ").strip().lower()

    if choice in ("y", "yes"):
        continue
    else:
        break

