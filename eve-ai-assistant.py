import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import random
import requests
import time
import threading
import pywhatkit
import pyautogui
import difflib

contacts = {
    "shoaib": "+919818068786",
    "omaim": "+919310687931",
    "mom": "+919810978680"
}

notes = []
todos = []
listening = True
music_playing = False

# Speak function
engine = pyttsx3.init()
def speak(text):
    print("Eve:", text)
    engine.say(text)
    engine.runAndWait()

# Listen function
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print("You:", command)
            return command.lower()
        except:
            speak("Sorry, I didn’t catch that.")
            return ""

# Wake word listener
def listen_for_wake_word():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Waiting for wake word 'Eve'...")
        while True:
            audio = recognizer.listen(source)
            try:
                command = recognizer.recognize_google(audio).lower()
                print("You:", command)
                if "eve" in command:
                    speak("Listening Shoaib")
                    global listening
                    listening = True
                    break
            except:
                pass


def send_whatsapp_message():
    speak("To whom do you want to send the message?")
    name_input = listen().lower().strip()

    # Find closest name match
    closest_match = difflib.get_close_matches(name_input, contacts.keys(), n=1, cutoff=0.6)

    if closest_match:
        name = closest_match[0]
        number = contacts[name]
        speak(f"Okay, sending to {name}. What is the message?")
        message = listen().strip()
        speak(f"You said: {message}. Should I send it?")
        confirm = listen().lower()

        if "yes" in confirm or "send" in confirm:
            speak("Sending your message...")
            pywhatkit.sendwhatmsg_instantly(number, message)
            time.sleep(5)  # Wait for WhatsApp web to open and type message
            pyautogui.press("enter")  # Press Enter to send
            speak(f"Message sent to {name}.")
        else:
            speak("Message not sent.")
    else:
        speak("Sorry, I couldn't find anyone with that name.")
   
# Notes Functions
def take_note():
    speak("What should I note down?")
    note = listen()
    if note:
        notes.append(note)
        speak("Note added.")

def read_notes():
    if notes:
        speak("Here are your notes:")
        for i, note in enumerate(notes, 1):
            speak(f"{i}. {note}")
    else:
        speak("You have no notes.")

# To-Do Functions
def add_todo(task):
    todos.append(task)
    speak(f"Added to your to-do list: {task}")

def remove_todo(task):
    if task in todos:
        todos.remove(task)
        speak(f"Removed {task} from your to-do list.")
    else:
        speak(f"{task} not found in your to-do list.")

def show_todos():
    if todos:
        speak("Your to-do list:")
        for i, task in enumerate(todos, 1):
            speak(f"{i}. {task}")
    else:
        speak("Your to-do list is empty.")

# Reminder
def set_reminder(seconds, reminder_text):
    def reminder_thread():
        global music_playing
        music_playing = True  # Pause listening
        time.sleep(seconds)
        speak(f"Reminder: {reminder_text}")
        music_playing = False  # Resume listening after reminder
    threading.Thread(target=reminder_thread).start()
    speak(f"Reminder set for {seconds} seconds from now.")


# Replies
def give_personality_reply():
    replies = [
        "I'm always here for you, Shoaib!",
        "You’re the boss!",
        "I am good",
        "I am just warming up myself",
        "Working smarter... not harder.",
        "I was born to serve you 😎",
        "Sometimes I feel like Jarvis... with you."
    ]
    speak(random.choice(replies))

# Time & Date
def tell_time():
    time_now = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {time_now}")

def tell_date():
    date_now = datetime.datetime.now().strftime("%A, %d %B %Y")
    speak(f"Today is {date_now}")

# Wikipedia
def search_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        speak(result)
    except:
        speak("Sorry, I couldn’t find anything on Wikipedia.")

# Google
def google_search(query):
    speak(f"Searching Google for {query}")
    webbrowser.open(f"https://www.google.com/search?q={query}")

