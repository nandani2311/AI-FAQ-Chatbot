import json
import nltk
import string
import tkinter as tk

from tkinter import scrolledtext
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
def preprocess(text):
    # Convert text to lowercase
    text = text.lower()

    # Split sentence into words
    tokens = word_tokenize(text)

    # Remove punctuation and stopwords
    cleaned_words = []

    for word in tokens:
        if word not in stopwords.words("english") and word not in string.punctuation:
            cleaned_words.append(word)

    return cleaned_words
# Open the JSON file
with open("faqs.json", "r") as file:
    faqs = json.load(file)
    questions = [faq["question"] for faq in faqs]
    processed_questions = []

for question in questions:
    words = preprocess(question)
    processed_questions.append(" ".join(words))
vectorizer = TfidfVectorizer()

faq_vectors = vectorizer.fit_transform(processed_questions)
def get_response(user_question):
def send_message():

    user_message = entry.get()

    if user_message.strip() == "":
        return

    response = get_response(user_message)

    chat_area.insert(tk.END, "You: " + user_message + "\n")
    chat_area.insert(tk.END, "Bot: " + response + "\n\n")

    entry.delete(0, tk.END)    

    processed_input = " ".join(preprocess(user_question))

    user_vector = vectorizer.transform([processed_input])

    similarity = cosine_similarity(user_vector, faq_vectors)

    best_match = similarity.argmax()

    score = similarity[0][best_match]

    if score < 0.2:
        return "Sorry, I don't know the answer."

    return faqs[best_match]["answer"]    

# Print all FAQs
print("Frequently Asked Questions:\n")

for faq in faqs:
    print("Question:", faq["question"])
    print("Answer:", faq["answer"])
    print("-" * 50)
# Create GUI Window
window = tk.Tk()
window.title("AI FAQ Chatbot")
window.geometry("600x500")

# Chat Area
chat_area = scrolledtext.ScrolledText(window, width=70, height=20)
chat_area.pack(pady=10)

# User Input
entry = tk.Entry(window, width=50)
entry.pack(side=tk.LEFT, padx=10, pady=10)

# Send Button
send_button = tk.Button(window, text="Send", command=send_message)
send_button.pack(side=tk.LEFT)

window.mainloop()