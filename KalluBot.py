import speech_recognition as sr
# subprocess --> creating a new process which is different from the process
import subprocess
import webbrowser
import pyautogui
import pyttsx3
import time
from datetime import datetime
import platform
import os
from playwright.sync_api import sync_playwright
dictionary_of_commands = {'hello':'greet you','who are you':'introduction of chatbot','thank':'say you welcome',
                          'thank u':'say you welcome same as thank','open calculator':'open calculator for you',
                          'search for':'search engine like chatgpt','current time':'say you the current time',
                          'shutdown':'end your chatbot'}
recognizer = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
current_hour = datetime.now().hour
def speak(text):
    engine.setProperty('voice', voices[0].id)
    engine.say(text)
    engine.runAndWait()
list_ = []
def recognize_speech():
    with sr.Microphone() as source:
        print("Listening for command...")

        # speak('Good Morning Sir')
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            # speak('Sorry sir reapeat it again please')
            return ""
        except sr.RequestError:
            print("Could not request results; check your network connection.")
            return ""
def open_jupyter_notebook():
    speak("Opening Jupyter Notebook")

    # Specify the path to the folder
    folder_path = "D:\\Office work\\day02 working"

    # Change the current working directory
    os.chdir(folder_path)

    try:
        # Identify the operating system
        os_type = platform.system()

        if os_type == "Windows":
            # Open a command prompt at the specified directory and run jupyter notebook
            # start --> start something
            # cmd /k --> open a new command
            # jupyter notebook --> open jupyter notebook  
            subprocess.Popen("start cmd /k jupyter notebook", shell=True)

    except Exception as e:
        speak(f"An error occurred while opening Jupyter Notebook: {e}")
def open_workspace():
    speak("Opening your workspace")
    
    os_type = platform.system()
    url = "http://192.168.1.58:6789/"
    url2 = "https://chatgpt.com/"
    url3 = "https://www.youtube.com/"
    url4 = "https://in.tradingview.com/"
    browser_user = "brave"
    slack = "C:/Users/abdul/OneDrive/Desktop/Slack.lnk"
    try:
        if os_type == "Windows":
            # Open Brave,Slack using their executable paths on Windows
            subprocess.Popen(["start", browser_user,url,url2,url3,url4], shell=True)
            subprocess.Popen(["start",slack],shell = True)
            # subprocess.Popen(["start",],shell = True)
            open_jupyter_notebook()
        else:
            speak("Unsupported operating system.")
    except:
        speak('sorry sir we fail to open your workspace')
     
def hello_kallu():
    speak("Hello Sir, My name is servant. How can i assisst you") # kallu
def my_self():
    speak("Hey there! I am [qqalloo], your personal assistant here to make life a little easier. Need a hand with something or just want to know what I can do? Just ask! I am here to help you with whatever you need, whenever you need it. Lets get started!")
    pass

def open_calculator():
    speak("Opening Calculator")
    try:
        # For Windows, the calculator app can be opened directly
        if platform.system() == "Windows":
            subprocess.Popen("calc")
        else:
            speak("Calculator functionality is not supported on this OS.")
    except Exception as e:
        speak(f"An error occurred while opening the Calculator: {e}")
def speak_current_time():

    # Get the current time
    now = datetime.now()

    # %I: Represents the hour (01 to 12) in a 12-hour clock format.
    # %M: Represents the minute (00 to 59).
    # %p: Represents AM or PM.
    current_time = now.strftime("%I:%M %p")

    # Prepare the speech
    speech = f"The current time is {current_time}"

    # Speak the current time
    speak(speech)
def open_chatgpt_and_search(search_text):
    speak(f'Seraching for{search_text}')
    try:
        with sync_playwright() as p:
            # Launch a new browser
            browser = p.chromium.launch(headless=True)  # Set headless=True to run in headless mode
            context = browser.new_context()
            page = context.new_page()
            
            # login page
            blackbox_url = "https://www.blackbox.ai/"
            # div..class..flex items-center justify-center   ---> button click
            # Navigate to ChatGPT
            page.goto(blackbox_url)
            time.sleep(5)
            # Type the search text into the input field
            input_field = page.query_selector("textarea[id='chat-input-box']")
            input_field.fill(f'what is {search_text}?')
            # print(f'{search_text} filled')
            # Submit the query (assuming Enter key is used)
            input_field.press("Enter")
            # print('Enter press')
            time.sleep(20)
            # Wait for the response to be displayed
            paragraphs =page.locator("div.prose.break-words.dark\\:prose-invert.prose-p\\:leading-relaxed.prose-pre\\:p-0.fix-max-with-100 p.mb-2.last\\:mb-0").all_text_contents()  # Update this selector based on the actual response element
            # prose break-words dark:prose-invert prose-p:leading-relaxed prose-pre:p-0 fix-max-with-100
            paragraphs = paragraphs[1:3]
            final_result = ' '.join(paragraphs)
            print('ready to speak')
            speak(final_result)
            browser.close()
            
    except Exception as e:
        speak(f"can you search again")
def execute_command(command):
    try:
        if "open my workspace" in command:
            open_workspace()
        elif "hello" in command:
            hello_kallu()
        elif "who are you" in command:
            my_self()
        elif command == 'thank' :
            speak('welcome sir')
        elif command == 'thank u':
            speak('welcome sir')
        elif "open calculator" in command:
            open_calculator()
        elif "search for" in command:
            search_query = command.split("search for",1)[1].strip()
            open_chatgpt_and_search(search_query)
        elif "current time" in command:
            speak_current_time()
    except:
        speak("Command not recognized. Please try again.")

if __name__ == "__main__":
    number_of_time = 1
    while True:
        print(f' we includes all this commands')
        for key, value in dictionary_of_commands.items():
            print(f"{key}: {value}")
        if number_of_time == 1:
            if 5 <= current_hour < 12:
                speak('Good Morning Sir, My name is servant. How can i assisst you')
            elif 12 <= current_hour < 17:
                speak('Good Afternoon Sir, My name is servant . How can i assisst you')
            elif 17 <= current_hour < 21:
                speak('Good Evening Sir, My name is servant . How can i assisst you')
            else:
                speak('Hello Sir')
        number_of_time = number_of_time + 1
        command = recognize_speech()
        if command:
            execute_command(command)
        if command == 'shutdown':
            speak('Okay sir, shuttingdown')
            break
        if command == 'close':
            speak('Okay sir, closing')
            break
        