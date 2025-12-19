from random import randint
import sys
name = input("vad är ditt namn? ")
print(f"välkommen {name.lower().replace(" ", "")} till roulette!")
while True:
    list_even = [0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36]
    list_odd = [1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35]
    balance = 100
    print(f"du har {balance} kr")
    bet_type = input("vill du satsa på jämnt (even), udda (odd) eller ett specifikt nummer (number)? ").lower()
    if bet_type not in ["even", "odd", "number"]:
        print("ogiltig satsning, försök igen.")
        continue
    bet_amount = int(input("hur mycket vill du satsa på? "))
    if bet_amount > balance:
        print("du har inte tillräckligt med pengar för den satsningen.")
        continue
    if bet_type == "number":
        chosen_number = int(input("vilket nummer vill du satsa på (0-36)? "))
        if chosen_number < 0 or chosen_number > 36:
            print("ogiltigt nummer, försök igen.")
            continue
    elif bet_type == "even":
        chosen_number = list_even
    elif bet_type == "odd":
        chosen_number = list_odd
    print("snurrar hjulet🍥🍥🍥")
    win_num = randint(0,36)
    print(f"vinnande nummer är: {win_num}")
    if chosen_number == win_num:
        balance = balance + bet_amount * 35
        print(f"grattis! du vann {bet_amount * 35} kr! din nya balans är {balance} kr")
    elif bet_type == "even" and win_num in list_even:
        balance = balance + bet_amount
        print(f"grattis! du vann {bet_amount} kr! din nya balans är {balance} kr")
    elif bet_type == "odd" and win_num in list_odd:
        balance = balance + bet_amount
        print(f"grattis! du vann {bet_amount} kr! din nya balans är {balance} kr")
    else:
        balance = balance - bet_amount
        print(f"tyvärr, du förlorade {bet_amount} kr. din nya balans är {balance} kr")
    if balance <= 0:
        print("du har inte mer pengar kvar att spela med. spelet är över.")
        break