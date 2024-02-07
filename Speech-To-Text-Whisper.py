
import sounddevice as sd
import soundfile as sf
import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import datetime
import queue
import pygame
import whisper
from langdetect import detect
import spacy
import calamancy

# Initialize Pygame mixer for audio playback
pygame.mixer.init()

# Initialize language models
nlp_english = spacy.load("en_core_web_sm")
nlp_tagalog = calamancy.load("tl_calamancy_md-0.1.0")

def generate_unique_filename(base_dir="audio", base_name="recorded_audio"):
    os.makedirs(base_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(base_dir, f"{base_name}_{timestamp}.wav")

def record_audio_ui(duration=5, sample_rate=44100, root=None):
    file_path = generate_unique_filename()

    recording_window = ctk.CTkToplevel(root)
    recording_window.title("Recording")
    recording_window.geometry("300x150")

    recording_label = ctk.CTkLabel(recording_window, text="Preparing to record...")
    recording_label.pack(pady=20)

    def update_countdown(i):
        if i > 0:
            recording_label.configure(text=f"Recording... {i} seconds remaining")
            recording_window.after(1000, lambda: update_countdown(i-1))
        else:
            recording_label.configure(text="Recording finished. Processing...")

    def start_recording():
        recording_label.configure(text="Recording... Speak now.")
        recording_window.after(1000, lambda: update_countdown(duration - 1))
        recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2, dtype='float32')
        sd.wait()
        sf.write(file_path, recording, sample_rate)
        print(f"Audio recorded and saved as '{file_path}'")

    threading.Thread(target=start_recording, daemon=True).start()

    def play_audio():
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
        except Exception as e:
            messagebox.showerror("Playback Error", f"An error occurred during playback: {e}")

    play_button = ctk.CTkButton(recording_window, text="Play", command=play_audio)
    play_button.pack(pady=10)

def setup_initial_ui(root):
    record_button = ctk.CTkButton(root, text="Record", command=lambda: record_audio_ui(5, 44100, root))
    record_button.pack(pady=20)

    select_button = ctk.CTkButton(root, text="Select Audio File", command=lambda: open_audio_file(root))
    select_button.pack(pady=10)

    quit_button = ctk.CTkButton(root, text="Quit", command=root.destroy)
    quit_button.pack(pady=10)

def open_audio_file(root):
    file_path = filedialog.askopenfilename(initialdir="./audio", title="Select Audio File",
                                           filetypes=(("Audio files", "*.wav *.mp3 *.m4a"), ("All files", "*.*")))
    if file_path:
        transcribe_and_prepare_extraction(root, file_path)

def transcribe_and_prepare_extraction(root, file_path):
    transcription_data_queue = queue.Queue()
    threading.Thread(target=transcribe_and_analyze, args=(file_path, transcription_data_queue), daemon=True).start()
    root.after(100, lambda: update_ui_with_transcription(root, transcription_data_queue))

def transcribe_and_analyze(file_path, transcription_data_queue):
    model = whisper.load_model("base")
    result = model.transcribe(file_path)
    transcription = result["text"]
    try:
        lang = detect(transcription)
    except:
        lang = "error"
    detected_lang = "English" if lang == 'en' else "Tagalog" if lang == 'tl' else "Mixed/Unknown"
    transcription_data_queue.put((transcription, detected_lang))

def update_ui_with_transcription(root, transcription_data_queue):
    try:
        transcription, detected_lang = transcription_data_queue.get_nowait()
    except queue.Empty:
        root.after(100, lambda: update_ui_with_transcription(root, transcription_data_queue))
        return
    show_transcription_results(root, transcription, detected_lang)

def show_transcription_results(root, transcription, detected_lang):
    results_window = ctk.CTkToplevel(root)
    results_window.title("Transcription Results")
    results_window.geometry("600x400")

    transcription_label = ctk.CTkLabel(results_window, text=f"Transcription:\n{transcription}\nDetected Language: {detected_lang}")
    transcription_label.pack(pady=20)

    extraction_entry = ctk.CTkEntry(results_window, placeholder_text="Enter words to extract")
    extraction_entry.pack(pady=10)

    extract_button = ctk.CTkButton(results_window, text="Extract", command=lambda: extract_words(transcription, extraction_entry.get(), detected_lang, results_window))
    extract_button.pack(pady=10)

def extract_words(transcription, user_input, detected_lang, window):
    nlp_model = nlp_english if detected_lang == "English" else nlp_tagalog
    doc = nlp_model(transcription)
    words_to_extract = user_input.split()
    extracted_words = [word.text for word in doc if word.text.lower() in [w.lower() for w in words_to_extract]]

    extracted_words_label = ctk.CTkLabel(window, text="Extracted Words: " + ', '.join(extracted_words))
    extracted_words_label.pack(pady=10)

def setup_gui():
    global root
    root = ctk.CTk()
    root.title("Speech-To-Text Application")
    root.geometry("400x200")
    setup_initial_ui(root)
    root.mainloop()

if __name__ == "__main__":
    setup_gui()
