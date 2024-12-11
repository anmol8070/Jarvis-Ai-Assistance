import pyttsx3
import speech_recognition as sr
import keyboard
import os
import subprocess as sp
import imdb
import wolframalpha
import pyautogui
import webbrowser
import time
from datetime import datetime
from decouple import config
from random import choice
from conv import random_text
from online import find_my_ip, search_on_google, search_on_wikipedia, youtube, send_email, get_news, weather_forecast

engine = pyttsx3.init('sapi5')
engine.setProperty('volume', 1.5)
engine.setProperty('rate', 225)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

USER = config('USER')
BOT = config('BOT')

def speak(text):
    engine.say(text)
    engine.runAndWait()

def greet_me():
    hour = datetime.now().hour
    if 6 <= hour < 12:
        speak(f"Good morning {USER}")
    elif 12 <= hour < 16:
        speak(f"Good afternoon {USER}")
    elif 16 <= hour < 19:
        speak(f"Good evening {USER}")
    speak(f"I am {BOT}. How may I assist you, {USER}?")

listening = False

def start_listening():
    global listening
    listening = True
    print("Started listening...")

def pause_listening():
    global listening
    listening = False
    print("Stopped listening.")

keyboard.add_hotkey('ctrl+l', start_listening)
keyboard.add_hotkey('ctrl+s', pause_listening)

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.energy_threshold = 5000  
        r.pause_threshold = 0.5  
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(query)

        if 'stop' in query or 'exit' in query:
            hour = datetime.now().hour
            if 21 <= hour < 6:
                speak("Good night sir, take care!")
            else:
                speak("Have a good day sir!")
            exit()

        elif "take a note" in query:
            speak("What would you like me to note down?")
            note = take_command().capitalize()

            with open('notes.txt', 'a') as file:
                file.write(f"{datetime.now()}: {note}\n")
            
            speak("I've saved your note.")

        else:
            speak(choice(random_text))

    except Exception as e:
        print(e)
        speak("Sorry, I couldn't understand. Can you please repeat that?")
        query = 'none'
    return query

if __name__ == '__main__':
    greet_me()

    while True:
        if listening:
            query = take_command().lower()

            if "how are you" in query:
                speak("I am absolutely fine, sir. What about you?")

            elif "open command prompt" in query:
                speak("Opening command prompt.")
                os.system('start cmd')

            elif "open camera" in query:
                speak("Opening camera, sir.")
                os.system('start microsoft.windows.camera:')

            elif "ip address" in query:
                ip_address = find_my_ip()
                speak(f"Your IP address is {ip_address}")
                print(f"Your IP address is {ip_address}")

            elif "youtube" in query:
                speak("What do you want to play on YouTube, sir?")
                video = take_command().lower()
                youtube(video)

            elif "open google" in query:
                speak(f"What do you want to search on Google, {USER}?")
                query = take_command().lower()
                search_on_google(query)

            elif "wikipedia" in query:
                speak("What do you want to search on Wikipedia?")
                search = take_command().lower()
                results = search_on_wikipedia(search)
                speak(f"According to Wikipedia: {results}")
                print(results)

            elif "send an email" in query:
                speak("On what email address do you want to send, sir? Please enter in the terminal.")
                receiver_add = input("Email address: ")
                speak("What should be the subject, sir?")
                subject = take_command().capitalize()
                speak("What is the message?")
                message = take_command().capitalize()

                if send_email(receiver_add, subject, message):
                    speak("I have sent the email, sir.")
                    print("I have sent the email, sir.")
                else:
                    speak("Something went wrong. Please check the error log.")

            elif "give me news" in query:
                speak("I am reading out the latest headline of today, sir.")
                speak(get_news())
                print(*get_news(), sep='\n')

            elif "weather" in query:
                ip_address = find_my_ip()
                speak("Tell me the name of your city.")
                city = input("Enter the name of your city: ")
                speak(f"Getting a weather report for your city {city}")
                weather, temp, feels_like = weather_forecast(city)
                speak(f"The current temperature is {temp}, but it feels like {feels_like}")
                speak(f"Also, the weather report talks about {weather}")
                print(f"Description: {weather}\nTemperature: {temp}\nFeels like: {feels_like}")

            elif "movie" in query:
                movies_db = imdb.IMDb()
                speak("Please tell me the movie name:")
                text = take_command()
                movies = movies_db.search_movie(text)
                speak("Searching for " + text)
                speak("I found these movies.")
                
                for movie in movies:
                    title = movie["title"]
                    year = movie["year"]
                    speak(f"{title} - {year}")
                    info = movie.getID()
                    movie_info = movies_db.get_movie(info)
                    rating = movie_info["rating"]
                    cast = movie_info.get('cast', [])[:5]
                    plot = movie_info.get('plot outline', 'Plot summary not available.')

                    speak(f"{title} was released in {year}. It has an IMDb rating of {rating}.")
                    speak(f"Cast: {', '.join(cast)}")
                    speak(f"Plot: {plot}")

                    print(f"{title} - {year}\nIMDb Rating: {rating}\nCast: {', '.join(cast)}\nPlot: {plot}")

