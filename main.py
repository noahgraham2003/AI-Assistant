import os
import time
import pyaudio
import speech_recognition as sr
import playsound
from gtts import gTTS
import openai
import uuid
import pygame

api_key = ""
lang = 'en'


openai.api_key = api_key

guy = ""

# Initialize the pygame mixer for audio playback
pygame.mixer.init()

def split_text_into_chunks(text, chunk_size):
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks

while True:
    def get_adio():
        r = sr.Recognizer()
        with sr.Microphone(device_index=1) as source:
            audio = r.listen(source)
            said = ""

            try:
                said = r.recognize_google(audio)
                print(said)
                global guy
                guy = said

                if "Jarvis" in said:
                    new_string = said.replace("Jarvis", "")
                    new_string = new_string.strip()
                    print(new_string)
                    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": new_string}])
                    text = completion.choices[0].message.content

                    # Split the response into smaller chunks
                    chunk_size = 100  # Adjust the chunk size as needed
                    text_chunks = split_text_into_chunks(text, chunk_size)

                    # Generate and play audio for each chunk
                    for i, chunk in enumerate(text_chunks):
                        speech = gTTS(text=chunk, lang=lang, slow=False, tld="com.au")
                        file_name = f"chunk_{i}.mp3"
                        speech.save(file_name)
                        pygame.mixer.music.load(file_name)
                        pygame.mixer.music.play()

            except Exception as e:
                pass

        return said

    if "stop" in guy:
        break

    get_adio()
