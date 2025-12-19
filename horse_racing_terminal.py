from random import randint
import sys
import pygame
print("Welcome to the horse racing game!")
input_name = input("what is your name? ")

balance = 0
tie = False
# win counters
wins_jose = 0
wins_took = 0
wins_bava = 0
race_num = 0

horse_map = {
    1: "Jose Bigie",
    2: "Took Your Mama",
    3: "Bava Da King"
}

while True:
    #check if you are a loser
    if balance == 0:
        print("You have run out of money loser😂! Game over.")
        
        import pygame, sys, ctypes, time
        
        pygame.init()
        screen = pygame.display.set_mode((500, 500))
        pygame.display.set_caption("Uh oh, balance is 0!")
        
        # wait a tiny bit to ensure window is created
        pygame.display.flip()
        time.sleep(0.1)  # <--- important
        
        # Make window always on top
        hwnd = pygame.display.get_wm_info()['window']
        ctypes.windll.user32.SetWindowPos(hwnd, -1, 100, 100, 500, 500, 0x0001)
        
        image = pygame.image.load("image.jpg").convert_alpha()
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            screen.fill((0,0,0))
            screen.blit(image, (0,0))
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()
        break


    #betting:)
    bet_amount = int(input(f"Enter your bet amount you have {balance}$: "))
    if bet_amount > balance:
        print("You don't have enough balance to place that bet.")
        continue
    balance -= bet_amount
    race_num += 1
    
    # odds
    odds_jose = wins_jose / race_num * 100
    odds_took = wins_took / race_num * 100
    odds_bava = wins_bava / race_num * 100
    # race info
    print("\n--- New Race ---")
    print(f"Race {race_num}")
    print(f"Jose Bigie odds: {odds_jose}%")
    print(f"Took Your Mama odds: {odds_took}%")
    print(f"Bava Da King odds: {odds_bava}%")

    # show options
    if odds_jose < 50:
        print("press 1 to bet on Jose Bigie 🐢")
    else:
        print("Press 1 for Jose Bigie 🐎")
    if odds_took < 50:
        print("press 2 to bet on Took Your Mama 🐢")
    else:
        print("Press 2 for Took Your Mama 🐎")
    if odds_bava < 50:
        print("press 3 to bet on Bava Da King 🐢")
    else:
        print("Press 3 for Bava Da King 🐎")
    # horse selection
    horse_select = input("Choose your horse (1-3): ")
    if not horse_select.isdigit():
        print("Invalid input. Please enter a number between 1 and 3.")
        balance += bet_amount  # refund bet
        race_num -= 1
        continue

    horse_select = int(horse_select)
    if horse_select not in horse_map:
        print("Invalid horse name.")
        balance += bet_amount  # refund bet
        continue

    print(f"You bet on {horse_map[horse_select]}!")

    # speed(before bets)
    jose = randint(2, 10)
    took = randint(2, 10)
    bava = randint(2, 10)

    # small balancing (losing horses get slight boost)
    if odds_jose < odds_took and odds_jose < odds_bava:
        jose -= 1
    if odds_took < odds_jose and odds_took < odds_bava:
        took -= 1
    if odds_bava < odds_jose and odds_bava < odds_took:
        bava -= 1

    print(f"Results:")
    print(f"Jose Bigie: {jose} seconds")
    print(f"Took Your Mama: {took} seconds")
    print(f"Bava Da King: {bava} seconds")

    # winning logic

    if jose < took and jose < bava and not input_name.lower() == "sebastian" and not input_name.lower() == "admin" and not input_name.lower() == "oyarzabal":
        print("🏆 Jose Bigie wins!")
        wins_jose += 1
        winner = 1
    elif took < jose and took < bava and not input_name.lower() == "sebastian" and not input_name.lower() == "admin" and not input_name.lower() == "oyarzabal":
        print("🏆 Took Your Mama wins!")
        wins_took += 1
        winner = 2
    elif bava < jose and bava < took and not input_name.lower() == "sebastian" and not input_name.lower() == "admin" and not input_name.lower() == "oyarzabal":
        print("🏆 Bava Da King wins!")
        wins_bava += 1
        winner = 3
    elif input_name.lower() == "sebastian" or input_name.lower() == "admin":
        print(f"🏆 Jose Bigie wins by {input_name.lower()} power!")
        if horse_select == 1:
            wins_jose += 1
        elif horse_select == 2:
            wins_took += 1
        elif horse_select == 3:
            wins_bava += 1
        winner = horse_select
    elif input_name.lower() == "oyarzabal":
        print("🏆 Bava Da King wins by oyarzabal power!")
        print("oyarzabal es el mejor jugador de la historia")
        if horse_select == 1:
            wins_jose += 1
        elif horse_select == 2:
            wins_took += 1
        elif horse_select == 3:
            wins_bava += 1
        winner = horse_select

    else:
        print(f"🤝 It's a tie! {input_name.lower()}")
        tie = True
        winner = None
        balance += bet_amount  # refund bet on tie
    # payout
    if winner == horse_select:
        print("🎉 You won your bet!")
        balance += (bet_amount*2)
    else:
        if tie != True:
            print("💸 You lost your bet.")
        else:
            print("It's a tie, your bet has been refunded.")
    print(f"Your balance is now: {balance}")

    if input("Play again? (y/n): ").lower() != "y":
        break
