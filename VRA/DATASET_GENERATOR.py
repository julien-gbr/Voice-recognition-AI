# Script pour enregistrer des phrases et créer un jeu de données audio

import sounddevice as sd
from scipy.io.wavfile import write
import os
from pynput import keyboard
import numpy as np
from datetime import datetime
import re
import unicodedata
import threading  # Importer threading pour utiliser Event

def File_reformer(value):
    value = str(value)
    value = unicodedata.normalize('NFKD', value).encode('ASCII', 'ignore').decode('ASCII')
    value = re.sub(r'[^\w\s-]', '', value).strip()
    value = re.sub(r'[\s]+', '_', value)
    return value

command_sentences = [
    "lance google",
    "lance spotify",
    "ferme google",
    "éteins l'ordinateur",
    "ouvre le terminal"
]

base_directory = "Recording_files"

fs = 44100

while True:
    try:
        number_of_repetitions = int(input("Entrez le nombre de répétitions pour chaque phrase : "))
        if number_of_repetitions <= 0:
            print("Only positive numbers are allowed.")
            continue
        break
    except ValueError:
        print("Please enter a valid integer.")

def record_sentence():
    print("Press Space to stop the recording.")
    recording = []
    stop_event = threading.Event()

    def callback(indata, frames, time, status):
        recording.append(indata.copy())
        if stop_event.is_set():
            raise sd.CallbackStop()

    def on_press(key):
        if key == keyboard.Key.space:
            stop_event.set()
            return False 

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    with sd.InputStream(samplerate=fs, channels=1, dtype='int16', callback=callback):
        print("Recording... Press Space to stop.")
        while not stop_event.is_set():
            sd.sleep(100)

    listener.join()
    audio_data = np.concatenate(recording, axis=0)
    return audio_data

for idx, phrase in enumerate(command_sentences):
    phrase_dir_name = File_reformer(phrase)
    phrase_directory = os.path.join(base_directory, phrase_dir_name)
    if not os.path.exists(phrase_directory):
        os.makedirs(phrase_directory)

    for rep in range(number_of_repetitions):
        print(f"\nYou need to repeat the sentence: '{phrase}' (Repetition {rep + 1}/{number_of_repetitions})")
        input("Press Enter to start recording.")
        print("Speak now.")

        audio_data = record_sentence()

        print("Recording ended.")

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Build the file name
        filename = f"{phrase_dir_name}_{timestamp}.wav"
        filepath = os.path.join(phrase_directory, filename)

        write(filepath, fs, audio_data)

print("\nFinished.")
