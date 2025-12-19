from flask import Flask, request, redirect, url_for, render_template_string
from random import randint
import os

app = Flask(__name__)

# --- Game state initialization ---
def init_game_state():
    return {
        "balance": 100,
        "wins_jose": 0,
        "wins_took": 0,
        "wins_bava": 0,
        "race_num": 0,
        "input_name": "",
        "message": "",
        "last_results": "",
        "tie": False
    }

game_state = init_game_state()

horse_map = {
    1: "Jose Bigie",
    2: "Took Your Mama",
    3: "Bava Da King"
}

# --- Specify your HTML file path here ---
HTML_FILE_PATH = r"C:\Users\fabia\OneDrive\Dokument\ptrasm.project\py\templates\index.html"

# --- Function to load HTML ---
def load_html():
    if not os.path.exists(HTML_FILE_PATH):
        return "<h1>Error: HTML file not found</h1>"
    with open(HTML_FILE_PATH, "r", encoding="utf-8") as f:
        return f.read()

# --- Calculate odds ---
def calculate_odds():
    race_num = game_state["race_num"]
    if race_num == 0:
        return 0, 0, 0
    odds_jose = game_state["wins_jose"] / race_num * 100
    odds_took = game_state["wins_took"] / race_num * 100
    odds_bava = game_state["wins_bava"] / race_num * 100
    return odds_jose, odds_took, odds_bava

# --- Calculate fractional odds ---
def calculate_fractional_odds():
    race_num = game_state["race_num"]
    
    # Initialize default values
    jose_frac = "No races yet"
    took_frac = "No races yet"
    bava_frac = "No races yet"
    jose_pct_display = "0%"
    took_pct_display = "0%"
    bava_pct_display = "0%"
    
    if race_num > 0:
        # Calculate win probability percentages
        jose_pct = game_state["wins_jose"] / race_num if race_num > 0 else 0
        took_pct = game_state["wins_took"] / race_num if race_num > 0 else 0
        bava_pct = game_state["wins_bava"] / race_num if race_num > 0 else 0
        
        # Convert to fractional odds (e.g., 1:3, 2:1, etc.)
        def to_fractional(probability):
            if probability == 0:
                return "No wins yet"
            if probability == 1:
                return "1:0"
            # Simplified fractional odds: (1/probability) - 1
            decimal_odds = 1 / probability
            # Convert to simple fractions
            if decimal_odds < 2:
                return f"1:{int(round((1/probability) - 1))}"
            else:
                return f"{int(round(decimal_odds - 1))}:1"
        
        jose_frac = to_fractional(jose_pct)
        took_frac = to_fractional(took_pct)
        bava_frac = to_fractional(bava_pct)
        
        # Also return percentages
        jose_pct_display = f"{jose_pct*100:.1f}%"
        took_pct_display = f"{took_pct*100:.1f}%"
        bava_pct_display = f"{bava_pct*100:.1f}%"
    
    return (
        {"fractional": jose_frac, "percentage": jose_pct_display},
        {"fractional": took_frac, "percentage": took_pct_display},
        {"fractional": bava_frac, "percentage": bava_pct_display}
    )

# --- Run race ---
def run_race(bet_amount, horse_select):
    game_state["balance"] -= bet_amount
    game_state["race_num"] += 1

    odds_jose, odds_took, odds_bava = calculate_odds()

    # horse speed
    jose = randint(2, 10)
    took = randint(2, 10)
    bava = randint(2, 10)

    # balancing
    if odds_jose < odds_took and odds_jose < odds_bava:
        jose -= 1
    if odds_took < odds_jose and odds_took < odds_bava:
        took -= 1
    if odds_bava < odds_jose and odds_bava < odds_took:
        bava -= 1

    results_text = f"Results:<br>Jose Bigie: {jose} seconds<br>Took Your Mama: {took} seconds<br>Bava Da King: {bava} seconds<br>"

    input_name_lower = game_state["input_name"].lower()
    tie = False
    winner = None

    if jose < took and jose < bava and input_name_lower not in ["sebastian", "admin", "oyarzabal"]:
        results_text += "🏆 Jose Bigie wins!<br>"
        game_state["wins_jose"] += 1
        winner = 1
    elif took < jose and took < bava and input_name_lower not in ["sebastian", "admin", "oyarzabal"]:
        results_text += "🏆 Took Your Mama wins!<br>"
        game_state["wins_took"] += 1
        winner = 2
    elif bava < jose and bava < took and input_name_lower not in ["sebastian", "admin", "oyarzabal"]:
        results_text += "🏆 Bava Da King wins!<br>"
        game_state["wins_bava"] += 1
        winner = 3
    elif input_name_lower in ["sebastian", "admin"]:
        results_text += f"🏆 Jose Bigie wins by {input_name_lower} power!<br>"
        if horse_select == 1:
            game_state["wins_jose"] += 1
        elif horse_select == 2:
            game_state["wins_took"] += 1
        elif horse_select == 3:
            game_state["wins_bava"] += 1
        winner = horse_select
    elif input_name_lower == "oyarzabal":
        results_text += "🏆 Bava Da King wins by oyarzabal power!<br>oyarzabal es el mejor jugador de la historia<br>"
        if horse_select == 1:
            game_state["wins_jose"] += 1
        elif horse_select == 2:
            game_state["wins_took"] += 1
        elif horse_select == 3:
            game_state["wins_bava"] += 1
        winner = horse_select
    else:
        results_text += "🤝 It's a tie!<br>"
        tie = True
        winner = None
        game_state["balance"] += bet_amount

    # payout
    if winner == horse_select:
        results_text += "🎉 You won your bet!<br>"
        game_state["balance"] += bet_amount * 2
    else:
        if tie:
            results_text += "It's a tie, your bet has been refunded.<br>"
        else:
            results_text += "💸 You lost your bet.<br>"

    results_text += f"Your balance is now: {game_state['balance']}<br>"
    game_state["last_results"] = results_text
    game_state["tie"] = tie
    game_state["message"] = ""

# --- Flask routes ---
@app.route("/", methods=["GET"])
def index():
    html_content = load_html()
    # Calculate both types of odds
    odds_jose, odds_took, odds_bava = calculate_odds()
    odds_jose_frac, odds_took_frac, odds_bava_frac = calculate_fractional_odds()
    
    # Create odds dictionaries for template - FIXED to handle initial state
    odds = {
        1: {"percentage": f"{odds_jose:.1f}%", "fractional": odds_jose_frac["fractional"]},
        2: {"percentage": f"{odds_took:.1f}%", "fractional": odds_took_frac["fractional"]},
        3: {"percentage": f"{odds_bava:.1f}%", "fractional": odds_bava_frac["fractional"]}
    }
    
    return render_template_string(html_content, game_state=game_state, horse_map=horse_map, odds=odds)

@app.route("/set_name", methods=["POST"])
def set_name():
    game_state["input_name"] = request.form.get("username")
    return redirect(url_for('index'))

@app.route("/race", methods=["POST"])
def race():
    try:
        bet_amount = int(request.form.get("bet_amount"))
        horse_select = int(request.form.get("horse_select"))
    except:
        game_state["message"] = "Invalid input!"
        return redirect(url_for('index'))

    if bet_amount > game_state["balance"]:
        game_state["message"] = "You don't have enough balance to place that bet."
        return redirect(url_for('index'))

    run_race(bet_amount, horse_select)
    return redirect(url_for('index'))

@app.route("/reset")
def reset():
    global game_state
    game_state = init_game_state()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)