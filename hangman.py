import tkinter as tk
from tkinter import messagebox
import random
import string

WORDS = ['CodeAlpha','Internship','python', 'hangman', 'programming', 'university', 'computer', 'science']

BG_COLOR = "#22223b"
FG_COLOR = "#d4fd52"
ACCENT_COLOR = "#abd2ff"
CORRECT_COLOR = "#4ed276"
WRONG_COLOR = "#f05353"

class HangmanGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Hangman Game")
        self.master.configure(bg=BG_COLOR)
        self.word = random.choice(WORDS)
        self.guessed = set()
        self.max_attempts = 6
        self.attempts = 0

        self.word_display = tk.StringVar()
        self.update_display()

        tk.Label(master, text="Hangman", font=("Segoe UI", 28, "bold"), bg=BG_COLOR, fg=ACCENT_COLOR).pack(pady=(20, 5))
        tk.Label(master, text="Guess the word:", font=("Segoe UI", 14), bg=BG_COLOR, fg=FG_COLOR).pack()
        tk.Label(master, textvariable=self.word_display, font=('Consolas', 32, "bold"), bg=BG_COLOR, fg=FG_COLOR).pack(pady=10)

        self.letters_frame = tk.Frame(master, bg=BG_COLOR)
        self.letters_frame.pack(pady=10)
        self.letter_buttons = {}
        self.create_letter_buttons()

        self.info = tk.Label(master, text=f"Attempts left: {self.max_attempts - self.attempts}", font=("Segoe UI", 12), bg=BG_COLOR, fg=ACCENT_COLOR)
        self.info.pack(pady=5)

        self.guessed_label = tk.Label(master, text="Guessed letters: ", font=("Segoe UI", 10), bg=BG_COLOR, fg=FG_COLOR)
        self.guessed_label.pack(pady=5)

        self.reset_btn = tk.Button(master, text="Reset Game", command=self.reset_game, font=("Segoe UI", 10, "bold"),
                                   bg=ACCENT_COLOR, fg=BG_COLOR, activebackground=FG_COLOR, activeforeground=BG_COLOR, relief="flat")
        self.reset_btn.pack(pady=15)

    def create_letter_buttons(self):
        for widget in self.letters_frame.winfo_children():
            widget.destroy()
        self.letter_buttons.clear()
        for idx, letter in enumerate(string.ascii_lowercase):
            btn = tk.Button(self.letters_frame, text=letter, width=3, font=("Segoe UI", 12, "bold"),
                            bg=FG_COLOR, fg=BG_COLOR, relief="flat",
                            command=lambda l=letter: self.guess_letter(l))
            btn.grid(row=idx // 9, column=idx % 9, padx=2, pady=2)
            self.letter_buttons[letter] = btn

    def update_display(self):
        display = ' '.join([letter if letter in self.guessed else '_' for letter in self.word])
        self.word_display.set(display)

    def guess_letter(self, letter):
        if letter in self.guessed:
            return
        self.guessed.add(letter)
        btn = self.letter_buttons[letter]
        if letter in self.word:
            btn.config(bg=CORRECT_COLOR, fg=FG_COLOR, state="disabled")
        else:
            btn.config(bg=WRONG_COLOR, fg=FG_COLOR, state="disabled")
            self.attempts += 1
        self.update_display()
        self.info.config(text=f"Attempts left: {self.max_attempts - self.attempts}")
        self.guessed_label.config(text=f"Guessed letters: {', '.join(sorted(self.guessed))}")

        if all(l in self.guessed for l in self.word):
            self.end_game(True)
        elif self.attempts >= self.max_attempts:
            self.end_game(False)

    def end_game(self, won):
        for btn in self.letter_buttons.values():
            btn.config(state="disabled")
        if won:
            self.show_custom_popup("Congratulations!", f"You guessed the word: {self.word}", CORRECT_COLOR)
        else:
            self.show_custom_popup("Game Over!", f"The word was: {self.word}", WRONG_COLOR)

    def show_custom_popup(self, title, message, color):
        popup = tk.Toplevel(self.master)
        popup.title(title)
        popup.configure(bg=BG_COLOR)
        popup.geometry("350x150")
        popup.resizable(False, False)
        popup.grab_set()  # Make the popup modal

        tk.Label(
            popup, text=title, font=("Segoe UI", 18, "bold"),
            bg=BG_COLOR, fg=color
        ).pack(pady=(20, 5))

        tk.Label(
            popup, text=message, font=("Segoe UI", 12),
            bg=BG_COLOR, fg=FG_COLOR
        ).pack(pady=(0, 15))

        tk.Button(
            popup, text="OK", font=("Segoe UI", 10, "bold"),
            bg=ACCENT_COLOR, fg=BG_COLOR, activebackground=FG_COLOR, activeforeground=BG_COLOR,
            relief="flat", width=10,
            command=popup.destroy
        ).pack()

    def reset_game(self):
        self.word = random.choice(WORDS)
        self.guessed = set()
        self.attempts = 0
        self.update_display()
        self.info.config(text=f"Attempts left: {self.max_attempts - self.attempts}")
        self.guessed_label.config(text="Guessed letters: ")
        self.create_letter_buttons()

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    game = HangmanGame(root)
    root.mainloop()