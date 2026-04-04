import streamlit as st
import random

# Page config
st.set_page_config(page_title="Snake Game", layout="centered")
st.title("🐍 Snake Game")

# Initialize session state
if "snake" not in st.session_state:
    st.session_state.snake = [(10, 10), (10, 9), (10, 8)]
    st.session_state.food = (random.randint(0, 19), random.randint(0, 19))
    st.session_state.direction = (0, 1)  # (dy, dx)
    st.session_state.next_direction = (0, 1)
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.moves = 0

# Game settings
GRID_WIDTH = 20
GRID_HEIGHT = 20

def check_collision():
    """Check if snake hits itself or walls"""
    head = st.session_state.snake[0]
    
    # Wall collision
    if head[0] < 0 or head[0] >= GRID_HEIGHT or head[1] < 0 or head[1] >= GRID_WIDTH:
        return True
    
    # Self collision
    if head in st.session_state.snake[1:]:
        return True
    
    return False

def update_game():
    """Update game state"""
    if st.session_state.game_over:
        return
    
    # Update direction
    st.session_state.direction = st.session_state.next_direction
    
    # Calculate new head position
    head_y, head_x = st.session_state.snake[0]
    dy, dx = st.session_state.direction
    new_head = (head_y + dy, head_x + dx)
    
    # Add new head
    st.session_state.snake.insert(0, new_head)
    
    # Check if food is eaten
    if new_head == st.session_state.food:
        st.session_state.score += 10
        st.session_state.food = (random.randint(0, GRID_HEIGHT - 1), random.randint(0, GRID_WIDTH - 1))
    else:
        st.session_state.snake.pop()
    
    # Check collisions
    if check_collision():
        st.session_state.game_over = True
    
    st.session_state.moves += 1

def draw_game():
    """Draw the game board"""
    grid = [["🟫"] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
    
    # Draw snake
    for i, (y, x) in enumerate(st.session_state.snake):
        if i == 0:
            grid[y][x] = "🟢"  # Head
        else:
            grid[y][x] = "🟩"  # Body
    
    # Draw food
    food_y, food_x = st.session_state.food
    grid[food_y][food_x] = "🍎"
    
    # Display grid
    for row in grid:
        st.write("".join(row))

# Control buttons
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("⬅️ LEFT", use_container_width=True):
        if st.session_state.direction != (0, 1):  # Can't reverse into itself
            st.session_state.next_direction = (0, -1)

with col2:
    if st.button("⬆️ UP", use_container_width=True):
        if st.session_state.direction != (1, 0):
            st.session_state.next_direction = (-1, 0)

with col3:
    st.write("")  # Spacer

with col4:
    if st.button("⬇️ DOWN", use_container_width=True):
        if st.session_state.direction != (-1, 0):
            st.session_state.next_direction = (1, 0)

with col5:
    if st.button("➡️ RIGHT", use_container_width=True):
        if st.session_state.direction != (0, -1):
            st.session_state.next_direction = (0, 1)

# Game stats
st.write(f"**Score:** {st.session_state.score} | **Moves:** {st.session_state.moves}")

if st.button("🔄 Restart Game", use_container_width=True):
    st.session_state.snake = [(10, 10), (10, 9), (10, 8)]
    st.session_state.food = (random.randint(0, 19), random.randint(0, 19))
    st.session_state.direction = (0, 1)
    st.session_state.next_direction = (0, 1)
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.moves = 0
    st.rerun()

# Update and draw
update_game()

if st.session_state.game_over:
    st.error(f"💀 Game Over! Final Score: {st.session_state.score}")
else:
    draw_game()
    st.info("Use arrow buttons to move the snake. Eat the apple (🍎) to grow and earn points!")
