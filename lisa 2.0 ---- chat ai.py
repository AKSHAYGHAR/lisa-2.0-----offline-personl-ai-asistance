import tkinter as tk
from tkinter import scrolledtext
import requests
import pyttsx3
import threading
import time

# ---------- Voice Setup ----------
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    if "female" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break
else:
    engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 170)
voice_enabled = True
typing = False

# ---------- Lisa AI with Identity Detection ----------
def chat_with_lisa(prompt):
    prompt_lower = prompt.lower()

    # ✅ Custom identity response
    hindi_qs = ["tum kaun ho", "kisne banaya", "tumhe kisne banaya", "tum kon ho", "kon banaya", "tumhara naam kya hai"]
    english_qs = ["who made you",  "who created you","who is creator","who is  create you","who is made you","who is yor developer","who is  develope  you"]
    english1_qs =['what is your name ','who are you ',]

    for q in hindi_qs:
        if q in prompt_lower:
            return "Mujhe Akshay ne banaya hai. Mera naam Lisa 2.0🤖 hai. Mera pehla version thik nahi tha😿 isliye main 2.0 hoon."
    for q in english_qs:
        if q in prompt_lower:
            return "I was created by Akshay. My name is Lisa 2.0🤖. My first version wasn't good🤒, so I'm 2.0 now."
    for q in english1_qs:
        if q in prompt_lower:
            return "my Name is lisa 2.0🤖 and iam created by Akshay.My first version was not good🤒 so i am 2.0 now😎"
from tkinter import scrolledtext
import requests
import pyttsx3
import threading
import time

# ---------- Voice Setup ----------
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    if "female" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break
else:
    engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 170)
voice_enabled = True
typing = False

# ---------- Lisa AI with Identity Detection ----------
def chat_with_lisa(prompt):
    prompt_lower = prompt.lower()

    #  Custom identity response
    hindi_qs = ["tum kaun ho", "kisne banaya", "tumhe kisne banaya", "tum kon ho", "kon banaya", "tumhara naam kya hai"]
    english_qs = ["who are you", "who made you", "what is your name", "who created you"]

    for q in hindi_qs:
        if q in prompt_lower:
            return "Mujhe Akshay ne banaya hai. Mera naam Lisa 2.0 hai. Mera pehla version thik nahi tha isliye main 2.0 hoon."
    for q in english_qs:
        if q in prompt_lower:
            return "I was created by Akshay. My name is Lisa 2.0. My first version wasn't good, so I'm 2.0 now."


    #  Normal chat
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen:0.5b",
            "prompt": (
                "Tumhara naam Lisa hai. Tum sirf chhoti aur friendly baatein karti ho. "
                "Reply karte waqt sirf Hinglish (Hindi + English mix in English letters) me bolna. "
                "Koi pure Hindi ya English mat bolna, dono ka mix use karo. "
                "Avoid deep or formal answers. Friendly aur short reply do:\nUser: " + prompt
            ),
            "stream": False
        }
    )
    return response.json()["response"]

# ---------- Speak ----------
def speak(text):
    if voice_enabled:
        engine.say(text)
        engine.runAndWait()

# ---------- Typing Animation ----------
def typing_animation(tag):
    dots = ""
    while typing:
        chat_box.delete(tag, f"{tag} + 1 lines")
        chat_box.insert(tag, f"🤖 Lisa: typing{dots}\n", "loading")
        chat_box.see(tk.END)
        window.update()
        dots = "." if dots == "..." else dots + "."
        time.sleep(0.5)

# ---------- Send Message ----------
def send_message(event=None):
    global typing
    msg = user_input.get()
    if msg.strip() == "":
        return

    chat_box.config(state='normal')
    chat_box.insert(tk.END, f"\n🧑 You: {msg}\n", "user")
    chat_box.config(state='disabled')
    chat_box.see(tk.END)
    user_input.delete(0, tk.END)
    window.update()

    # Typing animation
    typing = True
    loading_tag = chat_box.index(tk.END)
    chat_box.config(state='normal')
    chat_box.insert(tk.END, "🤖 Lisa: typing\n", "loading")
    chat_box.config(state='disabled')
    window.update()

    anim_thread = threading.Thread(target=typing_animation, args=(loading_tag,))
    anim_thread.start()

    def get_response():
        global typing
        response = chat_with_lisa(msg)
        typing = False
        anim_thread.join()

        chat_box.config(state='normal')
        chat_box.delete(loading_tag, f"{loading_tag} + 1 lines")
        chat_box.insert(tk.END, f"🤖 Lisa: {response}\n", "lisa")
        chat_box.config(state='disabled')
        chat_box.see(tk.END)
        speak(response)

    threading.Thread(target=get_response).start()

# ---------- Voice Toggle ----------
def toggle_voice():
    global voice_enabled
    voice_enabled = not voice_enabled
    voice_button.config(text="🔊 Voice: ON" if voice_enabled else "🔇 Voice: OFF")

# ---------- GUI Setup ----------
window = tk.Tk()
window.title("Lisa 2.0 - Chat Assistant")
window.geometry("700x800")
window.config(bg="#101020")

title_label = tk.Label(window, text="💬 Lisa 2.0 - Chat with AI", font=("Helvetica", 40, "bold"), fg="white", bg="#101020")
title_label.pack(pady=10)

chat_box = scrolledtext.ScrolledText(window, wrap=tk.WORD, font=("Helvetica", 13), bg="#1b1b2f", fg="#ffffff", bd=0)
chat_box.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
chat_box.config(state='disabled')

# Input area
bottom_frame = tk.Frame(window, bg="#101020")
bottom_frame.pack(fill=tk.X, padx=10, pady=10)

user_input = tk.Entry(bottom_frame, font=("Helvetica", 14), bg="#2d2d44", fg="#ffffff", insertbackground='white')
user_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, ipady=8, padx=(0, 10))
user_input.bind("<Return>", send_message)

send_btn = tk.Button(bottom_frame, text="➤", font=("Arial", 14, "bold"), bg="#4e4ecf", fg="white", command=send_message)
send_btn.pack(side=tk.RIGHT)

# Voice Toggle
voice_button = tk.Button(window, text="🔊 Voice: ON", font=("Arial", 10), bg="#2d2d44", fg="white", command=toggle_voice)
voice_button.pack(pady=(0, 5))

# Chat styles
chat_box.tag_config("user", foreground="#00ffcc")
chat_box.tag_config("lisa", foreground="#ffcc66")
chat_box.tag_config("loading", foreground="#888888")

window.mainloop()
