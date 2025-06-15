import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests
import time 
from openai import OpenAI
from gtts import gTTS
import pygame
import os

#pip install pocketsphinx

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "generate your api key from newsapi site"
def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

    # Initialize mixer
    pygame.mixer.init()

    # Load and play the MP3
    pygame.mixer.music.load("temp.mp3")  # Replace with your MP3 file
    pygame.mixer.music.play()

    # Wait while the audio is playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.remove("temp.mp3")

def aiProcess(command):
    client = OpenAI(
    api_key="Put your api key here."
    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role" : "system", "content":"you are a virtual assistant named jarvis skilled in general tasks like alexa and google cloud, give short responses please."},
            {"role": "user", "content": command}
        ]
    )

    return completion.choices[0].message.content

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musiclibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        r = requests.get("put the generated link from newsapi site which news you want jarvis to read")
        if r.status_code == 200:
            #parse the json response 
            data = r.json()

            #extract the articles 
            articles = data.get('articles', [])

            #print the headlines 
            for article in articles:
                speak(article['title'])
    
    else:
        #let openAI handle the request
        output = aiProcess(c)
        speak(output)


              
    

if __name__ == "__main__":
    speak("Initializing jarvis.......")
    while True:
        #listen for the wake word jarvis
        #obtain audio from the microphone 
        r = sr.Recognizer()
     
        try:
            with sr.Microphone() as source:
                print("listening....")
                audio= r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            print("recognizing...")
            if(word.lower()=="jarvis"):
                speak("Yes sir")
                #listen for command 
                with sr.Microphone() as source:
                    print("Jarvis activated ....")
                    audio= r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)
        except Exception as e:
            print("error; {0}".format(e))

