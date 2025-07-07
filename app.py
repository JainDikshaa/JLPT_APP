import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import random
import time
from datetime import datetime
import pygame
from PIL import Image, ImageTk

# Initialize sound engine
pygame.mixer.init()

# ========== Configuration ==========
CONFIG = {
    "DATA_FILES": {
        "vocab": "n5_vocab.json",
        "saved_words": "saved_words.json",
        "progress": "user_progress.json"
    }
}

# ========== Sound Functions ==========
def play_sound(path):
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
    except:
        pass

# ========== Animation Helpers ==========
def fade_in(widget, delay=30, step=0.05):
    alpha = 0.0
    def increment():
        nonlocal alpha
        alpha += step
        try:
            widget.tk.call(widget._w, 'attributes', '-alpha', alpha)
        except:
            pass
        if alpha < 1.0:
            widget.after(delay, increment)
    try:
        widget.tk.call(widget._w, 'attributes', '-alpha', 0.0)
        increment()
    except:
        pass

def add_hover_effect(btn, enter_color, leave_color):
    btn.bind("<Enter>", lambda e: btn.config(bg=enter_color))
    btn.bind("<Leave>", lambda e: btn.config(bg=leave_color))

# ========== Sakura Animation ==========
def create_sakura(canvas):
    sprinkles = []
    for _ in range(30):
        x = random.randint(0, 600)
        y = random.randint(-500, 0)
        size = random.randint(2, 4)
        sprinkle = canvas.create_oval(x, y, x + size, y + size, fill="#ffb6c1", outline="")
        sprinkles.append((sprinkle, random.uniform(0.3, 1.0), size))

    def animate():
        for i, (sprinkle, speed, size) in enumerate(sprinkles):
            canvas.move(sprinkle, 0, speed)
            coords = canvas.coords(sprinkle)
            if coords[1] > 500:
                new_x = random.randint(0, 600)
                new_y = random.randint(-100, 0)
                canvas.coords(sprinkle, new_x, new_y, new_x + size, new_y + size)
        canvas.after(50, animate)

    animate()

# ========== Data Management ==========
def load_data():
    data = {}
    for key, filename in CONFIG["DATA_FILES"].items():
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data[key] = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data[key] = {"chapters": {}, "quizzes": {}} if key == "progress" else [] if key == "saved_words" else {}
    return data["vocab"], data["saved_words"], data["progress"]

def save_data(saved_words, progress):
    with open(CONFIG["DATA_FILES"]["saved_words"], "w", encoding="utf-8") as f:
        json.dump(saved_words, f, ensure_ascii=False, indent=2)
    
    with open(CONFIG["DATA_FILES"]["progress"], "w", encoding="utf-8") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)

vocab_data, saved_words, user_progress = load_data()

# ========== Progress Tracking ==========
def update_progress(chapter, activity, score=None):
    today = datetime.now().strftime("%Y-%m-%d")
    
    if chapter not in user_progress["chapters"]:
        user_progress["chapters"][chapter] = {"last_studied": "", "study_count": 0}
    
    if activity == "study":
        user_progress["chapters"][chapter]["last_studied"] = today
        user_progress["chapters"][chapter]["study_count"] += 1
    elif activity == "quiz" and score is not None:
        if chapter not in user_progress["quizzes"]:
            user_progress["quizzes"][chapter] = []
        user_progress["quizzes"][chapter].append({
            "date": today,
            "score": score,
            "total": len(vocab_data.get(chapter, []))
        })
    
    save_data(saved_words, user_progress)

# ========== Saved Words Manager ==========
def open_saved_words():
    saved_win = tk.Toplevel(root)
    saved_win.title("Your Saved Words")
    saved_win.geometry("600x500")
    saved_win.configure(bg="#fff0f5")
    fade_in(saved_win)

    frame = tk.Frame(saved_win, bg="#fff0f5")
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox = tk.Listbox(
        frame,
        yscrollcommand=scrollbar.set,
        font=("Arial", 12),
        bg="white",
        width=60,
        height=20
    )
    listbox.pack(fill="both", expand=True)
    scrollbar.config(command=listbox.yview)

    for word in saved_words:
        listbox.insert(tk.END, f"{word['japanese']} - {word['english']}")

    def delete_selected():
        selection = listbox.curselection()
        if selection:
            index = selection[0]
            del saved_words[index]
            save_data(saved_words, user_progress)
            listbox.delete(index)
            play_sound("delete.mp3")

    delete_btn = tk.Button(
        saved_win,
        text="🗑️ Delete Selected",
        command=delete_selected,
        bg="#ff4444",
        fg="white",
        font=("Arial", 12)
    )
    delete_btn.pack(pady=10)
    add_hover_effect(delete_btn, "#ff6666", "#ff4444")

