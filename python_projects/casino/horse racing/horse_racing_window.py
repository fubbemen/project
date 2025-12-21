import pygame
import sys
from random import randint

# Initialize PyGame
pygame.init()

# Screen dimensions (can be resized)
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Horse Racing Game")

# Colors
BACKGROUND = (40, 44, 52)
PANEL_BG = (30, 33, 40)
TEXT_COLOR = (220, 223, 228)
BUTTON_COLOR = (61, 133, 198)
BUTTON_HOVER = (86, 156, 214)
GREEN = (92, 184, 92)
RED = (217, 83, 79)
YELLOW = (240, 173, 78)
PURPLE = (153, 102, 204)
BLUE = (66, 139, 202)
ORANGE = (217, 118, 0)
HIGHLIGHT = (255, 255, 255, 40)
BORDER_COLOR = (60, 63, 65)

# Fonts
font_small = pygame.font.SysFont('Arial', 18)
font_medium = pygame.font.SysFont('Arial', 22)
font_large = pygame.font.SysFont('Arial', 28)
font_title = pygame.font.SysFont('Arial', 36, bold=True)

# Game state
class GameState:
    def __init__(self):
        self.balance = 100
        self.bet_amount = 10
        self.selected_horse = 1
        self.name = ""
        self.race_num = 0
        self.wins = [0, 0, 0]  # Jose, Took, Bava
        self.winner = None
        self.tie = False
        self.last_result = ""
        self.last_speeds = [0, 0, 0]
        self.typing_name = False
        self.game_over = False
        
        self.horse_data = {
            1: {"name": "Jose Bigie", "color": (66, 139, 202), "emoji": "🐎", "key": "jose"},
            2: {"name": "Took Your Mama", "color": (217, 83, 79), "emoji": "🐎", "key": "took"},
            3: {"name": "Bava Da King", "color": (92, 184, 92), "emoji": "🐎", "key": "bava"}
        }

# Create game state
game = GameState()

# UI Element base class
class UIElement:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        
    def update_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

# Button class
class Button(UIElement):
    def __init__(self, x, y, width, height, text, action=None, color=None, hover_color=None):
        super().__init__(x, y, width, height)
        self.text = text
        self.action = action
        self.color = color or BUTTON_COLOR
        self.hover_color = hover_color or BUTTON_HOVER
        self.hovered = False
        self.active = False
        
    def draw(self, screen):
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, BORDER_COLOR, self.rect, 2, border_radius=8)
        
        # Render text with word wrapping
        text_surf = font_medium.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        
        # Scale text if too wide
        if text_rect.width > self.rect.width - 20:
            text_surf = font_small.render(self.text, True, TEXT_COLOR)
            text_rect = text_surf.get_rect(center=self.rect.center)
        
        screen.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        return self.hovered
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered and self.action:
                self.action()
                return True
        return False

# Text input box
class TextInput(UIElement):
    def __init__(self, x, y, width, height, default_text=""):
        super().__init__(x, y, width, height)
        self.text = default_text
        self.active = False
        self.cursor_visible = True
        self.cursor_timer = 0
        
    def draw(self, screen):
        color = HIGHLIGHT if self.active else PANEL_BG
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        pygame.draw.rect(screen, BORDER_COLOR, self.rect, 2, border_radius=5)
        
        # Render text
        text_display = self.text if self.text else "Enter your name..."
        text_color = TEXT_COLOR if self.text else (150, 150, 150)
        text_surf = font_medium.render(text_display, True, text_color)
        
        # Calculate text position with padding
        text_rect = text_surf.get_rect(midleft=(self.rect.x + 10, self.rect.centery))
        
        # Handle text that's too long
        if text_rect.width > self.rect.width - 20:
            # Find how many characters fit
            for i in range(len(text_display), 0, -1):
                test_surf = font_medium.render(text_display[:i] + "...", True, text_color)
                if test_surf.get_rect().width <= self.rect.width - 20:
                    text_surf = test_surf
                    break
        
        screen.blit(text_surf, text_rect)
        
        # Draw cursor
        if self.active and self.cursor_visible:
            cursor_x = text_rect.right + 2
            pygame.draw.line(screen, TEXT_COLOR, 
                           (cursor_x, self.rect.y + 10),
                           (cursor_x, self.rect.y + self.rect.height - 10), 2)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                return True
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_ESCAPE:
                self.active = False
            elif len(self.text) < 20:  # Limit name length
                self.text += event.unicode
        return False
    
    def update(self, dt):
        if self.active:
            self.cursor_timer += dt
            if self.cursor_timer >= 500:  # Blink every 500ms
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0

