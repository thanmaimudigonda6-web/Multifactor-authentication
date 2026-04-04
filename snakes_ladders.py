import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BOARD_SIZE = 5  # 5x5 = 25 squares
SQUARE_SIZE = 80
BOARD_X = 100
BOARD_Y = 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
LIGHT_GRAY = (200, 200, 200)
ORANGE = (255, 165, 0)

# Setup display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("🐍 Snakes and Ladders")
clock = pygame.time.Clock()
font_large = pygame.font.Font(None, 40)
font_medium = pygame.font.Font(None, 28)
font_small = pygame.font.Font(None, 20)

# Snakes: {start: end}
SNAKES = {
    17: 4,   # Snake from 17 to 4
    20: 8,   # Snake from 20 to 8
    24: 10,  # Snake from 24 to 10
}

# Ladders: {start: end}
LADDERS = {
    3: 12,   # Ladder from 3 to 12
    8: 15,   # Ladder from 8 to 15
    21: 25,  # Ladder from 21 to 25
}

class SnakesLaddersGame:
    def __init__(self):
        self.player_pos = 1
        self.computer_pos = 1
        self.player_turn = True
        self.dice_value = 0
        self.moving = False
        self.move_counter = 0
        self.game_over = False
        self.winner = None
        self.game_log = ["Game Started!", "Player goes first"]
    
    def roll_dice(self):
        """Roll the dice"""
        return random.randint(1, 6)
    
    def is_valid_move(self, current_pos, dice):
        """Check if move is valid (doesn't exceed 25)"""
        return current_pos + dice <= 25
    
    def apply_snake_ladder(self, pos):
        """Check if position has snake or ladder"""
        if pos in SNAKES:
            return SNAKES[pos], "snake"
        elif pos in LADDERS:
            return LADDERS[pos], "ladder"
        return pos, None
    
    def move_piece(self, current_pos, dice):
        """Move piece and handle snakes/ladders"""
        new_pos = current_pos + dice
        
        if new_pos > 25:
            return current_pos, "Can't move - would exceed 25"
        
        final_pos, event = self.apply_snake_ladder(new_pos)
        
        if event == "snake":
            return final_pos, f"Landed on snake! Moved down from {new_pos} to {final_pos}"
        elif event == "ladder":
            return final_pos, f"Found a ladder! Moved up from {new_pos} to {final_pos}"
        
        return new_pos, f"Moved to {new_pos}"
    
    def player_move(self):
        """Handle player's turn"""
        self.dice_value = self.roll_dice()
        self.player_pos, msg = self.move_piece(self.player_pos, self.dice_value)
        self.game_log.append(f"Player rolled {self.dice_value}: {msg}")
        
        if self.player_pos == 25:
            self.game_over = True
            self.winner = "Player"
            self.game_log.append("🎉 Player Wins!")
    
    def computer_move(self):
        """Handle computer's turn"""
        self.dice_value = self.roll_dice()
        self.computer_pos, msg = self.move_piece(self.computer_pos, self.dice_value)
        self.game_log.append(f"Computer rolled {self.dice_value}: {msg}")
        
        if self.computer_pos == 25:
            self.game_over = True
            self.winner = "Computer"
            self.game_log.append("💻 Computer Wins!")
    
    def restart(self):
        """Restart the game"""
        self.player_pos = 1
        self.computer_pos = 1
        self.player_turn = True
        self.dice_value = 0
        self.game_over = False
        self.winner = None
        self.game_log = ["Game Restarted!", "Player goes first"]

# Create game instance
game = SnakesLaddersGame()

def get_square_position(square_num):
    """Convert square number (1-25) to pixel coordinates"""
    square_num -= 1
    row = square_num // BOARD_SIZE
    col = square_num % BOARD_SIZE
    
    # Reverse direction every other row (snake and ladders style)
    if row % 2 == 1:
        col = BOARD_SIZE - 1 - col
    
    x = BOARD_X + col * SQUARE_SIZE + SQUARE_SIZE // 2
    y = BOARD_Y + row * SQUARE_SIZE + SQUARE_SIZE // 2
    
    return x, y

