import speech_recognition as sr
import os
import webbrowser
import pyttsx3
import openai
import requests
from config import apikey


messages = []

openai.api_key = apikey

# https://youtu.be/Z3ZAJoi4x6Q
engine = pyttsx3.init()
def chat(query):
    messages.append({"role": "user", "content": query})
    response = openai.chat.completions.create(
    messages= messages,
    model="gpt-3.5-turbo",
)
    # todo: Wrap this inside of a  try catch block
    if(response.choices and response.choices[0].message):
        print(f"Assistant said:{response.choices[0].message.content}")
        engine.say(response.choices[0].message.content)
        engine.runAndWait()
        return response.choices[0].message.content

def get_weather(city):
    weather_api_key = "weather_api"  # Replace with your API key from WeatherAPI.com
    url = f"http://api.weatherapi.com/v1/current.json?key=weather_api&q={city}"
    try:
        response = requests.get(url)
        data = response.json()
        if 'error' not in data:
            weather_description = data['current']['condition']['text']
            temperature = data['current']['temp_c']
            return f"The weather in {city} is {weather_description}. The temperature is {temperature} degrees Celsius."
        else:
            return "Sorry, I couldn't retrieve the weather information."
    except Exception as e:
        return f"An error occurred: {e}"
    
def get_news():
    url = ('https://newsapi.org/v2/top-headlines?'
           'country=in&'
           'apiKey=news_api')
    try:
        response = requests.get(url)
        data = response.json()
        if data["status"] == "ok":
            articles = data["articles"]
            news_list = []
            for article in articles:
                title = article["title"]
                news_list.append(title)
            return (news_list[3] + "\n" + news_list[6])
        else:
            return "Sorry, I couldn't retrieve the news information."
    except Exception as e:
        return f"An error occurred: {e}"

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Jarvis"

if __name__ == '__main__':
    print('Welcome to A.I Assistant')
    engine.say("Hello, I am your A.I Assistant")
    engine.runAndWait()
    while True:
        query = takeCommand()
        # todo: Add more sites
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"],]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                engine.say(f"Opening {site[0]} sir...")
                engine.runAndWait()
                webbrowser.open(site[1])
                exit()

        if "weather" in query.lower():
            city = input("City: ")
            weather_info = get_weather(city)
            print(weather_info)
            engine.say(weather_info)
            engine.runAndWait()
            exit() 

        if "news" in query.lower():
            news_articles = get_news()
            print(news_articles)
            engine.say(f"Here are the top news articles {news_articles}")
            engine.runAndWait()
            exit()   

        if "open music" in query:
            musicPath = "C:\\Users\\agresh\\Downloads\\down-71.mp3"
            os.system(f"open {musicPath}")

        elif "End Chat".lower() in query.lower():
            exit()

        else:
            print("Chatting...")
            chat(query)