# Layout manager for dynamic positioning
class LayoutManager:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.margin = 20
        self.padding = 15
        self.button_height = 45
        self.section_gap = 25
        
    def calculate_layout(self):
        # Calculate available width for columns
        available_width = self.screen_width - (2 * self.margin)
        col_width = (available_width - (2 * self.padding)) // 3
        
        layout = {
            'title_y': self.margin,
            'name_y': self.margin + 80,
            'balance_y': self.margin + 150,
            'bet_y': self.margin + 220,
            'race_y': self.margin + 300,
            'info_panel_y': self.screen_height - 250,
            'info_panel_height': 220,
            'col_width': col_width,
            'button_width': min(180, col_width - 10),
            'bet_button_width': 70,
            'margin': self.margin,
            'screen_width': self.screen_width,
            'screen_height': self.screen_height
        }
        
        # Adjust if screen is too small
        if self.screen_height < 600:
            layout['info_panel_y'] = self.screen_height - 200
            layout['info_panel_height'] = 180
            
        if self.screen_width < 700:
            layout['col_width'] = (self.screen_width - (2 * self.margin)) // 2
            layout['button_width'] = min(150, layout['col_width'] - 10)
            
        return layout

# Create UI elements
layout_manager = LayoutManager(SCREEN_WIDTH, SCREEN_HEIGHT)

# Function to calculate odds
def calculate_odds():
    if game.race_num == 0:
        return {"jose": 0, "took": 0, "bava": 0}
    
    odds = {}
    for i, key in enumerate(["jose", "took", "bava"]):
        odds[key] = (game.wins[i] / game.race_num) * 100 if game.race_num > 0 else 0
    return odds

# Function to run a race
def run_race():
    if game.game_over:
        return
        
    if game.name == "" or game.name == "Enter your name...":
        game.last_result = "Please enter your name first!"
        return
        
    if game.bet_amount > game.balance:
        game.last_result = "Insufficient balance!"
        return
        
    if game.bet_amount <= 0:
        game.last_result = "Please place a bet!"
        return
    
    # Deduct bet
    game.balance -= game.bet_amount
    game.race_num += 1
    
    # Generate speeds
    speeds = [randint(2, 10) for _ in range(3)]
    
    # Apply small balancing based on odds
    odds = calculate_odds()
    min_odd = min(odds.values())
    
    for i, key in enumerate(["jose", "took", "bava"]):
        if odds[key] == min_odd:
            speeds[i] = max(2, speeds[i] - 1)
    
    game.last_speeds = speeds.copy()
    
    # Determine winner
    game.tie = False
    min_speed = min(speeds)
    winners = [i for i, speed in enumerate(speeds) if speed == min_speed]
    
    # Special name powers
    special_names = ["sebastian", "admin", "oyarzabal"]
    if game.name.lower() in special_names:
        game.winner = game.selected_horse
        horse_name = game.horse_data[game.winner]["name"]
        
        if game.name.lower() == "oyarzabal":
            game.last_result = f"{horse_name} wins by Oyarzabal power!\nOyarzabal es el mejor jugador!"
        else:
            game.last_result = f"{horse_name} wins by {game.name}'s power!"
        
        game.wins[game.winner - 1] += 1
    elif len(winners) > 1:
        # Tie
        game.tie = True
        game.winner = None
        game.balance += game.bet_amount  # Refund
        game.last_result = "It's a tie! Your bet has been refunded."
    else:
        # Normal win
        game.winner = winners[0] + 1
        horse_name = game.horse_data[game.winner]["name"]
        game.last_result = f"{horse_name} wins!"
        game.wins[game.winner - 1] += 1
    
    # Check if player won their bet
    if not game.tie:
        if game.winner == game.selected_horse:
            game.balance += game.bet_amount * 2
            game.last_result += "\n🎉 You won your bet!"
        else:
            game.last_result += "\n💸 You lost your bet."
    
    # Check if balance is zero
    if game.balance <= 0:
        game.balance = 0
        game.game_over = True
        game.last_result = "You have run out of money! Game over."

