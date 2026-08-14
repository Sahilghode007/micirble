import streamlit as st
from PIL import Image, ImageDraw
import random
import io

class ScribbleGame:
    def __init__(self):
        self.canvas_width = 600
        self.canvas_height = 400
        self.pen_width = 3
        self.current_word = ""
        self.all_words = ['cat', 'house', 'tree', 'car', 'apple', 'banana', 'flower', 'sun', 'moon', 'star']
        self.setup_drawing_backend()

    def setup_drawing_backend(self):
        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        self.draw_img = ImageDraw.Draw(self.image)

    def choose_word(self):
        self.current_word = random.choice(self.all_words)
        return self.current_word

    def programmatic_draw(self, word):
        self.clear_canvas() # Clear before drawing new word
        st.write(f"Programmatically drawing a simple representation of '{word}'...")

        if word == 'cat':
            self.draw_img.line([(100, 200), (200, 100), (300, 200)], fill="black", width=self.pen_width)
            self.draw_img.ellipse([150, 200, 250, 300], fill="gray", outline="black", width=self.pen_width)
        elif word == 'house':
            self.draw_img.rectangle([150, 200, 450, 350], outline="black", width=self.pen_width)
            self.draw_img.polygon([(125, 200), (300, 100), (475, 200)], outline="black", width=self.pen_width)
        elif word == 'tree':
            self.draw_img.rectangle([280, 250, 320, 350], fill="brown", outline="black", width=self.pen_width)
            self.draw_img.ellipse([200, 150, 400, 280], fill="green", outline="black", width=self.pen_width)
        elif word == 'car':
            self.draw_img.rectangle([100, 250, 400, 300], outline="black", width=self.pen_width)
            self.draw_img.polygon([(120, 250), (150, 200), (350, 200), (380, 250)], outline="black", width=self.pen_width)
            self.draw_img.ellipse([150, 290, 200, 340], fill="black")
            self.draw_img.ellipse([300, 290, 350, 340], fill="black")
        elif word == 'star':
            # Drawing a simple star shape
            points = [
                (300, 100), (320, 160), (380, 180), (340, 220), (360, 280),
                (300, 250), (240, 280), (260, 220), (220, 180), (280, 160)
            ]
            self.draw_img.polygon(points, outline="black", fill="yellow", width=self.pen_width)
        else:
            self.draw_img.text((50, 50), f"No specific drawing for '{word}' yet.", fill="black")
            self.draw_img.line([(50, 100), (self.canvas_width-50, self.canvas_height-100)], fill="red", width=self.pen_width)
            self.draw_img.line([(50, self.canvas_height-100), (self.canvas_width-50, 100)], fill="red", width=self.pen_width)

        return self.image

    def clear_canvas(self):
        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        self.draw_img = ImageDraw.Draw(self.image)


st.set_page_config(page_title="Scribble Drawing Game", layout="centered")

st.title("Scribble Drawing Game")
st.write("Generate random words and see their programmatic drawings!")

# Initialize the game in session state if not already present
if 'game' not in st.session_state:
    st.session_state.game = ScribbleGame()

if 'current_word' not in st.session_state:
    st.session_state.current_word = st.session_state.game.choose_word()

# Function to generate a new word and drawing
def generate_new_drawing():
    st.session_state.current_word = st.session_state.game.choose_word()

# Display the current word
st.header(f"Draw this: **{st.session_state.current_word.upper()}**")

# Generate and display the drawing
drawing_image = st.session_state.game.programmatic_draw(st.session_state.current_word)
st.image(drawing_image, caption=f"Programmatic drawing of '{st.session_state.current_word}'", use_column_width=True)

# Buttons for interaction
col1, col2 = st.columns(2)

with col1:
    st.button("Generate New Word", on_click=generate_new_drawing)

with col2:
    buf = io.BytesIO()
    drawing_image.save(buf, format="PNG")
    byte_im = buf.getvalue()
    st.download_button(
        label="Download Drawing",
        data=byte_im,
        file_name=f"drawing_{st.session_state.current_word}.png",
        mime="image/png"
    )