# ========== Progress Tracker Window ==========
def open_progress():
    progress_win = tk.Toplevel(root)
    progress_win.title("Your Learning Progress")
    progress_win.geometry("700x600")
    progress_win.configure(bg="#fff0f5")
    fade_in(progress_win)

    notebook = ttk.Notebook(progress_win)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    # Chapter Progress Tab
    chapter_frame = tk.Frame(notebook, bg="#fff0f5")
    notebook.add(chapter_frame, text="Chapter Progress")

    columns = ("chapter", "last_studied", "study_count")
    tree = ttk.Treeview(chapter_frame, columns=columns, show="headings")
    tree.heading("chapter", text="Chapter")
    tree.heading("last_studied", text="Last Studied")
    tree.heading("study_count", text="Study Count")
    
    for chapter, data in user_progress["chapters"].items():
        tree.insert("", tk.END, values=(chapter, data["last_studied"], data["study_count"]))
    
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    # Quiz History Tab
    quiz_frame = tk.Frame(notebook, bg="#fff0f5")
    notebook.add(quiz_frame, text="Quiz History")

    quiz_columns = ("chapter", "date", "score", "total")
    quiz_tree = ttk.Treeview(quiz_frame, columns=quiz_columns, show="headings")
    quiz_tree.heading("chapter", text="Chapter")
    quiz_tree.heading("date", text="Date")
    quiz_tree.heading("score", text="Score")
    quiz_tree.heading("total", text="Total")
    
    for chapter, quizzes in user_progress["quizzes"].items():
        for quiz in quizzes:
            quiz_tree.insert("", tk.END, values=(
                chapter, 
                quiz["date"], 
                f"{quiz['score']}/{quiz['total']}",
                quiz["total"]
            ))
    
    quiz_tree.pack(fill="both", expand=True, padx=10, pady=10)

# ========== Flashcard Functionality ==========
def open_learning():
    learning_window = tk.Toplevel(root)
    learning_window.title("Chapter-wise Learning")
    learning_window.geometry("500x600")
    learning_window.configure(bg="#fff0f5")
    fade_in(learning_window)

    tk.Label(learning_window, text="Select Chapter:", font=("Arial", 14), bg="#fff0f5").pack(pady=10)
    chapter_var = tk.StringVar(value=list(vocab_data.keys())[0] if vocab_data else "")

    chapter_menu = ttk.Combobox(learning_window, textvariable=chapter_var, values=list(vocab_data.keys()))
    chapter_menu.pack(pady=5)

    japanese_label = tk.Label(learning_window, text="", font=("Yu Gothic", 32, "bold"), bg="#fff0f5")
    romaji_label = tk.Label(learning_window, text="", font=("Segoe UI", 12, "italic"), bg="#fff0f5", fg="#999")
    english_label = tk.Label(learning_window, text="", font=("Segoe UI", 14), bg="#fff0f5")

    japanese_label.pack(pady=20)
    romaji_label.pack()
    english_label.pack(pady=5)

    index = [0]

    def show_card():
        chapter = chapter_var.get()
        flashcards = vocab_data.get(chapter, [])
        if flashcards:
            word = flashcards[index[0] % len(flashcards)]
            japanese_label.config(text=word["japanese"])
            romaji_label.config(text=word["romaji"])
            english_label.config(text=word["english"])
            update_progress(chapter, "study")
        else:
            japanese_label.config(text="No words in this chapter")
            romaji_label.config(text="")
            english_label.config(text="")

    def next_card():
        play_sound("click.mp3")
        index[0] += 1
        show_card()

    def prev_card():
        play_sound("click.mp3")
        index[0] -= 1
        show_card()

    def save_word():
        chapter = chapter_var.get()
        flashcards = vocab_data.get(chapter, [])
        if flashcards:
            word = flashcards[index[0] % len(flashcards)]
            if word not in saved_words:
                saved_words.append(word)
                save_data(saved_words, user_progress)
                play_sound("save.mp3")
                messagebox.showinfo("Saved", "Word added to your saved list!")

    def update_chapter(*args):
        index[0] = 0
        show_card()

    chapter_var.trace("w", update_chapter)

    btn_frame = tk.Frame(learning_window, bg="#fff0f5")
    btn_frame.pack(pady=10)

    btn_prev = tk.Button(btn_frame, text="⬅️ Prev", command=prev_card, bg="#6a1b9a", fg="white")
    btn_prev.pack(side=tk.LEFT, padx=5)
    add_hover_effect(btn_prev, "#9c27b0", "#6a1b9a")

    btn_next = tk.Button(btn_frame, text="Next ➡️", command=next_card, bg="#6a1b9a", fg="white")
    btn_next.pack(side=tk.LEFT, padx=5)
    add_hover_effect(btn_next, "#9c27b0", "#6a1b9a")

    btn_save = tk.Button(learning_window, text="⭐ Save Word", command=save_word, bg="#ff9800", fg="white")
    btn_save.pack(pady=6)
    add_hover_effect(btn_save, "#ffa726", "#ff9800")

    btn_view_saved = tk.Button(
        learning_window,
        text="📖 View Saved Words",
        command=open_saved_words,
        bg="#4caf50",
        fg="white"
    )
    btn_view_saved.pack(pady=6)
    add_hover_effect(btn_view_saved, "#66bb6a", "#4caf50")

    show_card()