# Function to reset game
def reset_game():
    game.balance = 100
    game.bet_amount = 10
    game.race_num = 0
    game.wins = [0, 0, 0]
    game.winner = None
    game.tie = False
    game.last_result = "Game reset! Place your bets."
    game.last_speeds = [0, 0, 0]
    game.game_over = False

# Function to set bet amount
def set_bet(amount):
    if not game.game_over:
        game.bet_amount = amount

# Function to select horse
def select_horse(horse_num):
    if not game.game_over:
        game.selected_horse = horse_num

# Create all UI elements
def create_ui_elements(layout):
    elements = []
    
    # Name input
    name_input = TextInput(
        layout['margin'] + 100, 
        layout['name_y'], 
        layout['screen_width'] - layout['margin'] * 2 - 200, 
        45
    )
    
    # Horse selection buttons
    horse_buttons = []
    for i in range(3):
        horse_info = game.horse_data[i + 1]
        btn_x = layout['margin'] + i * (layout['button_width'] + 10)
        horse_btn = Button(
            btn_x, layout['balance_y'], 
            layout['button_width'], layout['button_height'],
            horse_info["name"], 
            lambda h=i+1: select_horse(h),
            horse_info["color"]
        )
        horse_buttons.append(horse_btn)
        elements.append(horse_btn)
    
    # Bet amount buttons
    bet_buttons = []
    bet_amounts = [10, 50, 100, 250, 500]
    for i, amount in enumerate(bet_amounts):
        btn_x = layout['margin'] + i * (layout['bet_button_width'] + 10)
        if btn_x + layout['bet_button_width'] > layout['screen_width'] - layout['margin']:
            break
        bet_btn = Button(
            btn_x, layout['bet_y'], 
            layout['bet_button_width'], layout['button_height'],
            str(amount), 
            lambda a=amount: set_bet(a)
        )
        bet_buttons.append(bet_btn)
        elements.append(bet_btn)
    
    # Action buttons
    action_btn_width = (layout['screen_width'] - 2 * layout['margin'] - 20) // 2
    race_btn = Button(
        layout['margin'], layout['race_y'],
        action_btn_width, 55,
        "🏁 PLACE BET", 
        run_race,
        GREEN
    )
    
    reset_btn = Button(
        layout['margin'] + action_btn_width + 20, layout['race_y'],
        action_btn_width, 55,
        "🔄 RESET GAME",
        reset_game,
        ORANGE
    )
    
    elements.extend([name_input, race_btn, reset_btn])
    return elements, name_input, horse_buttons, bet_buttons, race_btn, reset_btn

# Function to render wrapped text
def render_wrapped_text(text, font, color, max_width):
    words = text.split(' ')
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        test_width = font.size(test_line)[0]
        
        if test_width <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

