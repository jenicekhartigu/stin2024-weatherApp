from dotenv import load_dotenv
import os
import requests

def get_api_key():
    load_dotenv()
    api_key = os.getenv('API_KEY')
    return api_key

def get_weather(city):
    url = f"http://api.weatherapi.com/v1/current.json?key={get_api_key()}&q={city}"
    response = requests.get(url)
    data = response.json()
    return data

def get_forecast(city):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={get_api_key()}&q={city}&days=7"
    response = requests.get(url)
    data = response.json()
    return data

def getApiData(cityName):
    weather_data = get_weather(cityName)
    weather_forecast = get_forecast(cityName)
    if 'error' in weather_data or 'error' in weather_forecast:
        error = weather_data['error']['message']
    else:
        error = None
    
    print(weather_data['current'])
    loc = weather_data['location']['name']
    actualTemp = weather_data['current']['temp_c']
    textWeather = weather_data['current']['condition']['text']
    imgWeather = weather_data['current']['condition']['icon']
    
    print(type(imgWeather))
    
    return loc, actualTemp, textWeather