# ========== Quiz Functionality ==========
class QuizApp:
    def __init__(self, master, chapter):
        self.master = master
        self.chapter = chapter
        self.words = vocab_data.get(chapter, [])
        self.current_question = 0
        self.score = 0
        self.start_time = time.time()
        
        self.setup_ui()
        self.next_question()
    
    def setup_ui(self):
        self.master.title(f"Quiz - {self.chapter}")
        self.master.geometry("500x500")
        self.master.configure(bg="#fff0f5")
        
        self.question_label = tk.Label(
            self.master,
            text="",
            font=("Arial", 16),
            wraplength=400,
            bg="#fff0f5"
        )
        self.question_label.pack(pady=20)
        
        self.answer_var = tk.StringVar()
        self.option_buttons = []
        
        for i in range(4):
            btn = tk.Radiobutton(
                self.master,
                text="",
                variable=self.answer_var,
                value="",
                font=("Arial", 12),
                bg="#fff0f5",
                selectcolor="#ffccd5"
            )
            btn.pack(anchor="w", padx=50, pady=5)
            self.option_buttons.append(btn)
        
        self.feedback_label = tk.Label(
            self.master,
            text="",
            font=("Arial", 12),
            bg="#fff0f5"
        )
        self.feedback_label.pack(pady=5)
        
        self.timer_label = tk.Label(
            self.master,
            text="Time left: 30s",
            font=("Arial", 12),
            bg="#fff0f5"
        )
        self.timer_label.pack()
        
        self.submit_btn = tk.Button(
            self.master,
            text="Submit",
            font=("Arial", 12),
            bg="#4caf50",
            fg="white",
            command=self.check_answer
        )
        self.submit_btn.pack(pady=10)
        add_hover_effect(self.submit_btn, "#66bb6a", "#4caf50")
        
        self.timer_id = None
        self.time_left = 30
    
    def next_question(self):
        if self.current_question >= len(self.words) or self.current_question >= 10:
            self.show_results()
            return
        
        if self.timer_id:
            self.master.after_cancel(self.timer_id)
        
        self.time_left = 30
        self.timer_label.config(text=f"Time left: {self.time_left}s")
        self.start_timer()
        
        question = self.words[self.current_question]
        correct_answer = question["english"]
        
        # Generate options
        options = [correct_answer]
        while len(options) < 4:
            random_word = random.choice(self.words)
            if random_word["english"] not in options:
                options.append(random_word["english"])
        
        random.shuffle(options)
        
        # Update UI
        self.question_label.config(text=f"What does '{question['japanese']}' mean?")
        self.answer_var.set("")
        self.feedback_label.config(text="")
        
        for btn, opt in zip(self.option_buttons, options):
            btn.config(text=opt, value=opt)
    
    def start_timer(self):
        if self.time_left > 0:
            self.timer_label.config(text=f"Time left: {self.time_left}s")
            self.time_left -= 1
            self.timer_id = self.master.after(1000, self.start_timer)
        else:
            self.check_answer()
    
    def check_answer(self):
        if self.timer_id:
            self.master.after_cancel(self.timer_id)
            self.timer_id = None
        
        user_answer = self.answer_var.get()
        correct_answer = self.words[self.current_question]["english"]
        
        if user_answer == correct_answer:
            self.score += 1
            self.feedback_label.config(text="✅ Correct!", fg="green")
        else:
            self.feedback_label.config(text=f"❌ Wrong! Correct: {correct_answer}", fg="red")
        
        self.current_question += 1
        self.master.after(1500, self.next_question)
    
    def show_results(self):
        time_taken = int(time.time() - self.start_time)
        update_progress(self.chapter, "quiz", self.score)
        messagebox.showinfo(
            "Quiz Complete",
            f"Your Score: {self.score}/{min(10, len(self.words))}\n"
            f"Time Taken: {time_taken} seconds"
        )
        self.master.destroy()

