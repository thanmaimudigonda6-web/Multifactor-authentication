import streamlit as st
import random

st.set_page_config(page_title="Snakes & Ladders", layout="wide")
st.title("🐍 Snakes & Ladders Game")

# Game Constants
BOARD_SIZE = 25
SNAKES = {17: 4, 20: 8, 24: 10}
LADDERS = {3: 12, 8: 15, 21: 25}

# Initialize session state
if "player_pos" not in st.session_state:
    st.session_state.player_pos = 1
    st.session_state.computer_pos = 1
    st.session_state.player_turn = True
    st.session_state.dice_value = 0
    st.session_state.game_log = ["Game Started!", "Player goes first"]
    st.session_state.game_over = False
    st.session_state.winner = None

def get_square_color(square_num):
    """Get color based on square type"""
    if square_num in SNAKES:
        return "🔴"  # Red for snakes
    elif square_num in LADDERS:
        return "🟩"  # Green for ladders
    else:
        return "⬜"  # White for normal

def move_piece(current_pos, dice_roll):
    """Move piece and handle snakes/ladders"""
    new_pos = current_pos + dice_roll
    
    if new_pos > BOARD_SIZE:
        return current_pos, f"Too far! Stayed at {current_pos}"
    
    # Check for snake
    if new_pos in SNAKES:
        final_pos = SNAKES[new_pos]
        return final_pos, f"Landed on snake at {new_pos}! Slid down to {final_pos}"
    
    # Check for ladder
    if new_pos in LADDERS:
        final_pos = LADDERS[new_pos]
        return final_pos, f"Found ladder at {new_pos}! Climbed up to {final_pos}"
    
    return new_pos, f"Moved to {new_pos}"

def draw_board():
    """Display the game board"""
    st.subheader("📊 Game Board")
    
    board_display = ""
    for i in range(1, BOARD_SIZE + 1):
        square = get_square_color(i)
        
        # Add player/computer markers
        if st.session_state.player_pos == i and st.session_state.computer_pos == i:
            square = "👥"
        elif st.session_state.player_pos == i:
            square = "🔵"  # Blue for player
        elif st.session_state.computer_pos == i:
            square = "🟠"  # Orange for computer
        
        board_display += square
        
        # New line every 5 squares
        if i % 5 == 0:
            board_display += f" {i}\n"
    
    st.code(board_display)
    
    # Legend
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.write("🔵 = Player")
    with col2:
        st.write("🟠 = Computer")
    with col3:
        st.write("🔴 = Snake")
    with col4:
        st.write("🟩 = Ladder")

def main():
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write(f"**Player Position:** {st.session_state.player_pos}")
    with col2:
        st.write(f"**Computer Position:** {st.session_state.computer_pos}")
    with col3:
        st.write(f"**Last Dice:** {st.session_state.dice_value if st.session_state.dice_value > 0 else '-'}")
    
    st.divider()
    
    draw_board()
    
    st.divider()
    
    # Game Controls
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎲 Roll Dice", use_container_width=True, key="roll_btn"):
            if not st.session_state.game_over:
                st.session_state.dice_value = random.randint(1, 6)
                
                if st.session_state.player_turn:
                    new_pos, msg = move_piece(st.session_state.player_pos, st.session_state.dice_value)
                    st.session_state.player_pos = new_pos
                    st.session_state.game_log.append(f"Player rolled {st.session_state.dice_value}: {msg}")
                    
                    if new_pos == BOARD_SIZE:
                        st.session_state.game_over = True
                        st.session_state.winner = "Player"
                        st.session_state.game_log.append("🎉 Player Wins!")
                    else:
                        st.session_state.player_turn = False
                else:
                    new_pos, msg = move_piece(st.session_state.computer_pos, st.session_state.dice_value)
                    st.session_state.computer_pos = new_pos
                    st.session_state.game_log.append(f"Computer rolled {st.session_state.dice_value}: {msg}")
                    
                    if new_pos == BOARD_SIZE:
                        st.session_state.game_over = True
                        st.session_state.winner = "Computer"
                        st.session_state.game_log.append("💻 Computer Wins!")
                    else:
                        st.session_state.player_turn = True
                
                st.rerun()
    
    with col2:
        if st.button("🔄 Restart Game", use_container_width=True, key="restart_btn"):
            st.session_state.player_pos = 1
            st.session_state.computer_pos = 1
            st.session_state.player_turn = True
            st.session_state.dice_value = 0
            st.session_state.game_log = ["Game Restarted!", "Player goes first"]
            st.session_state.game_over = False
            st.session_state.winner = None
            st.rerun()
    
    # Game Status
    st.divider()
    
    if st.session_state.game_over:
        st.success(f"🎉 **{st.session_state.winner} Wins!** 🎉")
    else:
        turn_msg = "🔵 Player's Turn" if st.session_state.player_turn else "🟠 Computer's Turn"
        st.info(turn_msg)
    
    # Game Log
    st.subheader("📝 Game Log")
    for log in st.session_state.game_log[-5:]:  # Show last 5 moves
        st.write(f"• {log}")

if __name__ == "__main__":
    main()
