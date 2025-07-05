import tkinter as tk
import random

words = [
    {"jp": "ねこ", "en": "cat"},
    {"jp": "いぬ", "en": "dog"},
    {"jp": "みず", "en": "water"},
    {"jp": "たべる", "en": "to eat"},
    {"jp": "のむ", "en": "to drink"},
    {"jp": "みる", "en": "to see"},
    {"jp": "きく", "en": "to listen"},
    {"jp": "よむ", "en": "to read"},
    {"jp": "かく", "en": "to write"},
    {"jp": "いく", "en": "to go"},
    {"jp": "くる", "en": "to come"},
    {"jp": "する", "en": "to do"},
    {"jp": "ある", "en": "to exist (non-living)"},
    {"jp": "いる", "en": "to exist (living)"},
    {"jp": "せんせい", "en": "teacher"},
    {"jp": "がくせい", "en": "student"},
    {"jp": "ともだち", "en": "friend"},
    {"jp": "かぞく", "en": "family"},
    {"jp": "おかあさん", "en": "mother"},
    {"jp": "おとうさん", "en": "father"},
    {"jp": "あね", "en": "older sister"},
    {"jp": "あに", "en": "older brother"},
    {"jp": "いもうと", "en": "younger sister"},
    {"jp": "おとうと", "en": "younger brother"},
    {"jp": "がっこう", "en": "school"},
    {"jp": "えき", "en": "station"},
    {"jp": "でんしゃ", "en": "train"},
    {"jp": "くるま", "en": "car"},
    {"jp": "じてんしゃ", "en": "bicycle"},
    {"jp": "バス", "en": "bus"},
    {"jp": "いえ", "en": "house"},
    {"jp": "へや", "en": "room"},
    {"jp": "まど", "en": "window"},
    {"jp": "ドア", "en": "door"},
    {"jp": "つくえ", "en": "desk"},
    {"jp": "いす", "en": "chair"},
    {"jp": "ほん", "en": "book"},
    {"jp": "ざっし", "en": "magazine"},
    {"jp": "しんぶん", "en": "newspaper"},
    {"jp": "てがみ", "en": "letter"},
    {"jp": "でんわ", "en": "telephone"},
    {"jp": "けいたい", "en": "mobile phone"},
    {"jp": "パソコン", "en": "computer"},
    {"jp": "テレビ", "en": "TV"},
    {"jp": "えいが", "en": "movie"},
    {"jp": "おんがく", "en": "music"},
    {"jp": "うた", "en": "song"},
    {"jp": "やさい", "en": "vegetable"},
    {"jp": "くだもの", "en": "fruit"},
    {"jp": "ごはん", "en": "rice/meal"},
    {"jp": "パン", "en": "bread"},
    {"jp": "にく", "en": "meat"},
    {"jp": "さかな", "en": "fish"},
    {"jp": "たまご", "en": "egg"},
    {"jp": "あさ", "en": "morning"},
    {"jp": "ひる", "en": "noon"},
    {"jp": "ばん", "en": "evening"},
    {"jp": "よる", "en": "night"},
    {"jp": "いま", "en": "now"},
    {"jp": "きのう", "en": "yesterday"},
    {"jp": "きょう", "en": "today"},
    {"jp": "あした", "en": "tomorrow"},
    {"jp": "ひと", "en": "person"},
    {"jp": "おんな", "en": "woman"},
    {"jp": "おとこ", "en": "man"},
    {"jp": "こども", "en": "child"},
    {"jp": "なまえ", "en": "name"},
    {"jp": "せいねんがっぴ", "en": "birthdate"},
    {"jp": "とし", "en": "age"},
    {"jp": "くに", "en": "country"},
    {"jp": "にほん", "en": "Japan"},
    {"jp": "えいご", "en": "English"},
    {"jp": "にほんご", "en": "Japanese"},
    {"jp": "ことば", "en": "language"},
    {"jp": "はなす", "en": "to speak"},
    {"jp": "きく", "en": "to ask/hear"},
    {"jp": "こたえる", "en": "to answer"},
    {"jp": "しつもん", "en": "question"},
    {"jp": "べんきょう", "en": "study"},
    {"jp": "テスト", "en": "test"},
    {"jp": "しごと", "en": "job"},
    {"jp": "かいしゃ", "en": "company"},
    {"jp": "いしゃ", "en": "doctor"},
    {"jp": "びょういん", "en": "hospital"},
    {"jp": "くすり", "en": "medicine"},
    {"jp": "びょうき", "en": "illness"},
    {"jp": "じかん", "en": "time"},
    {"jp": "いちじ", "en": "1 o’clock"},
    {"jp": "しゅうまつ", "en": "weekend"},
    {"jp": "ひるやすみ", "en": "lunch break"},
    {"jp": "やすみ", "en": "holiday"},
    {"jp": "ともだち", "en": "friend"},
    {"jp": "でかける", "en": "to go out"},
    {"jp": "かえる", "en": "to return"},
    {"jp": "はいる", "en": "to enter"},
    {"jp": "でる", "en": "to leave"},
    {"jp": "あるく", "en": "to walk"},
    {"jp": "はしる", "en": "to run"},
    {"jp": "とまる", "en": "to stop"},
    {"jp": "はじまる", "en": "to begin"},
    {"jp": "おわる", "en": "to end"},
    {"jp": "あける", "en": "to open"},
    {"jp": "しめる", "en": "to close"},
    {"jp": "つける", "en": "to turn on"},
    {"jp": "けす", "en": "to turn off"},
]


def next_card():
    global current_word
    current_word = random.choice(words)
    word_label.config(text=current_word["jp"])
    meaning_label.config(text="")

def show_meaning():
    meaning_label.config(text=current_word["en"])

root = tk.Tk()
root.title("JLPT N5 Flashcards")
root.configure(bg="#fff3f3")

word_label = tk.Label(root, text="", font=("Helvetica", 36, "bold"), fg="#ff5e5e", bg="#fff3f3")
word_label.pack(pady=30)

meaning_label = tk.Label(root, text="", font=("Arial", 22), fg="#777", bg="#fff3f3")
meaning_label.pack(pady=10)

show_button = tk.Button(root, text="✨ Show Meaning ✨", command=show_meaning, font=("Arial", 14), bg="#ffcccc", activebackground="#ffe6e6")
show_button.pack(pady=5)

next_button = tk.Button(root, text="🔁 Next Word", command=next_card, font=("Arial", 14), bg="#ffd9d9", activebackground="#ffe6e6")
next_button.pack(pady=5)


next_card()
root.mainloop()
