import tkinter as tk
from tkinter import messagebox
import random
import os
import base64
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def load_scores():
    scores = []
    try:
        score_path = resource_path("scores.txt")
        if os.path.exists(score_path):
            with open(score_path, "r") as file:
                lines = file.readlines()
                for line in lines:
                    try:
                        decoded = base64.b64decode(line.strip()).decode("utf-8")
                        parts = decoded.split()
                        if len(parts) == 2 and parts[1].isdigit():
                            scores.append((parts[0], int(parts[1])))
                    except (base64.binascii.Error, ValueError):
                        print(f"Error decoding line: {line}")
        return sorted(scores, key=lambda x: x[1], reverse=True)[:3]
    except FileNotFoundError:
        print("Score file not found.")
        return []
    except IOError as e:
        print(f"Error reading score file: {e}")
        return []

def save_scores(scores):
    try:
        score_path = resource_path("scores.txt")
        with open(score_path, "w") as file:
            for entry in scores:
                encoded_entry = base64.b64encode(f"{entry[0]} {entry[1]}".encode("utf-8")).decode("utf-8")
                file.write(f"{encoded_entry}\n")
    except IOError as e:
        print(f"Error writing score file: {e}")

class GuessTheDoor:
    def __init__(self, root):
        self.root = root
        self.root.title("Guess The Door")
        self.root.configure(bg="black")
        self.root.geometry("400x300")

        self.title_label = tk.Label(root, text="Guess The Door", font=("Arial", 30, "bold"), fg="white", bg="black")
        self.title_label.pack(pady=20)

        self.start_button = tk.Button(root, text="Start Spiel", command=self.start_game, bg="purple", fg="white", width=15, height=2)
        self.start_button.pack(pady=10)

        self.leaderboard_button = tk.Button(root, text="Leaderboard", command=self.show_leaderboard, bg="purple", fg="white", width=15)
        self.leaderboard_button.pack(pady=10)

        self.exit_button = tk.Button(root, text="Beenden", command=root.destroy, bg="purple", fg="white", width=15)
        self.exit_button.pack(pady=10)

    def start_game(self):
        self.root.withdraw()
        self.name_window = tk.Toplevel(self.root)
        self.name_window.title("Spiel Starten")
        self.name_window.configure(bg="black")
        self.name_window.geometry("300x150")

        tk.Label(self.name_window, text="Wie lautet dein Name?", fg="white", bg="black").pack(pady=10)
        self.name_entry = tk.Entry(self.name_window)
        self.name_entry.pack(pady=5)

        tk.Button(self.name_window, text="Starten", command=self.start_game_round, bg="purple", fg="white").pack(pady=10)

    def start_game_round(self):
        name = self.name_entry.get()
        if not name:
            self.show_custom_messagebox("Fehler!", "Gib einen Namen ein!", "red", lambda: None)
            return
        self.name_window.destroy()
        self.name = name
        self.score = 0
        self.play_round()

    def play_round(self):
        self.round_window = tk.Toplevel(self.root)
        self.round_window.title("Wähle eine Tür")
        self.round_window.configure(bg="black")
        self.round_window.geometry("400x250")

        self.correct_door = random.choice(["Links", "Mitte", "Rechts"])
        tk.Label(self.round_window, text=f"Hallo {self.name}, wähle eine Tür:", fg="white", bg="black").pack(pady=10)

        button_frame = tk.Frame(self.round_window, bg="black")
        button_frame.pack()

        self.left_button = tk.Button(button_frame, text="Links", command=lambda: self.check_guess("Links"), bg="purple", fg="white", width=10, height=2)
        self.left_button.pack(side=tk.LEFT, padx=10)

        self.middle_button = tk.Button(button_frame, text="Mitte", command=lambda: self.check_guess("Mitte"), bg="purple", fg="white", width=10, height=2)
        self.middle_button.pack(side=tk.LEFT, padx=10)

        self.right_button = tk.Button(button_frame, text="Rechts", command=lambda: self.check_guess("Rechts"), bg="purple", fg="white", width=10, height=2)
        self.right_button.pack(side=tk.LEFT, padx=10)

    def check_guess(self, guess):
        if guess == self.correct_door:
            self.score += 1
            self.flash_screen()
            self.show_custom_messagebox("Richtig!", f"Richtig! Score: {self.score}", "green", self.continue_game)
        else:
            self.round_window.destroy()
            self.show_custom_messagebox("Falsch!", f"Falsch! Die richtige Tür war {self.correct_door}.", "red", self.show_main_window)
            if self.score > 0:
                scores = load_scores()
                scores.append((self.name, self.score))
                save_scores(scores)

    def continue_game(self):
        self.round_window.destroy()
        self.play_round()

    def show_main_window(self):
        self.root.deiconify()
        self.root.update()

    def flash_screen(self):
        flash_window = tk.Toplevel(self.root)
        flash_window.configure(bg="white")
        flash_window.attributes('-fullscreen', True)
        flash_window.after(200, flash_window.destroy)

    def show_leaderboard(self):
        self.root.withdraw()
        leaderboard_window = tk.Toplevel(self.root)
        leaderboard_window.title("Leaderboard")
        leaderboard_window.configure(bg="black")
        leaderboard_window.geometry("300x200")

        scores = load_scores()
        if not scores:
            tk.Label(leaderboard_window, text="Keine Ergebnisse verfügbar.", fg="white", bg="black").pack(pady=10)
            return

        tk.Label(leaderboard_window, text="Leaderboard", font=("Arial", 14), fg="white", bg="black").pack(pady=5)
        for i, entry in enumerate(scores):
            tk.Label(leaderboard_window, text=f"{i + 1}. {entry[0]} - {entry[1]}", fg="white", bg="black").pack()
        tk.Button(leaderboard_window, text="Zurück", command=lambda: self.return_main(leaderboard_window)).pack()

    def return_main(self, leaderboard_window):
        leaderboard_window.destroy()
        self.root.deiconify()
        self.root.update()

    def show_custom_messagebox(self, title, message, color, callback):
        message_window = tk.Toplevel(self.root)
        message_window.title(title)
        message_window.configure(bg="black")
        message_window.geometry("250x100")

        tk.Label(message_window, text=message, fg="white", bg="black").pack(pady=10)
        ok_button = tk.Button(message_window, text="OK", command=lambda: self.close_messagebox(message_window, callback), bg=color, fg="white")
        ok_button.pack(pady=5)

    def close_messagebox(self, message_window, callback):
        message_window.destroy()
        if callback:
            callback()

if __name__ == "__main__":
    root = tk.Tk()
    app = GuessTheDoor(root)
    root.mainloop()