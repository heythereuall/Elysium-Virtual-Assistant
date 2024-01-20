import pyttsx3  # text to speech lib
import speech_recognition as sr  # pip install speechRecognition lib
import datetime  # lib for date  and time
import wikipedia  # pip install wikipedia lib
import webbrowser  # lib for opening web browser
from colorama import init, Fore  # for animation
import time  # for time fetch
import requests  # for fetching request for API
import pyjokes  # for jokes lib
from newsapi import NewsApiClient  # news Api


def loading_animation():  # fun for animation
    # print statement means printing on terminal everywhere
    print("Initializing Elysium...", end="", flush=True)
    for _ in range(5):
        time.sleep(0.5)
        print(Fore.YELLOW + ".", end="", flush=True)
    print(Fore.RESET + "\n")


MASTER = "Aditi"

engine = pyttsx3.init('sapi5')   # voice engine
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(text):    # to speak what to say
    engine.say(text)
    engine.runAndWait()


def get_weather(city):  # weather city fucntion
    # weather city api key fetched from a friend
    api_key = '148e6a91ffd20655d50414de299111d6'
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=148e6a91ffd20655d50414de299111d6"

    try:
        response = requests.get(base_url)
        data = response.json()

        if data["cod"] != "404":
            main_data = data["main"]
            temperature_kelvin = main_data["temp"]
            temperature_celsius = temperature_kelvin - 273.15
            temperature_celsius_rounded = round(temperature_celsius, 2)
            weather_description = data["weather"][0]["description"]

            speak(
                f"The temperature in {city} is {temperature_celsius_rounded} Celsius with {weather_description}.")
        else:
            speak(f"Sorry, I couldn't find weather information for {city}.")

    except Exception as e:
        print(f"Error fetching weather information: {e}")
        speak("Sorry, there was an error fetching weather information.")


def wishMe():  # fun to wish
    hour = int(datetime.datetime.now().hour)
    print(hour)

    if hour >= 0 and hour < 12:
        speak("good morning" + MASTER)
    elif hour >= 12 and hour < 18:
        speak("good afternoon" + MASTER)

    else:
        speak("good Evening" + MASTER)

    speak("i am your assistant. How may I help you?")


def takeCommand():  # function to listen to command given by us
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}\n")

    except Exception as e:
        print("Say that again please...")
        query = ""

    return query


def tell_joke():  # fun to tell a joke
    joke = pyjokes.get_joke()
    speak(joke)
    print("Joke:", joke)


def google_search(query):  # fun to google search
    speak("Searching on Google")
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)


def get_news():  # fun to news fetch
    newsapi = NewsApiClient(api_key='c442231f05d34f349f0e3c572c7a2ee1')
    top_headlines = newsapi.get_top_headlines(
        language='en', country='us', page_size=5)

    articles = top_headlines['articles']

    for idx, article in enumerate(articles, start=1):
        title = article['title']
        speak(f"News {idx}: {title}")
        print(f"News {idx}: {title}")


def main():  # main fun that starts at the beggening other function calls inside of the main fucntion only
    speak("Initializing Elysium...")
    loading_animation()

    while True:
        wishMe()
        query = takeCommand()

        if 'wikipedia' in query.lower():  # query.lower means what we said in mic has wikipedia in it
            speak('searching Wikipedia...')
            query = query.replace("wikipedia", "")
            # these two are passing parameters
            results = wikipedia.summary(query, sentences=2)
            print(results)
            speak(results)

        elif 'open youtube' in query.lower():
            url = "https://www.youtube.com/"
            webbrowser.open(url)

        elif 'news' in query.lower():
            speak('Fetching the latest news headlines...')
            get_news()

        elif 'open google' in query.lower():
            url = "https://www.google.com/"
            webbrowser.open(url)

        elif 'joke' in query.lower():
            tell_joke()

        elif 'weather' in query.lower():
            speak("Sure, for which city?")
            city = takeCommand()  # params
            get_weather(city)

        elif 'the time' in query.lower():
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"{MASTER} the time is {strTime}")
            print("Time", strTime)

        elif 'stop' in query.lower():
            speak("Exiting Elysium.")
            break

        elif 'google' in query.lower():
            google_search(query)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:  # enterruption is here if i write something on terminal the elysium willl stop
        print('Exiting Elysium')
