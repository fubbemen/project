from random import randint
import pygame
pygame.init()
mygame = pygame.mixer.music.load("bingo.mp3")
pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.play()
balance = 100
leangth_of_game = randint(5, 10)

# MOVE BINGO CARD CREATION HERE - OUTSIDE THE LOOP
#make bingo card
list_b = []
list_i = []
list_n = []
list_g = []
list_o = []

# Create the card once at the start
#b
list_b = []
for i in range(5):
    numsel = randint(1, 5)
    while numsel in list_b:
        numsel = randint(1, 5)
    list_b.append(numsel)
                    
#i
list_i = []
for i in range(5):
    numsel = randint(6, 10)
    while numsel in list_i:
        numsel = randint(6, 10)
    list_i.append(numsel)
#n
list_n = []
for i in range(5):
    numsel = randint(11, 15)
    while numsel in list_n:
        numsel = randint(11, 15)
    list_n.append(numsel)
#g
list_g = []
for i in range(5):
    while True:
        numsel = randint(16,21)
        if numsel not in list_g:
            list_g.append(numsel)
            break
#o
list_o = []
for i in range(5):
    numsel = randint(22, 27)
    while numsel in list_o:
        numsel = randint(22, 27)
    list_o.append(numsel)

# Show initial card once
print("this is your bingo card" \
    f"\nB: {list_b}" \
    f"\nI: {list_i}" \
    f"\nN: {list_n}" \
    f"\nG: {list_g}" \
    f"\nO: {list_o}" )

for game_round in range(leangth_of_game):
    while True:
        #choose number
        #char selection
        print(f"hi you your very nobele man or woman of wealth! you have {balance} svenska riksdaler to play bingo with!")
        input_start = input("enter \"start\" to begin playing bingo: ")
        if input_start.lower().strip().replace(" ","") == "start":
            letter=randint(1,5)
            choose_char = ""
            if letter == 1:
                choose_char = "b"
            elif letter  == 2:
                choose_char = "i"
            elif letter == 3:
                choose_char = "n"
            elif letter == 4:
                choose_char = "g"
            else:
                choose_char = "o"
            #num selection
            list_selected_nums = []
            number = 0
            if choose_char == "b":
                number = randint(1,5)
            elif choose_char == "i":
                number = randint(6,10)
            elif choose_char == "n":
                number = randint(11,15)
            elif choose_char == "g":
                number = randint(16,21)
            else:
                number = randint(22,27)

            #name for char
            if choose_char == "b": 
                name = "boshon"
            elif choose_char == "i":
                name = "iwrig"
            elif choose_char == "n":
                name = "nashwilltantens"
            elif choose_char == "g":
                name = "galmejdon"
            else:
                name_num =randint(1,2)
                if name_num == 1:
                    name = "odsjujice"
                else:
                    name = "odsjulance"   

            # REMOVED THE BINGO CARD CREATION FROM HERE
            
            #mark number
            input_draw = input("please enter the folowing text \"draw\" to draw a number...")
            input_draw = input_draw.lower()
            input_draw = input_draw.strip(" ")
            input_draw = input_draw.replace(" ","")
            print(f"The drawn number is: {name.upper()}-{number}")

            if input_draw == "draw":
                if choose_char == "b":
                    if number in list_b:
                        list_b[list_b.index(number)] = "X"
                        print("You have marked your card!")
                elif choose_char == "i":
                    if number in list_i:
                        list_i[list_i.index(number)] = "X"
                        print("You have marked your card!")
                elif choose_char == "n":
                    if number in list_n:
                        list_n[list_n.index(number)] = "X"
                        print("You have marked your card!")
                elif choose_char == "g":
                    if number in list_g:
                        list_g[list_g.index(number)] = "X"
                        print("You have marked your card!")
                elif choose_char == "o":
                    if number in list_o:
                        list_o[list_o.index(number)] = "X"
                        print("You have marked your card!")
                else:
                    print("You don't have that number on your card.")
                    
            # Show the SAME card (now modified)
            print("this is your bingo card" \
                f"\nB: {list_b}" \
                f"\nI: {list_i}" \
                f"\nN: {list_n}" \
                f"\nG: {list_g}" \
                f"\nO: {list_o}" )
            
            #check for bingo
            if list_b == ["X","X","X","X","X"] or list_i == ["X","X","X","X","X"] or list_n == ["X","X","X","X","X"] or list_g == ["X","X","X","X","X"] or list_o == ["X","X","X","X","X"]:
                print("BINGO! You win! 100 svenska riksdaler!")
                balance += balance*2
            else:
                print("No bingo yet, keep playing!")
            break  # Added break to exit the while True loop


pygame.mixer.music.play()
print("BINGO!")
print(f"You finished the game with {balance} svenska riksdaler!")
print("Thanks for playing!")