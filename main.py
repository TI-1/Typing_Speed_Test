import math
import tkinter as tk
from tkinter import *
import random

YELLOW = "#f7f5dd"


class TypingSpeedTest(tk.Tk):

    def __init__(self):
        super().__init__()

        # Initialise class variables
        self.timer = None
        self.wpm = None
        self.accuracy = None
        self.reset = False
        self.count = 60
        self.running = False

        # Create app design
        self.title("Speed Typing Test")
        self.FONT_NAME = "Courier"
        self.config(padx=20, pady=50, bg=YELLOW)
        self.canvas = Canvas(width=500, height=400, highlightthickness=0)
        self.canvas.grid(row=3, column=0, rowspan=3, columnspan=4, sticky='NEWS')
        self.title_label = Label(text="Typing Speed Test", font=(self.FONT_NAME, 50), bg=YELLOW)
        self.title_label.grid(row=2, column=1)
        self.time_label = Label(text="01:00", font=(self.FONT_NAME, 15), bg=YELLOW)
        self.time_label.grid(row=0, column=0)
        self.wpm_label = Label(text="WPM:", font=(self.FONT_NAME, 15), bg=YELLOW)
        self.wpm_label.grid(row=0, column=2)
        self.wpm_value = Label(text="0", font=(self.FONT_NAME, 15), bg=YELLOW)
        self.acc_label = Label(text="Accuracy:", font=(self.FONT_NAME, 15), bg=YELLOW)
        self.acc_label.grid(row=1, column=2)
        self.acc_value = Label(text="0%", font=(self.FONT_NAME, 15), bg=YELLOW)
        self.text_input = Entry()
        self.text_input.grid(row=6, column=0, columnspan=4, rowspan=3, sticky='NEWS', pady=50)
        self.text_input.bind("<KeyPress>", self.run)
        self.sentence_text = self.get_sentence()
        self.canvas_text = self.canvas.create_text(20, 20, width=780, anchor="nw", text=self.sentence_text,
                                                   fill="black",
                                                   font=(self.FONT_NAME, 15, "bold"))
        self.reset_button = Button(text="Reset", command=self.reset_app)

    # Get Random sentence from text file of sentences
    def get_sentence(self):
        f = open('sentences.txt').read()
        sentences = f.split('\n')
        sentence = random.choice(sentences)
        return sentence

    #
    def run(self, event):
        if not self.reset:
            if not self.running:
                if event.keycode not in [16, 17, 18]:
                    self.running = True
                    self.count_down()
            if not self.sentence_text.startswith(self.text_input.get()):
                self.text_input.config(fg="red")
            else:
                self.text_input.config(fg="green")
            if self.text_input.get() == self.sentence_text[:-1] or event.keycode == 13:
                self.time_label.after_cancel(self.timer)
                self.reset = True
                self.results()
                self.running = False

    def count_down(self):
        count_min = math.floor(self.count / 60)
        count_sec = self.count % 60
        if count_sec < 0:
            count_sec = f"0{count_sec}"
        self.time_label.configure(text=f"0{count_min}:{count_sec}")
        if self.count > 0:
            self.timer = self.time_label.after(1000, self.count_down)
            self.count -= 1
        if self.count == 0:
            self.time_label.after_cancel(self.timer)
            self.results()
            self.running = False
            self.reset = True

    def results(self):
        count = 0
        for i, c in enumerate(self.sentence_text):
            try:
                if self.text_input.get()[i] == c:
                    count += 1
            except:
                pass
        accuracy = count / len(self.text_input.get()) * 100
        self.acc_value.config(text=f"{int(accuracy)}%")
        self.acc_value.grid(row=1, column=3)
        wpm = len(self.text_input.get()) * 60 / (5 * 60 - self.count)
        self.wpm_value.config(text=f"{wpm}")
        self.wpm_value.grid(row=0, column=3)
        self.reset_button.grid(row=9, column=0, columnspan=4)

    def reset_app(self):
        self.running = False
        self.reset = True
        self.count = 60
        self.time_label.configure(text="01:00")
        self.acc_value.grid_remove()
        self.wpm_value.grid_remove()
        self.reset_button.grid_remove()
        self.canvas.itemconfig(self.canvas_text, text=self.get_sentence())
        self.wpm_value.config(text=f"0")
        self.text_input.delete(0, tk.END)


app = TypingSpeedTest()
app.mainloop()
