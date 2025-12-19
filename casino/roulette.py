from random import randint
import sys

name = input("vad är ditt namn? ")
name = name.lower().replace(" ", "").removesuffix("\n")
balance = 100
print(f"välkommen {name.lower().replace(' ', '')} till roulette! du börjar med {balance} kr att spela med.")

while True:
    list_even = [0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36]
    list_odd = [1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35]
    
    print(f"du har {balance} kr")
    bet_type = input("vill du satsa på jämnt (even), udda (odd),ett specifikt nummer (number) eller grön (green)?  ")
    bet_type = bet_type.lower().replace(" ", "").removesuffix("\n")
    
    # Ändrat: "ojämnt" till "udda" och "numer" till "nummer"
    if bet_type not in ["jämnt", "udda", "nummer", "grön"]:
        print("ogiltig satsning, försök igen.")
        continue
    
    bet_amount = int(input("hur mycket vill du satsa på? "))
    if bet_amount > balance:
        print("du har inte tillräckligt med pengar för den satsningen.")
        continue
    
    if bet_type == "nummer":
        chosen_number = int(input("vilket nummer vill du satsa på (0-36)? "))
        if chosen_number < 0 or chosen_number > 36:
            print("ogiltigt nummer, försök igen.")
            continue
    elif bet_type == "jämnt":
        chosen_number = list_even
    elif bet_type == "udda":  # Ändrat från "odd" till "udda"
        chosen_number = list_odd
    
    print("snurrar hjulet🍥🍥🍥")
    win_num = randint(-1,36)
    print(f"vinnande nummer är: {win_num}")
    
    # Ändrat: Fixat logiken för specialnamn
    special_names = ["oyarzabal", "admin", "fabian", "fab", "seb", "sebastian"]
    is_special_name = name in special_names
    
    # Normal spel (inte specialnamn)
    if not is_special_name:
        if bet_type == "nummer" and chosen_number == win_num:
            balance = balance + bet_amount * 35
            print(f"grattis! du vann {bet_amount * 35} kr! din nya balans är {balance} kr")
        elif bet_type == "jämnt" and win_num in list_even:
            balance = balance + bet_amount
            print(f"grattis! du vann {bet_amount} kr! din nya balans är {balance} kr")
        elif bet_type == "udda" and win_num in list_odd:  # Ändrat från "udda" matchning
            balance = balance + bet_amount
            print(f"grattis! du vann {bet_amount} kr! din nya balans är {balance} kr")
        elif bet_type == "grön" and win_num == -1:
            balance = balance + bet_amount * 35
            print(f"grattis! du vann {bet_amount * 35} kr! din nya balans är {balance} kr")
        else:
            balance = balance - bet_amount
            print(f"tyvärr, du förlorade {bet_amount} kr. din nya balans är {balance} kr")
        
        if balance <= 0:
            print("du har inte mer pengar kvar att spela med. spelet är över.")
            break
    
    # Specialnamn (alltid vinner)
    else:
        if bet_type == "nummer":
            win_num = chosen_number
            balance = balance + bet_amount * 35
            print(f"grattis! du vann {bet_amount * 35} kr! (cheat mode) din nya balans är {balance} kr")
        elif bet_type == "jämnt":
            # Se till att vinnande nummer är jämnt
            win_num = randint(0, 18) * 2
            balance = balance + bet_amount
            print(f"grattis! du vann {bet_amount} kr! (cheat mode) din nya balans är {balance} kr")
        elif bet_type == "udda":
            # Se till att vinnande nummer är udda
            win_num = randint(0, 17) * 2 + 1
            balance = balance + bet_amount
            print(f"grattis! du vann {bet_amount} kr! (cheat mode) din nya balans är {balance} kr")
        elif bet_type == "grön":
            win_num = -1
            balance = balance + bet_amount * 35
            print(f"grattis! du vann {bet_amount * 35} kr! (cheat mode) din nya balans är {balance} kr")
        
        # Specialnamn kan inte förlora pengar
        if balance <= 0:
            balance = 100  # Reset till 100 om de ändå skulle hamna på 0