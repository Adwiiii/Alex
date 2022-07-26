import smtplib
import pywhatkit  # for playing music on YouTube
import speech_recognition as sr  # for recognizing speech
import pyttsx3  # engine to make the program speak
import webbrowser  # to open things on a default web browser, can be configured to open a certain browser
import wikipedia  # to search things on wikipedia, wikipedia api
import requests  # library to establish connections/ get requests
import datetime  # python's inline date and time library to output current day and time
import pyjokes  # to tell a joke upon command


runtime = True  # to end the program later on when needed
engine = pyttsx3.init()  # configuring the engine for the program to speak
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
activationWord = 'computer'


def takeCommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:

        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")

    except Exception as e:
        print(e)
        print("Unable to Recognize your voice.")
        return "None"


def speak(text, rate=190):  # rate to define speed of the dictation
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()

    # Enable low security in gmail
    server.login('Enter gmail ID', 'Enter gmail Password')
    server.sendmail('Enter gmail ID', to, content)
    server.close()


rec = sr.Recognizer()

my_micro = sr.Microphone(device_index=0)  # source for microphone, may be 0 or 1 depending on source_id

speak("Initiating system check. System check complete"
      "Welcome aboard Captain. I'm Alex. What can i do for you?")  # welcome message, change according to necessity

while runtime:
    print("Say something...")
    with my_micro as source:
        audio = rec.listen(source)
        to_text = rec.recognize_google(audio)
        print(f"You said: {to_text}")
        speak(f"You said {to_text}")
    if "hello" in to_text:
        print("Hello Aditya, How are you?")
        speak("Hello Aditya, How are you?")

    if "fine" in to_text:
        print("That's good to hear!")
        speak("That's good to hear!")

    if "Google" in to_text:
        webbrowser.open("https://google.com")
        speak("Opening Google")

    if "YouTube" in to_text:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube")

    if "Gmail" in to_text:
        webbrowser.open("https://gmail.com")
        speak("Opening Gmail")

    if 'Wikipedia' in to_text:
        speak('Searching Wikipedia...')
        to_text = to_text.replace("Wikipedia", "")
        results = wikipedia.summary(to_text, sentences=3)
        speak("According to Wikipedia")
        print(results)
        speak(results)

    if "song" in to_text:
        speak("What song do you want to play?")
        print("What song do you want to play?")
        try:
            with my_micro as source:
                audio = rec.listen(source)
                music = rec.recognize_google(audio)
                print("You said:", music)
                speak("You said" + music)
                speak("playing" + music)
                pywhatkit.playonyt(music)
        except Exception:
            print("Could not understand what you were trying to tell")
            speak("Could not understand what you were trying to tell")
        runtime = False

    if 'time' in to_text:
        strTime = datetime.datetime.now().strftime("% H:% M:% S")
        print(f"The time is {strTime}")
        speak(f"The time is {strTime}")

    if "weather" in to_text:
        speak("Which place?")
        print("Which place?")
        with my_micro as source:
            audio = rec.listen(source)
            output = rec.recognize_google(audio)
            print("You said: " + output)
        print(f"Displaying weather report for {output}")
        url = 'https://wttr.in/{}'.format(output)
        res = requests.get(url)
        speak(f"Showing weather for {output}")
        print(res.text)
        runtime = False

    if 'joke' in to_text:
        joke = pyjokes.get_joke()
        print(joke)
        speak(joke)

    if "who i am" in to_text:
        print("If you talk then definitely your human, Oh wait even i speak")
        speak("If you talk then definitely your human, Oh wait even i speak")

    if 'is love' in to_text:
        print("It is 7th sense that destroy all other senses")
        speak("It is 7th sense that destroy all other senses")

    if "news" in to_text:
        def NewsFromBBC():
            # BBC news api
            # following query parameters are used
            # source, sortBy and apiKey
            query_params = {
                "source": "bbc-news",
                "sortBy": "top",
                "apiKey": "c04f4aa525cc48b995c9b81e62a349c2"
            }
            main_url = " https://newsapi.org/v1/articles"

            # fetching data in json format
            res = requests.get(main_url, params=query_params)
            open_bbc_page = res.json()

            # getting all articles in a string article
            article = open_bbc_page["articles"]
            print("Displaying news")
            speak("Displaying news")

            # empty list which will
            # contain all trending news
            results = []

            for ar in article:
                results.append(ar["title"])

            for i in range(len(results)):
                # printing all trending news
                print(i + 1, results[i])

        # Driver Code
        if __name__ == '__main__':
            # function call
            NewsFromBBC()
        runtime = False

    if "among" in to_text:
        webbrowser.open("https://amongusplay.online/")
        speak("Opening Among us")

    if "write a note" in to_text:
        speak("What do you want to add to your note?")
        print("What do you want to add to your note?")
        with my_micro as source:
            audio = rec.listen(source)
            note = rec.recognize_google(audio)
        file = open('Alex.txt', 'w')
        file.write(note)
        speak("Note added successfully")

    if "display note" in to_text:
        speak("Showing Notes")
        file = open("Alex.txt", "r")
        print(file.read())

    if "delete note" in to_text:
        speak("Are you sure you want to delete your current notes?")
        print("Are you sure you want to delete your current notes?")
        with my_micro as source:
            audio = rec.listen(source)
            erase = rec.recognize_google(audio)
            if "yes" in erase:
                print("Deleting notes")
                speak("Deleting notes")
                file.close()

    if 'send a mail' in to_text:
        try:
            speak("What should I say?")
            content = takeCommand()
            speak("whom should i send this to?")
            to = input()
            sendEmail(to, content)
            speak("Email has been sent!")
        except Exception as e:
            print(e)
            speak("I am not able to send this email")

    if to_text == "exit":
        speak("Shutting down systems")
        runtime = False
