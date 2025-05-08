import customtkinter as ctk
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
import threading
from googletrans import Translator
import time

# ==== CONFIG ====
API_KEY = "ENTER API KEY"  # <-- Replace this with your actual API key
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat()

recognizer = sr.Recognizer()
mic = sr.Microphone()
translator = Translator()

languages = {
    "English": "en",
    "Tamil": "ta",
    "Malayalam": "ml",
    "Telugu": "te",
    "Hindi": "hi",
    "Arabic": "ar",
    "French": "fr"
}

# Voice engine
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 150)
tts_engine.setProperty('volume', 1.0)

stop_speaking = False
stop_typing = False

# ==== APP SETUP ====
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("🎙 AI Personal Voice Assistant")
app.geometry("800x900")  # Set window size

# ==== FUNCTIONS (UI ONLY) ====
def toggle_theme():
    if theme_switch.get() == "on":
        ctk.set_appearance_mode("light")
    else:
        ctk.set_appearance_mode("dark")

def speak_text(text):
    global stop_speaking
    stop_speaking = False
    try:
        if not stop_speaking:
            tts_engine.say(text)
            tts_engine.runAndWait()
    except Exception as e:
        add_bubble(f"Voice error: {str(e)}", "System")

def stop_all():
    global stop_speaking, stop_typing
    stop_speaking = True
    stop_typing = True
    add_bubble("🛑 Stopped!", "System")
    threading.Thread(target=speak_text, args=("Stopped!",)).start()

def add_bubble(message, who="You"):
    color = {
        "You": "#3a3b3c" if ctk.get_appearance_mode() == "Dark" else "#e0e0e0",
        "AI": "#1f538d" if ctk.get_appearance_mode() == "Dark" else "#cde3ff",
        "System": "red"
    }.get(who, "#3a3b3c")

    wrapper = ctk.CTkFrame(chat_frame, fg_color="transparent")
    wrapper.pack(fill="x", pady=5)

    bubble = ctk.CTkFrame(wrapper, corner_radius=15, fg_color=color)
    bubble.pack(pady=5, padx=20)

    label = ctk.CTkLabel(bubble, text=f"{who}: {message}", font=("Arial", 14), wraplength=500, justify="center")
    label.pack(padx=10, pady=5)

    chat_canvas.update_idletasks()
    chat_canvas.yview_moveto(1)

def listen_and_reply():
    listen_button.configure(text="🎙 Listening...", fg_color="#007FFF")
    app.update()
    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        user_input = recognizer.recognize_google(audio, language=languages[input_language.get()])
        add_bubble(user_input, "You")

        translated_input = translator.translate(user_input, src=languages[input_language.get()], dest="en").text
        response = chat.send_message(translated_input)
        reply = response.text
        translated_reply = translator.translate(reply, src="en", dest=languages[output_language.get()]).text

        threading.Thread(target=type_text, args=(translated_reply,)).start()
        threading.Thread(target=speak_text, args=(translated_reply,)).start()

    except sr.UnknownValueError:
        error_message = "Couldn't understand!"
        add_bubble(error_message, "System")
        threading.Thread(target=speak_text, args=(error_message,)).start()

    except sr.RequestError as e:
        error_message = f"Error: {e}"
        add_bubble(error_message, "System")
        threading.Thread(target=speak_text, args=(error_message,)).start()

    finally:
        listen_button.configure(text="🎤 Speak", fg_color="#1f538d")

def send_text():
    user_input = text_entry.get().strip()
    if user_input == "":
        return
    text_entry.delete(0, ctk.END)
    add_bubble(user_input, "You")

    translated_input = translator.translate(user_input, src=languages[input_language.get()], dest="en").text
    try:
        response = chat.send_message(translated_input)
        reply = response.text
        translated_reply = translator.translate(reply, src="en", dest=languages[output_language.get()]).text

        threading.Thread(target=type_text, args=(translated_reply,)).start()
        threading.Thread(target=speak_text, args=(translated_reply,)).start()

    except Exception as e:
        error_message = f"Error: {str(e)}"
        add_bubble(error_message, "System")
        threading.Thread(target=speak_text, args=(error_message,)).start()

