from dotenv import load_dotenv
import os
import requests

def getApiKey():
    load_dotenv()
    api_key = os.getenv('API_KEY')
    return api_key

def getWeather(city):
    url = f"http://api.weatherapi.com/v1/current.json?key={getApiKey()}&q={city}"
    response = requests.get(url)
    data = response.json()
    return data

def getForecast(city):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={getApiKey()}&q={city}&days=7"
    response = requests.get(url)
    data = response.json()
    return data

def getApiData(cityName):
    weather_data = getWeather(cityName)
    weather_forecast = getForecast(cityName)
    if 'error' in weather_data or 'error' in weather_forecast:
        error = weather_data['error']['message']
    else:
        error = None
    
    loc = weather_data['location']['name']
    actualTemp = weather_data['current']['temp_c']
    textWeather = weather_data['current']['condition']['text']
    imgWeather = weather_data['current']['condition']['icon']
    
    # print(type(imgWeather))
    
    return loc, actualTemp, textWeather