def open_quiz():
    quiz_win = tk.Toplevel(root)
    quiz_win.title("Select Quiz Chapter")
    quiz_win.geometry("300x200")
    quiz_win.configure(bg="#fff0f5")
    fade_in(quiz_win)
    
    tk.Label(
        quiz_win,
        text="Select Chapter for Quiz:",
        font=("Arial", 14),
        bg="#fff0f5"
    ).pack(pady=20)
    
    chapter_var = tk.StringVar(value=list(vocab_data.keys())[0] if vocab_data else "")
    
    chapter_menu = ttk.Combobox(quiz_win, textvariable=chapter_var, values=list(vocab_data.keys()))
    chapter_menu.pack(pady=10)
    
    def start_quiz():
        quiz_win.destroy()
        quiz_window = tk.Toplevel(root)
        QuizApp(quiz_window, chapter_var.get())
    
    start_btn = tk.Button(
        quiz_win,
        text="Start Quiz",
        command=start_quiz,
        bg="#c2185b",
        fg="white",
        font=("Arial", 12)
    )
    start_btn.pack(pady=10)
    add_hover_effect(start_btn, "#e91e63", "#c2185b")

# ========== Main Application ==========
root = tk.Tk()
root.title("JLPT N5 Mastery App")
root.geometry("600x500")  # Adjusted height since we removed one button
root.configure(bg="#ffe4ec")
fade_in(root)

canvas = tk.Canvas(root, width=600, height=500, bg="#ffe4ec", highlightthickness=0)
canvas.pack(fill="both", expand=True)

create_sakura(canvas)

welcome_label = tk.Label(
    canvas,
    text="✨ Welcome to JLPT N5 Mastery! ✨",
    font=("Helvetica", 22, "bold"),
    bg="#ffe4ec",
    fg="#8b004f"
)
canvas.create_window(300, 80, window=welcome_label)

button_font = ("Arial", 14)
button_color = "#ffccd5"

buttons = [
    ("📚 Chapter-wise Learning", open_learning),
    ("📝 Chapter-wise Quiz", open_quiz),
    ("⭐ Your Saved Words", open_saved_words),
    ("📈 Learning Progress", open_progress)
    # Removed the Japan News button
]

for i, (text, cmd) in enumerate(buttons):
    btn = tk.Button(
        canvas,
        text=text,
        command=cmd,
        font=button_font,
        bg=button_color,
        fg="#000",
        activebackground="#ffc0cb",
        relief=tk.RAISED,
        padx=10,
        pady=5,
        width=20
    )
    canvas.create_window(300, 150 + i * 70, window=btn)
    add_hover_effect(btn, "#ffb6c1", "#ffccd5")

play_sound("start.mp3")
root.mainloop()