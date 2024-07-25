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
from online import find_my_ip,search_on_google,search_on_wikipedia,youtube,send_email,get_news,weather_forecast


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
    print("started listening ")

def pause_listening():
    global listening
    listening = False
    print("stopped listening")

keyboard.add_hotkey('ctrl+l', start_listening)
keyboard.add_hotkey('ctrl+s', pause_listening)

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.energy_threshold = 5000  # Adjust this value for faster recognition
        r.pause_threshold = 0.5  # Adjust the pause threshold as needed
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
                speak("I am absolutely fine sir. What about you?")

            elif "open command prompt" in query:
                speak("Opening command prompt")
                os.system('start cmd')

            elif "open camera" in query:
                speak("Opening camera Sir")
                os.system('start microsoft.windows.camera:')


            elif "ip address" in query:
                ip_address = find_my_ip()
                speak(f"your ip address is{ip_address}")
                print(f"your ip address is{ip_address}")


            elif"youtube"in query:
                speak("what do you want to play on youtube sir?")
                video = take_command().lower()
                youtube(video)


            elif"open google"in query:
                speak(f"what do you want to search on google{USER}")
                query = take_command().lower()
                search_on_google(query)

            elif"wikipedia" in query:
                speak(f"what do you want to search on wikipedia")
                search = take_command().lower()
                results = search_on_wikipedia(search)
                speak(f"According to wikipedia,{results}")
                speak("I am printing in on terminal")
                print(results)


            elif "send an email" in query:
                speak("On what email address do you want to send sir?. Please enter in the terminal")
                receiver_add = input("Email address:")
                speak("What should be the subject sir?")
                subject = take_command().capitalize()
                speak("What is the message ?")
                message = take_command().capitalize()
                if send_email(receiver_add, subject, message):
                    speak("I have sent the email sir")
                    print("I have sent the email sir")
                else:
                    speak("something went wrong Please check the error log")

            elif "give me news" in query:
                speak(f"I am reading out the latest headline of today,sir")
                speak(get_news())
                speak("I am printing it on screen sir")
                print(*get_news(), sep='\n')

            elif 'weather' in query:
                ip_address = find_my_ip()
                speak("tell me the name of your city")
                city = input("Enter name of your city")
                speak(f"Getting weather report for your city {city}")
                weather, temp, feels_like = weather_forecast(city)
                speak(f"The current temperature is {temp}, but it feels like {feels_like}")
                speak(f"Also, the weather report talks about {weather}")
                speak("For your convenience, I am printing it on the screen sir.")
                print(f"Description: {weather}\nTemperature: {temp}\nFeels like: {feels_like}")

            elif "movie" in query:
                movies_db = imdb.IMDb()
                speak("Please tell me the movie name:")
                text = take_command()
                movies = movies_db.search_movie(text)
                speak("searching for" + text)
                speak("I found these")
                for movie in movies:
                    title = movie["title"]
                    year = movie["year"]
                    speak(f"{title}-{year}")
                    info = movie.getID()
                    movie_info = movies_db.get_movie(info)
                    rating = movie_info["rating"]
                    cast = movie_info["cast"]
                    actor = cast[0:5]
                    plot = movie_info.get('plot outline', 'plot summary not available')
                    speak(f"{title} was released in {year} has imdb ratings of {rating}.It has a cast of {actor}. "
                          f"The plot summary of movie is {plot}")

                    print(f"{title} was released in {year} has imdb ratings of {rating}.\n It has a cast of {actor}. \n"
                          f"The plot summary of movie is {plot}")

            elif "calculate" in query:
                app_id = "TEAWKP-63GLGUYQU9"
                client = wolframalpha.Client(app_id)
                ind = query.lower().split().index("calculate")
                text = query.split()[ind + 1:]
                result = client.query(" ".join(text))
                try:
                    ans = next(result.results).text
                    speak("The answer is " + ans)
                    print("The answer is " + ans)
                except StopIteration:
                    speak("I couldn't find that . Please try again")


            elif 'what is' in query or 'who is' in query or 'which is' in query:
                app_id = "TEAWKP-63GLGUYQU9"
                client = wolframalpha.Client(app_id)
                try:

                    ind = query.lower().index('what is') if 'what is' in query.lower() else \
                        query.lower().index('who is') if 'who is' in query.lower() else \
                            query.lower().index('which is') if 'which is' in query.lower() else None

                    if ind is not None:
                        text = query.split()[ind + 2:]
                        res = client.query(" ".join(text))
                        ans = next(res.results).text
                        speak("The answer is " + ans)
                        print("The answer is " + ans)
                    else:
                        speak("I couldn't find that. Please try again.")
                except StopIteration:
                    speak("I couldn't find that. Please try again.")

            elif 'subscribe' in query:
                speak(
                    "Everyone who are watching this video, Please subscribe for more amazing content from AnuragDwivedi"
                    ". I will show you how to do this")
                speak("Firstly Go to youtube")
                webbrowser.open("https://www.youtube.com/")
                speak("click on the search bar")
                pyautogui.moveTo(795, 120, 1)
                pyautogui.click(x=795, y=120, clicks=1, interval=0, button='left')
                speak("Anurag Dwivedi")
                pyautogui.typewrite("AnuragDwivedi", 0.1)
                time.sleep(1)
                speak("press enter")
                pyautogui.press('enter')
                pyautogui.moveTo(971, 314, 1)
                speak("Here you will see our channel")
                pyautogui.moveTo(1688, 314, 1)
                speak("click here to subscribe our channel")
                pyautogui.click(x=1688, y=314, clicks=1, interval=0, button='left')
                speak("And also Don't forget to press the bell icon")
                pyautogui.moveTo(1750, 314, 1)
                pyautogui.click(x=1750, y=314, clicks=1, interval=0, button='left')
                speak("turn on all notifications")
                pyautogui.click(x=1750, y=320, clicks=1, interval=0, button='left')