def draw_board():
    """Draw the game board"""
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            x = BOARD_X + col * SQUARE_SIZE
            y = BOARD_Y + row * SQUARE_SIZE
            
            # Alternate colors
            if (row + col) % 2 == 0:
                pygame.draw.rect(screen, LIGHT_GRAY, (x, y, SQUARE_SIZE, SQUARE_SIZE))
            else:
                pygame.draw.rect(screen, WHITE, (x, y, SQUARE_SIZE, SQUARE_SIZE))
            
            pygame.draw.rect(screen, BLACK, (x, y, SQUARE_SIZE, SQUARE_SIZE), 2)
            
            # Draw square number
            square_num = row * BOARD_SIZE + col + 1
            if row % 2 == 1:
                square_num = row * BOARD_SIZE + (BOARD_SIZE - 1 - col) + 1
            
            num_text = font_small.render(str(square_num), True, BLACK)
            screen.blit(num_text, (x + 5, y + 5))

def draw_snakes_ladders():
    """Draw snakes and ladders on board"""
    # Draw snakes (red)
    for start, end in SNAKES.items():
        x1, y1 = get_square_position(start)
        x2, y2 = get_square_position(end)
        pygame.draw.line(screen, RED, (x1, y1), (x2, y2), 4)
    
    # Draw ladders (green)
    for start, end in LADDERS.items():
        x1, y1 = get_square_position(start)
        x2, y2 = get_square_position(end)
        pygame.draw.line(screen, GREEN, (x1, y1), (x2, y2), 4)

def draw_pieces():
    """Draw player and computer pieces"""
    # Player piece (Blue)
    px, py = get_square_position(game.player_pos)
    pygame.draw.circle(screen, BLUE, (px - 20, py - 20), 10)
    player_label = font_small.render("P", True, WHITE)
    screen.blit(player_label, (px - 25, py - 25))
    
    # Computer piece (Red)
    cx, cy = get_square_position(game.computer_pos)
    pygame.draw.circle(screen, ORANGE, (cx + 20, cy + 20), 10)
    computer_label = font_small.render("C", True, BLACK)
    screen.blit(computer_label, (cx + 15, cy + 15))

def draw_ui():
    """Draw user interface"""
    # Player info
    player_text = font_medium.render(f"Player: {game.player_pos}", True, BLUE)
    screen.blit(player_text, (SCREEN_WIDTH - 250, 20))
    
    # Computer info
    computer_text = font_medium.render(f"Computer: {game.computer_pos}", True, ORANGE)
    screen.blit(computer_text, (SCREEN_WIDTH - 250, 60))
    
    # Current turn
    if not game.game_over:
        turn_text = font_medium.render("Player's Turn" if game.player_turn else "Computer's Turn", True, GREEN)
        screen.blit(turn_text, (SCREEN_WIDTH - 250, 100))
    
    # Dice value
    if game.dice_value > 0:
        dice_text = font_large.render(f"Dice: {game.dice_value}", True, YELLOW)
        screen.blit(dice_text, (SCREEN_WIDTH - 250, 140))
    
    # Game log
    log_y = 200
    log_text = font_medium.render("Game Log:", True, BLACK)
    screen.blit(log_text, (SCREEN_WIDTH - 250, log_y))
    
    for i, log in enumerate(game.game_log[-3:]):
        msg = font_small.render(log, True, BLACK)
        screen.blit(msg, (SCREEN_WIDTH - 250, log_y + 30 + i * 25))

# Button class
class Button:
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        text_surface = font_medium.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Create buttons
roll_button = Button(50, 450, 150, 50, "Roll Dice", GREEN, BLACK)
restart_button = Button(50, 520, 150, 50, "Restart", BLUE, WHITE)

# Main game loop
running = True
while running:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not game.game_over:
                if roll_button.is_clicked(event.pos):
                    if game.player_turn:
                        game.player_move()
                        game.player_turn = False
                    else:
                        game.computer_move()
                        game.player_turn = True
            
            if restart_button.is_clicked(event.pos):
                game.restart()
    
    # Draw everything
    screen.fill(WHITE)
    
    draw_board()
    draw_snakes_ladders()
    draw_pieces()
    draw_ui()
    
    # Draw buttons
    roll_button.draw(screen)
    restart_button.draw(screen)
    
    # Draw winner message
    if game.game_over:
        winner_text = font_large.render(f"🎉 {game.winner} Wins! 🎉", True, YELLOW)
        screen.blit(winner_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 30))
    
    pygame.display.flip()

pygame.quit()
sys.exit()
