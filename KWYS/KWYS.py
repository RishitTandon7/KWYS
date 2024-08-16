import tkinter as tk
from tkinter import ttk
import speech_recognition as sr
from googletrans import *
from gtts import gTTS
import pygame.mixer

class SpeechTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Speech Translator")
        self.root.geometry("500x500")

        # Initialize Speech Recognition
        self.recognizer = sr.Recognizer()

        # Initialize Translator
        self.translator = Translator()

        # Initialize Pygame for audio playback
        pygame.mixer.init()

        # Input Language Selection
        self.input_label = ttk.Label(self.root, text="Select language you are speaking:")
        self.input_label.pack(pady=10)

        self.input_combo = ttk.Combobox(self.root, values=['Hindi', 'English', 'Bengali', 'Tamil', 'Telugu', 'Marathi', 'Spanish', 'German', 'Japanese', 'Korean'])
        self.input_combo.pack()

        # Target Language Selection
        self.target_label = ttk.Label(self.root, text="Select language you want to translate to:")
        self.target_label.pack(pady=10)

        self.target_combo = ttk.Combobox(self.root, values=['Hindi', 'English', 'Bengali', 'Tamil', 'Telugu', 'Marathi', 'Spanish', 'German', 'Japanese', 'Korean'])
        self.target_combo.pack()

        # Buttons
        self.start_button = ttk.Button(self.root, text="Start Listening", command=self.start_listening)
        self.start_button.pack(pady=20)

        self.pause_button = ttk.Button(self.root, text="Pause Listening", command=self.pause_listening, state=tk.DISABLED)
        self.pause_button.pack(pady=5)

        self.restart_button = ttk.Button(self.root, text="Restart", command=self.restart)
        self.restart_button.pack(pady=5)

        # Text Display
        self.text_display = tk.Text(self.root, height=10, width=60)
        self.text_display.pack(pady=20)

        # Play and Pause Buttons for Translation Playback
        self.play_button = ttk.Button(self.root, text="Play Translation", command=self.play_translation, state=tk.DISABLED)
        self.play_button.pack(pady=5)

        self.pause_translation_button = ttk.Button(self.root, text="Pause Translation", command=self.pause_translation, state=tk.DISABLED)
        self.pause_translation_button.pack(pady=5)

    def start_listening(self):
        self.start_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        self.play_button.config(state=tk.DISABLED)
        self.pause_translation_button.config(state=tk.DISABLED)
        self.restart_button.config(state=tk.DISABLED)
        self.text_display.delete(1.0, tk.END)

        # Get selected languages
        input_lang = self.get_language_code(self.input_combo.get())
        target_lang = self.get_language_code(self.target_combo.get())

        with sr.Microphone() as source:
            print("Speak something...")
            audio = self.recognizer.listen(source)

            try:
                text = self.recognizer.recognize_google(audio, language=input_lang)
                print("You said:", text)

                translated_text = self.translator.translate(text, src=input_lang, dest=target_lang).text
                print(f"Translated to {target_lang}: {translated_text}")
                self.text_display.insert(tk.END, f"Translated to {target_lang}: {translated_text}\n")

                self.play_translation_button_state(True)

                # Save translation to file for playback
                translation_file = "translation.mp3"  # Change this to a directory where you have write permissions
                tts = gTTS(text=translated_text, lang=target_lang)
                tts.save(translation_file)
                self.translation_file = translation_file

                # Play translation automatically
                pygame.mixer.music.load(self.translation_file)
                pygame.mixer.music.play()
                # translation_file = ""

            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio.")
                self.text_display.insert(tk.END, "Google Speech Recognition could not understand audio.\n")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                self.text_display.insert(tk.END, f"Could not request results from Google Speech Recognition service; {e}\n")

            self.start_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED)
            self.restart_button.config(state=tk.NORMAL)

    def pause_listening(self):
        self.recognizer.__setattr__("_operation_lock", True)

    def restart(self):
        self.text_display.delete(1.0, tk.END)
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.play_button.config(state=tk.DISABLED)
        self.pause_translation_button.config(state=tk.DISABLED)
        self.restart_button.config(state=tk.DISABLED)

    def play_translation(self):
        pygame.mixer.music.load(self.translation_file)
        pygame.mixer.music.play()

        self.play_translation_button_state(False)

    def pause_translation(self):
        pygame.mixer.music.pause()

        self.play_translation_button_state(True)

    def play_translation_button_state(self, enabled):
        if enabled:
            self.play_button.config(state=tk.NORMAL)
            self.pause_translation_button.config(state=tk.DISABLED)
        else:
            self.play_button.config(state=tk.DISABLED)
            self.pause_translation_button.config(state=tk.NORMAL)

    def get_language_code(self, language):
        if language == 'Hindi':
            return 'hi'
        elif language == 'English':
            return 'en'
        elif language == 'Bengali':
            return 'bn'
        elif language == 'Tamil':
            return 'ta'
        elif language == 'Telugu':
            return 'te'
        elif language == 'Marathi':
            return 'mr'
        elif language == 'Spanish':
            return 'es'
        elif language == 'German':
            return 'de'
        elif language == 'Japanese':
            return 'ja'
        elif language == 'Korean':
            return 'ko'
        else:
            return None

if __name__ == "__main__":
    root = tk.Tk()
    app = SpeechTranslatorApp(root)
    root.mainloop()