def type_text(text):
    global stop_typing
    stop_typing = False

    wrapper = ctk.CTkFrame(chat_frame, fg_color="transparent")
    wrapper.pack(fill="x", pady=5)

    bubble = ctk.CTkFrame(wrapper, corner_radius=15, fg_color="#1f538d" if ctk.get_appearance_mode() == "Dark" else "#cde3ff")
    bubble.pack(pady=5, padx=20)

    label = ctk.CTkLabel(bubble, text="", font=("Arial", 14), wraplength=500, justify="center")
    label.pack(padx=10, pady=5)

    display = ""

    for char in text:
        if stop_typing:
            break
        display += char
        label.configure(text=display + " |")
        chat_canvas.update_idletasks()
        chat_canvas.yview_moveto(1)
        time.sleep(0.03)

    label.configure(text=display)

# ==== UI ELEMENTS ====

# === Top Bar ===
top_frame = ctk.CTkFrame(app)
top_frame.pack(pady=10, fill="x")

input_language = ctk.CTkOptionMenu(top_frame, values=["English", "Tamil", "Malayalam", "Telugu", "Hindi", "Arabic", "French"])
input_language.set("English")
input_language.grid(row=0, column=0, padx=10)

output_language = ctk.CTkOptionMenu(top_frame, values=["English", "Tamil", "Malayalam", "Telugu", "Hindi", "Arabic", "French"])
output_language.set("English")
output_language.grid(row=0, column=1, padx=10)

theme_switch = ctk.CTkSwitch(top_frame, text="Theme", command=toggle_theme)
theme_switch.grid(row=0, column=2, padx=10)

# === Welcome ===
welcome_label = ctk.CTkLabel(app, text="👋 Hi", font=("Arial Black", 24))
welcome_label.pack(pady=20)

# === Chat Frame ===
chat_frame_container = ctk.CTkFrame(app)
chat_frame_container.pack(pady=10, fill="both", expand=True)

chat_canvas = ctk.CTkCanvas(chat_frame_container, bg="#2b2b2b", highlightthickness=0)
chat_canvas.pack(side="top", fill="both", expand=True)

chat_scrollbar = ctk.CTkScrollbar(chat_frame_container, command=chat_canvas.yview)
chat_scrollbar.pack(side="right", fill="y")

chat_canvas.configure(yscrollcommand=chat_scrollbar.set)

chat_frame = ctk.CTkFrame(chat_canvas)
chat_canvas.create_window((0, 0), window=chat_frame, anchor="n")  # Centered top

def on_frame_config(event):
    chat_canvas.configure(scrollregion=chat_canvas.bbox("all"))

chat_frame.bind("<Configure>", on_frame_config)

# === Bottom Input Bar (Centered) ===
bottom_frame = ctk.CTkFrame(app, corner_radius=15)
bottom_frame.pack(pady=10, fill="x", padx=20)

# Center the widgets in the bottom frame using grid
bottom_frame.grid_rowconfigure(0, weight=1)
bottom_frame.grid_columnconfigure(0, weight=1)

# Place the text entry and buttons in a grid inside the bottom frame
text_entry = ctk.CTkEntry(bottom_frame, placeholder_text="Type here...", width=400, height=40, corner_radius=20)
text_entry.grid(row=0, column=0, padx=5)

listen_button = ctk.CTkButton(bottom_frame, text="🎤", width=40, height=40, corner_radius=20, font=("Arial", 20), command=lambda: threading.Thread(target=listen_and_reply).start())
listen_button.grid(row=0, column=1, padx=5)

send_button = ctk.CTkButton(bottom_frame, text="➤", width=40, height=40, corner_radius=20, font=("Arial", 20), command=lambda: threading.Thread(target=send_text).start())
send_button.grid(row=0, column=2, padx=5)

stop_button = ctk.CTkButton(bottom_frame, text="⏹", width=40, height=40, fg_color="red", corner_radius=20, font=("Arial", 20), command=stop_all)
stop_button.grid(row=0, column=3, padx=5)

# === Start App ===
app.mainloop()