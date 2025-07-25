import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
import pyttsx3
import datetime
import os
import webbrowser
import pyjokes
import threading

# Initialize TTS and recognizer
engine = pyttsx3.init()
recognizer = sr.Recognizer()

# Speak function
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Listen for voice command
def listen_and_execute():
    command_display.insert(tk.END, "\nListening...\n")
    command_display.see(tk.END)

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio).lower()
        command_display.insert(tk.END, f"User: {command}\n")
        command_display.see(tk.END)
        handle_command(command)
    except sr.UnknownValueError:
        speak("Sorry, I did not understand.")
        command_display.insert(tk.END, "Assistant: Could not understand.\n")
    except sr.RequestError:
        speak("Network error.")
        command_display.insert(tk.END, "Assistant: Network error.\n")

# Handle voice commands
def handle_command(command):
    if "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        respond(f"The time is {now}")
    elif "joke" in command:
        respond(pyjokes.get_joke())
    elif "open notepad" in command:
        os.system("notepad")
        respond("Opening Notepad")
    elif "open calculator" in command:
        os.system("calc")
        respond("Opening Calculator")
    elif "google" in command:
        webbrowser.open("https://www.google.com")
        respond("Opening Google")
    elif "youtube" in command:
        webbrowser.open("https://www.youtube.com")
        respond("Opening YouTube")
    elif "note" in command:
        respond("What should I write?")
        take_note()
    elif "exit" in command or "stop" in command:
        respond("Goodbye!")
        root.quit()
    else:
        respond("I didn't understand that.")

# Respond with voice and display
def respond(text):
    speak(text)
    command_display.insert(tk.END, f"Assistant: {text}\n")
    command_display.see(tk.END)

# Note-taking
def take_note():
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
    try:
        note = recognizer.recognize_google(audio)
        with open("note.txt", "a") as f:
            f.write(f"{datetime.datetime.now()}: {note}\n")
        respond("Note saved.")
    except:
        respond("Could not save the note.")

# Run listener in a thread (to keep GUI responsive)
def start_listening():
    threading.Thread(target=listen_and_execute).start()

# ---------------- GUI ----------------
root = tk.Tk()
root.title("🎙️ Voice Assistant")
root.geometry("600x500")
root.resizable(False, False)

title = tk.Label(root, text="Voice Assistant", font=("Arial", 18, "bold"))
title.pack(pady=10)

command_display = scrolledtext.ScrolledText(root, height=20, font=("Arial", 10))
command_display.pack(padx=20, pady=10)

listen_btn = tk.Button(root, text="🎤 Start Listening", font=("Arial", 14), bg="#4CAF50", fg="white", command=start_listening)
listen_btn.pack(pady=10)

exit_btn = tk.Button(root, text="❌ Exit", font=("Arial", 12), command=root.quit)
exit_btn.pack(pady=5)

respond("Hello! I'm your assistant. Click the button and speak.")

root.mainloop()
