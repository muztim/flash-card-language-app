from tkinter import *
import pandas
import random
from csv import writer

BACKGROUND_COLOR = "#B1DDC6"
# ------------------------------- NEW WORD ------------------------------#
current_word = {}
words_to_learn = {}
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    words_to_learn = original_data.to_dict(orient="records")
else:
    words_to_learn = data.to_dict(orient="records")


def gen_card():
    global current_word, check_answer_timer
    current_word = random.choice(words_to_learn)
    canvas.itemconfig(canvas_image, image=card_front_image)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_word["French"], fill="black")

    check_answer_timer = window.after(3000, func=check_answer)

# ---------------------------- CHECK ANSWER -----------------------------#
def check_answer():
    canvas.itemconfig(canvas_image, image=card_back_image)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_word["English"], fill="white")

# ---------------------------- CHECK ANSWER -----------------------------#
def known_word():
    words_to_learn.remove(current_word)
    new_data = pandas.DataFrame(words_to_learn)
    new_data.to_csv("data/words_to_learn.csv", index=False)

    gen_card()

# ------------------------------- UI SETUP ------------------------------#
window = Tk()
window.title("Flash Card App")
window.config(padx=20, pady=20, bg=BACKGROUND_COLOR)

check_answer_timer = window.after(3000, func=check_answer)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front_image)
canvas.grid(column=0, row=0, columnspan=2)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))


# Buttons
cross_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=cross_image, command=gen_card)
wrong_button.grid(column=1, row=1)

tick_image = PhotoImage(file="images/right.png")
right_button = Button(image=tick_image, command=known_word)
right_button.grid(column=0, row=1)

gen_card()

window.mainloop()