import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import subprocess
import platform
import sys
import os
import random

# Initialize the voice engine
voice_engine = pyttsx3.init()
voice_engine.setProperty('rate', 155)  # Adjust speaking speed slightly

# Initialize speech recognizer
speech_recognizer = sr.Recognizer()

def talk(message):
    """Speak the message aloud and print it on console."""
    print(f"Assistant says: {message}")
    voice_engine.say(message)
    voice_engine.runAndWait()

def listen_for_command():
    """Capture user's voice and convert it to text."""
    with sr.Microphone() as mic:
        print("Listening for your command...")
        speech_recognizer.adjust_for_ambient_noise(mic, duration=1)
        audio_input = speech_recognizer.listen(mic)
    try:
        user_command = speech_recognizer.recognize_google(audio_input)
        print(f"You said: {user_command}")
        return user_command.lower()
    except sr.UnknownValueError:
        talk("Hmm, I couldn't understand that. Could you repeat?")
        return ""
    except sr.RequestError:
        talk("My voice recognition service seems unavailable right now.")
        return ""

def give_current_time():
    """Announce current local time."""
    now = datetime.datetime.now()
    time_readable = now.strftime("%I:%M %p")
    talk(f"The current local time is {time_readable}")

def give_current_date():
    """Announce today's date."""
    now = datetime.datetime.now()
    date_readable = now.strftime("%A, %B %d, %Y")
    talk(f"Today is {date_readable}")

def tell_random_joke():
    """Select a joke randomly and speak it."""
    humor_collection = [
        "Why did the computer go to the doctor? Because it caught a virus!",
        "I would tell you a chemistry joke, but I know I wouldn't get a reaction.",
        "Why was the math book sad? Too many problems.",
        "Parallel lines have so much in common. It's a shame they'll never meet.",
        "I told my computer I needed a break, now it won't stop sending me KitKat ads.",
        "Why did the skeleton stay home? He felt bone-tired.",
        "Did you hear about the claustrophobic astronaut? He needed a little space."
    ]
    selected_joke = random.choice(humor_collection)
    talk(selected_joke)

def open_code_editor():
    """Open Visual Studio Code depending on OS."""
    try:
        os_name = platform.system()
        if os_name == "Windows":
            subprocess.Popen(["code"])
        elif os_name == "Darwin":
            subprocess.Popen(["open", "-a", "Visual Studio Code"])
        else:  # Linux
            subprocess.Popen(["code"])
        talk("Launching Visual Studio Code.")
    except Exception as e:
        talk("I couldn't open Visual Studio Code.")
        print(e)

def open_web_browser(site_url, site_name="website"):
    """Open any website in default browser."""
    try:
        webbrowser.open(site_url)
        talk(f"Opening {site_name} for you.")
    except Exception as e:
        talk(f"Oops! I couldn't open {site_name}.")
        print(e)

def open_file_explorer():
    """Open the system file manager."""
    try:
        system_type = platform.system()
        if system_type == "Windows":
            subprocess.Popen("explorer")
        elif system_type == "Darwin":
            subprocess.Popen(["open", "."])
        else:  # Linux
            try:
                subprocess.Popen(["nautilus", "."])
            except FileNotFoundError:
                try:
                    subprocess.Popen(["dolphin", "."])
                except FileNotFoundError:
                    subprocess.Popen(["xdg-open", "."])
        talk("Opening your file manager.")
    except Exception as e:
        talk("I couldn't open the file manager.")
        print(e)

def handle_command(user_input):
    """Interpret the user's command and perform the action."""
    if not user_input:
        return

    if "time" in user_input:
        give_current_time()
    elif "date" in user_input or "day" in user_input:
        give_current_date()
    elif "joke" in user_input:
        tell_random_joke()
    elif "open" in user_input or "launch" in user_input:
        if "vscode" in user_input or "code" in user_input:
            open_code_editor()
        elif "chrome" in user_input or "browser" in user_input:
            open_web_browser("https://www.google.com", "Chrome")
        elif "youtube" in user_input:
            open_web_browser("https://www.youtube.com", "YouTube")
        elif "file" in user_input or "explorer" in user_input or "manager" in user_input:
            open_file_explorer()
        else:
            talk("Sorry, I don't know how to open that.")
    elif "hello" in user_input or "hi" in user_input or "hey" in user_input:
        talk("Hi there! How can I assist you today?")
    elif "help" in user_input or "what can you do" in user_input:
        talk("I can tell time, date, tell jokes, and open apps like Visual Studio Code, Chrome, YouTube, and your file manager.")
    elif "exit" in user_input or "quit" in user_input or "stop" in user_input:
        talk("Goodbye! Have a great day.")
        sys.exit(0)
    else:
        talk("I'm not sure what you mean. Try again or say 'help' to know what I can do.")

def run_assistant():
    """Start the voice assistant."""
    talk("Hello! I am your personal voice assistant. What can I do for you today?")
    while True:
        command_text = listen_for_command()
        handle_command(command_text)

if __name__ == "__main__":
    run_assistant()
