import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np
import time

# Set page layout
st.set_page_config(page_title="Streamlit Scribble", layout="wide")

# -----------------------------------------------------------------------------
# 1. GLOBAL MULTIPLAYER STATE (Shared across all browser sessions)
# -----------------------------------------------------------------------------
@st.cache_resource
def get_global_game_state():
    """Returns a mutable dictionary shared among ALL connected users."""
    return {
        "drawer": None,
        "secret_word": "APPLE",
        "canvas_image": None,
        "chat_history": [],
        "game_over": False,
        "winner": None,
    }

game_state = get_global_game_state()

# -----------------------------------------------------------------------------
# 2. USER SESSION SETUP
# -----------------------------------------------------------------------------
st.title("🎨 Streamlit Draw & Guess")

# Sidebar for User Join and Settings
st.sidebar.header("Player Setup")
username = st.sidebar.text_input("Enter your nickname:", value="Player1")

# Role Selection
role = st.sidebar.radio(
    "Select Role:",
    ("Guesser", "Drawer"),
    index=0 if game_state["drawer"] else 1
)

# Manage Drawer Assignment
if role == "Drawer":
    if game_state["drawer"] is None or game_state["drawer"] == username:
        game_state["drawer"] = username
    else:
        st.sidebar.warning(f"Drawer spot taken by {game_state['drawer']}. You are viewing as Guesser.")
        role = "Guesser"

# Control Button to Reset Game
if st.sidebar.button("Reset Game / Next Word"):
    game_state["secret_word"] = "PENCIL"
    game_state["canvas_image"] = None
    game_state["chat_history"] = []
    game_state["game_over"] = False
    game_state["winner"] = None
    st.rerun()

# -----------------------------------------------------------------------------
# 3. GAME UI LAYOUT
# -----------------------------------------------------------------------------
col_left, col_right = st.columns([2, 1])

with col_left:
    if role == "Drawer":
        st.subheader(f"✏️ You are Drawing! Secret Word: **{game_state['secret_word']}**")
        
        # Drawing Controls
        stroke_width = st.slider("Stroke width: ", 1, 25, 5)
        stroke_color = st.color_picker("Stroke color hex: ", "#000000")
        
        # Interactive Canvas Component
        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",
            stroke_width=stroke_width,
            stroke_color=stroke_color,
            background_color="#FFFFFF",
            update_streamlit=True,
            height=450,
            width=600,
            drawing_mode="freedraw",
            key="drawer_canvas",
        )

        # Broadcast canvas updates to global state
        if canvas_result.image_data is not None:
            game_state["canvas_image"] = canvas_result.image_data

    else:
        st.subheader("🖼️ Watch and Guess!")
        
        # Display the live drawing from global state
        if game_state["canvas_image"] is not None:
            st.image(
                game_state["canvas_image"],
                caption="Live Drawing Canvas",
                width=600
            )
        else:
            st.info("Waiting for the drawer to create a stroke...")
        
        # Auto-refresh mechanism for Guessers (polls server every 1.5 seconds)
        time.sleep(1.5)
        st.rerun()

with col_right:
    st.subheader("💬 Live Chat & Guesses")

    if game_state["game_over"]:
        st.balloons()
        st.success(f"🎉 Game Over! **{game_state['winner']}** guessed the word: **{game_state['secret_word']}**")

    # Display Chat History
    chat_container = st.container(height=300)
    for msg in game_state["chat_history"]:
        chat_container.write(msg)

    # Guess / Chat Input
    guess = st.text_input("Type your guess here:", key="guess_input", disabled=game_state["game_over"])
    
    if st.button("Send Guess") and guess:
        clean_guess = guess.strip().upper()
        
        if clean_guess == game_state["secret_word"]:
            msg = f"🏆 **{username}** guessed the correct word (**{game_state['secret_word']}**)!"
            game_state["chat_history"].append(msg)
            game_state["game_over"] = True
            game_state["winner"] = username
        else:
            msg = f"**{username}**: {guess}"
            game_state["chat_history"].append(msg)
        
        st.rerun()