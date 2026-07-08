import json
import nltk
import string
import tkinter as tk
from tkinter import scrolledtext

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from datetime import datetime
import time

# Download NLTK resources (first time only)
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

# -------------------- Preprocess --------------------
def preprocess(text):
    text = text.lower()
    tokens = word_tokenize(text)

    cleaned_words = []

    for word in tokens:
        if word not in stopwords.words("english") and word not in string.punctuation:
            cleaned_words.append(word)

    return cleaned_words


# -------------------- Load FAQs --------------------
with open("faqs.json", "r") as file:
    faqs = json.load(file)

questions = [faq["question"] for faq in faqs]

processed_questions = []

for question in questions:
    processed_questions.append(" ".join(preprocess(question)))

vectorizer = TfidfVectorizer()
faq_vectors = vectorizer.fit_transform(processed_questions)


# -------------------- Get Response --------------------
def get_response(user_question):

    processed_input = " ".join(preprocess(user_question))

    user_vector = vectorizer.transform([processed_input])

    similarity = cosine_similarity(user_vector, faq_vectors)

    best_match = similarity.argmax()

    score = similarity[0][best_match]

    if score < 0.2:
        return (
            "🤖 Sorry! I couldn't find an answer.\n"
            "Please ask another AI-related question."
        )

    return faqs[best_match]["answer"]
# -------------------- Send Button --------------------
def send_message():

    print("button clicked")

    user_message = entry.get()

    if user_message.strip() == "":
        return

    response = get_response(user_message)

    current_time = datetime.now().strftime("%I:%M %p")

    chat_area.insert(
        tk.END,
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    )

    chat_area.insert(
        tk.END,
        f"👤 You ({current_time})\n",
        "user"
    )

    chat_area.insert(
        tk.END,
        f"{user_message}\n\n"
    )

    chat_area.insert(
        tk.END,
        f"🤖 Bot ({current_time})\n",
        "bot"
    )

    chat_area.insert(
        tk.END,
        f"{response}\n\n"
    )

    chat_area.see(tk.END)

    entry.delete(0, tk.END)
# -------------------- GUI --------------------
window = tk.Tk()
window.title("AI FAQ Chatbot")
window.geometry("800x650")
window.configure(bg="#1e1e1e")
window.resizable(False, False)

header = tk.Label(
    window,
    text="🤖 AI FAQ Chatbot\nPowered by NLP & Machine Learning",
    font=("Segoe UI", 16, "bold"),
    bg="#1f1f1f",
    fg="white",
    pady=10
)

header.pack()
chat_area = scrolledtext.ScrolledText(
    window,
    width=90,
    height=18,
    font=("Segoe UI", 11),
    bg="#252526",
    fg="white",
    insertbackground="white",
    wrap=tk.WORD
)

chat_area.tag_config("user", foreground="#4FC3F7")
chat_area.tag_config("bot", foreground="#81C784")
chat_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
chat_area.insert(tk.END,
"🤖 Welcome to AI FAQ Chatbot!\n"
"Ask me anything about Python, AI, NLP, Machine Learning.\n\n")

bottom_frame = tk.Frame(window, bg="#1e1e1e")
bottom_frame.pack(fill="x", pady=10)

entry = tk.Entry(
    bottom_frame,
    width=65,
    font=("Segoe UI", 12),
    bg="#3c3c3c",
    fg="white",
    insertbackground="white",
    relief="flat"
)

entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

send_button = tk.Button(
    bottom_frame,
    text="Send",
    font=("Segoe UI",10,"bold"),
    bg="#0e639c",
    fg="white",
    command=send_message
)

send_button.pack(side=tk.LEFT)
clear_button = tk.Button(
    bottom_frame,
    text="🗑 Clear Chat",
    bg="#dc3545",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    activebackground="#c82333",
    activeforeground="white",
    relief="flat",
    padx=12,
    pady=5,
    command=lambda: chat_area.delete(1.0, tk.END)
)

clear_button.pack(side=tk.LEFT, padx=10)
entry.bind("<Return>", lambda event: send_message())
window.mainloop()