# Open Apps
def open_app(name):
    if 'chrome' in name:
        path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        os.startfile(path)
        speak("Opening Chrome")
        global music_playing
        music_playing = True  # pause listening like with YouTube

    elif 'code' in name or 'vs code' in name:
        path = "C:\\Users\\YourUsername\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        try:
            os.startfile(path)
            speak("Opening VS Code")
        except:
            speak("VS Code path seems incorrect. Please update it.")
    else:
        speak("Sorry, I don't know how to open that yet.")

# Weather
def get_weather(city):
    api_key = "28ab29b27a550baae7bbb09ab12e81fa"
    city = city.strip().lower()
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    if response.get("cod") == 200:
        temp = response["main"]["temp"]
        condition = response["weather"][0]["description"]
        speak(f"The weather in {city} is {condition} with a temperature of {temp} degrees Celsius.")
    else:
        speak("Sorry, I couldn't find the weather for that city.")

# MAIN LOOP
if __name__ == "__main__":
    speak("Eve Activated. Ready for commands.")

    while True:
        if music_playing:
            # Only listen for the wake word
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                print("Waiting for wake word...")
                try:
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio).lower()
                    print("You:", command)
                    if "hey" in command or "eve" in command:  # Or change to your new wake word
                        music_playing = False
                        speak("Listening Shoaib")
                        command = listen()
                except:
                    continue
        else:
            command = listen()

            if 'play' in command:
                song = command.replace('play', '').strip()
                if song:
                    speak(f"Playing {song} on YouTube")
                    webbrowser.open(f"https://www.youtube.com/results?search_query={song.replace(' ', '+')}")
                    music_playing = True
                else:
                    speak("Please tell me the name of the song to play.")

            elif 'hello' in command:
                speak("Hello Shoaib, what can I do for you?")

            elif 'how are you' in command or 'how r you' in command or 'how r u' in command:
                give_personality_reply()

            elif 'weather in' in command:
                city = command.replace('weather in', '').strip()
                get_weather(city)

            elif 'take a note' in command:
                take_note()

            elif 'read my notes' in command:
                read_notes()

            elif 'add to do' in command:
                task = command.replace('add to do', '').strip()
                if task:
                    add_todo(task)
                else:
                    speak("Please tell me what task to add.")

            elif 'remove to do' in command:
                task = command.replace('remove to do', '').strip()
                if task:
                    remove_todo(task)
                else:
                    speak("Please tell me which task to remove.")

            elif 'show my to dos' in command or "show my to do" in command:
                show_todos()

            elif 'remind me in' in command:
                try:
                    parts = command.split('remind me in')[1].strip().split(' ', 2)
                    amount = int(parts[0])
                    unit = parts[1]
                    reminder_text = parts[2] if len(parts) > 2 else "No reminder text provided"
                    seconds = 0
                    if 'minute' in unit:
                        seconds = amount * 60
                    elif 'second' in unit:
                        seconds = amount
                    elif 'hour' in unit:
                        seconds = amount * 3600
                    else:
                        speak("Sorry, I only understand seconds, minutes, or hours for reminders.")
                        seconds = 0
                    if seconds > 0:
                        set_reminder(seconds, reminder_text)
                except Exception:
                    speak("Sorry, I didn't understand the reminder command.")

            elif 'time' in command:
                tell_time()

            elif 'date' in command:
                tell_date()

            elif 'search wikipedia' in command:
                query = command.replace('search wikipedia', '').strip()
                search_wikipedia(query)

            elif 'search google' in command:
                query = command.replace('search google', '').strip()
                google_search(query)
                music_playing = True  # reuse flag to stop listening until wake word

            elif 'send a whatsapp' in command:
                send_whatsapp_message()

            elif 'open' in command:
                open_app(command)

            elif 'stop' in command or 'exit' in command:
                speak("Shutting down. Goodbye Shoaib!")
                break
