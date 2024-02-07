# Speech-to-Text Application
This speech-to-text application is designed to record audio from the user's microphone, transcribe the recorded audio into text, and allow for the extraction of specific words from the transcription. Built with Python, it leverages various libraries to handle audio recording, playback, transcription, and natural language processing.

Features
Audio Recording: Users can record their voice directly through the application's interface. Each recording is saved with a unique filename, generated based on the current timestamp, ensuring no overwrites of previous recordings.
Playback Functionality: Immediately after recording, users can play back their recording to ensure it captures the intended audio clearly.
Transcription: The application utilizes the Whisper model for accurate speech-to-text transcription. After recording, it automatically transcribes the audio to text.
Language Detection: Utilizing the langdetect library, the application can detect whether the transcribed text is in English or Tagalog, supporting bilingual use cases.
Word Extraction: Post-transcription, users have the option to extract and display specific words from the transcribed text. This feature is particularly useful for analyzing the recorded content more efficiently.
Natural Language Processing: Leveraging Spacy and Calamancy for English and Tagalog respectively, the application provides robust NLP capabilities for the extraction process.

# Dependencies
Python 3.8+

customtkinter

sounddevice

soundfile

Whisper AI

langdetect

Spacy

Calamancy

pygame

Ensure all dependencies are installed using pip:

```bash
pip install customtkinter
pip install sounddevice
pip install soundfile
pip install langdetect
pip install spacy
pip install calamanCy
pip install pygame
```

# Usage
Run the main file which would be named Speech-To-Text-Whisper.py

# Interface
The application provides a simple and intuitive GUI for recording, playback, and transcription. Users can start a new recording, play back the most recent recording, select an existing audio file for transcription, and extract specific words from the transcribed text.

# Future Enhancements
> Support for more languages in transcription and NLP processing.

> Improved error handling and user feedback mechanisms.

> Integration with external APIs for enhanced transcription accuracy.

> Feature to export transcribed text to a file.