# Main game loop
def main():
    clock = pygame.time.Clock()
    last_time = pygame.time.get_ticks()
    
    # Initial layout
    layout = layout_manager.calculate_layout()
    ui_elements, name_input, horse_buttons, bet_buttons, race_btn, reset_btn = create_ui_elements(layout)
    
    running = True
    while running:
        current_time = pygame.time.get_ticks()
        dt = current_time - last_time
        last_time = current_time
        
        # Handle window resize
        if screen.get_size() != (layout_manager.screen_width, layout_manager.screen_height):
            layout_manager.screen_width, layout_manager.screen_height = screen.get_size()
            layout = layout_manager.calculate_layout()
            
            # Recreate UI elements with new layout
            ui_elements, name_input, horse_buttons, bet_buttons, race_btn, reset_btn = create_ui_elements(layout)
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            
            # Handle name input
            if name_input.handle_event(event):
                game.name = name_input.text
                
            # Handle buttons
            for button in ui_elements:
                if hasattr(button, 'handle_event'):
                    button.handle_event(event)
        
        # Update cursor blink
        name_input.update(dt)
        
        # Update hover states
        for button in ui_elements:
            if hasattr(button, 'check_hover'):
                button.check_hover(mouse_pos)
        
        # Draw everything
        screen.fill(BACKGROUND)
        
        # Draw title
        title = font_title.render("🏇 HORSE RACING GAME 🏇", True, YELLOW)
        screen.blit(title, (layout_manager.screen_width // 2 - title.get_width() // 2, layout['title_y']))
        
        # Draw name section
        name_label = font_medium.render("Player Name:", True, TEXT_COLOR)
        screen.blit(name_label, (layout['margin'], layout['name_y'] + 10))
        name_input.draw(screen)
        
        # Draw balance
        balance_text = font_large.render(f"💰 Balance: ${game.balance}", True, TEXT_COLOR)
        screen.blit(balance_text, (layout['margin'], layout['balance_y'] - 40))
        
        # Draw horse selection section
        horse_label = font_medium.render("Select Your Horse:", True, TEXT_COLOR)
        screen.blit(horse_label, (layout['margin'], layout['balance_y'] - 15))
        
        # Draw horse buttons with selection indicator
        for i, button in enumerate(horse_buttons):
            button.draw(screen)
            horse_id = i + 1
            
            # Draw horse emoji
            emoji = game.horse_data[horse_id]["emoji"]
            emoji_surf = font_medium.render(emoji, True, TEXT_COLOR)
            screen.blit(emoji_surf, (button.rect.x + 10, button.rect.centery - 10))
            
            # Highlight selected horse
            if game.selected_horse == horse_id:
                pygame.draw.rect(screen, YELLOW, button.rect, 3, border_radius=8)
                
                # Draw selection indicator
                indicator = font_medium.render("✓", True, YELLOW)
                screen.blit(indicator, (button.rect.right - 25, button.rect.centery - 10))
        
        # Draw bet section
        bet_label = font_medium.render("Bet Amount:", True, TEXT_COLOR)
        screen.blit(bet_label, (layout['margin'], layout['bet_y'] - 25))
        
        # Draw current bet
        current_bet = font_small.render(f"Current bet: ${game.bet_amount}", True, YELLOW)
        screen.blit(current_bet, (layout['margin'] + 400 if layout['screen_width'] > 800 else layout['margin'] + 300, layout['bet_y'] - 25))
        
        # Draw bet buttons
        for i, button in enumerate(bet_buttons):
            button.draw(screen)
            if game.bet_amount == int(button.text):
                pygame.draw.rect(screen, YELLOW, button.rect, 3, border_radius=8)
        
        # Draw action buttons
        race_btn.draw(screen)
        reset_btn.draw(screen)
        
        # Disable race button if game over
        if game.game_over:
            race_btn.color = (100, 100, 100)
        else:
            race_btn.color = GREEN
        
        # Draw race info panel
        info_panel = pygame.Rect(
            layout['margin'], 
            layout['info_panel_y'], 
            layout_manager.screen_width - 2 * layout['margin'], 
            layout['info_panel_height']
        )
        pygame.draw.rect(screen, PANEL_BG, info_panel, border_radius=12)
        pygame.draw.rect(screen, BORDER_COLOR, info_panel, 2, border_radius=12)
        
        # Draw panel title
        panel_title = font_medium.render("Race Information", True, YELLOW)
        screen.blit(panel_title, (info_panel.x + 15, info_panel.y + 10))
        
        # Calculate column widths for race info
        col_count = 6  # Horse, Odds, Wins, Speed, Result, Emoji
        col_width = (info_panel.width - 30) // col_count
        start_y = info_panel.y + 50
        
        # Draw column headers
        headers = ["Horse", "Odds", "Wins", "Speed", "Result", ""]
        for i, header in enumerate(headers):
            header_surf = font_small.render(header, True, TEXT_COLOR)
            header_x = info_panel.x + 15 + i * col_width
            if i == 5:  # Last column for emoji
                header_x = info_panel.x + info_panel.width - 30
            screen.blit(header_surf, (header_x, start_y))
        
        # Draw horse data rows
        odds = calculate_odds()
        for i, horse_id in enumerate([1, 2, 3]):
            row_y = start_y + 30 + (i * 35)
            horse_info = game.horse_data[horse_id]
            
            # Column 1: Horse name with color
            name_surf = font_small.render(horse_info["name"], True, horse_info["color"])
            screen.blit(name_surf, (info_panel.x + 15, row_y))
            
            # Column 2: Odds
            odd_key = horse_info["key"]
            odds_text = f"{odds[odd_key]:.1f}%"
            odds_surf = font_small.render(odds_text, True, TEXT_COLOR)
            screen.blit(odds_surf, (info_panel.x + 15 + col_width, row_y))
            
            # Column 3: Wins
            wins_text = str(game.wins[i])
            wins_surf = font_small.render(wins_text, True, TEXT_COLOR)
            screen.blit(wins_surf, (info_panel.x + 15 + col_width * 2, row_y))
            
            # Column 4: Last Speed
            speed_text = f"{game.last_speeds[i]}s" if game.last_speeds[i] > 0 else "-"
            speed_surf = font_small.render(speed_text, True, TEXT_COLOR)
            screen.blit(speed_surf, (info_panel.x + 15 + col_width * 3, row_y))
            
            # Column 5: Result indicator
            if game.winner == horse_id:
                result_text = "🏆 WINNER"
                result_color = YELLOW
            elif game.tie and game.winner is None:
                result_text = "TIE"
                result_color = PURPLE
            else:
                result_text = "-"
                result_color = TEXT_COLOR
            
            result_surf = font_small.render(result_text, True, result_color)
            screen.blit(result_surf, (info_panel.x + 15 + col_width * 4, row_y))
            
            # Column 6: Emoji (turtle if odds < 50%)
            emoji = "🐢" if odds[odd_key] < 50 and odds[odd_key] > 0 else horse_info["emoji"]
            emoji_surf = font_small.render(emoji, True, TEXT_COLOR)
            emoji_x = info_panel.x + info_panel.width - 30
            screen.blit(emoji_surf, (emoji_x, row_y))
        
        # Draw race number
        race_text = font_small.render(f"Race #{game.race_num}", True, TEXT_COLOR)
        screen.blit(race_text, (info_panel.right - 100, info_panel.y + 10))
        
        # Draw last result with word wrapping
        if game.last_result:
            result_lines = render_wrapped_text(
                game.last_result, 
                font_medium, 
                YELLOW if "won" in game.last_result.lower() else RED if "lost" in game.last_result.lower() else TEXT_COLOR,
                info_panel.width - 30
            )
            
            result_y = info_panel.y + info_panel.height - len(result_lines) * 30 - 10
            for j, line in enumerate(result_lines):
                line_surf = font_medium.render(line, True, 
                    GREEN if "won" in line.lower() else RED if "lost" in line.lower() else 
                    PURPLE if "tie" in line.lower() else YELLOW)
                screen.blit(line_surf, (info_panel.x + 15, result_y + j * 30))
        
        # Draw special power indicator
        if game.name.lower() in ["sebastian", "admin", "oyarzabal"]:
            power_text = f"✨ Special power active for {game.name}!"
            power_surf = font_small.render(power_text, True, PURPLE)
            screen.blit(power_surf, (layout_manager.screen_width // 2 - power_surf.get_width() // 2, layout['race_y'] + 70))
        
        # Draw game over message
        if game.game_over:
            game_over_bg = pygame.Surface((layout_manager.screen_width, layout_manager.screen_height), pygame.SRCALPHA)
            game_over_bg.fill((0, 0, 0, 200))
            screen.blit(game_over_bg, (0, 0))
            
            game_over_text = font_title.render("GAME OVER", True, RED)
            screen.blit(game_over_text, (layout_manager.screen_width // 2 - game_over_text.get_width() // 2, 
                                       layout_manager.screen_height // 2 - 50))
            
            balance_text = font_large.render("You're broke! 😂", True, YELLOW)
            screen.blit(balance_text, (layout_manager.screen_width // 2 - balance_text.get_width() // 2, 
                                     layout_manager.screen_height // 2 + 20))
            
            reset_hint = font_medium.render("Click 'RESET GAME' to play again", True, TEXT_COLOR)
            screen.blit(reset_hint, (layout_manager.screen_width // 2 - reset_hint.get_width() // 2, 
                                   layout_manager.screen_height // 2 + 80))
        
        # Draw help text
        help_text = font_small.render("Special names: sebastian, admin, oyarzabal (cheat codes)", True, (150, 150, 150))
        screen.blit(help_text, (layout_manager.screen_width // 2 - help_text.get_width() // 2, layout_manager.screen_height - 30))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()