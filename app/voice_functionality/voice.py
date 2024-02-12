import tkinter as tk
import speech_recognition as sr
import pyttsx3
import pyaudio
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def talk(something):
    engine.say(something)
    engine.runAndWait()

def on_button_click():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            chat_box.insert(tk.END, f"User: {text}\n")

            # Speak the transcribed text
            talk(text)
        except sr.UnknownValueError:
            chat_box.insert(tk.END, "User: (Unable to recognize speech)\n")

app = tk.Tk()
app.title("Voice Chatbot")

chat_box = tk.Text(app, wrap=tk.WORD)
chat_box.pack()

mic_button = tk.Button(app, text="Click to Speak", command=on_button_click)
mic_button.pack()

app.mainloop()

'''
talk function can also be used :
lets say , I have done a swap , def talk can be used to say that 
the swapping successfully from {token1} to {token2} '''