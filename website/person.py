from typing import Collection

from dotenv import load_dotenv
import os
import requests

class Person:
    def __init__(
        self, name: str, age: int, *, jobs: Collection[str] | None = None
    ) -> None:
        self.name = name
        self.age = age
        self.jobs = jobs or []
        
    @property
    def forename(self) -> str:
        return self.name.split(" ")[0]
    
    @property
    def surname(self) -> str:
        name = self.name.split(" ")[-1]
        return name if name != self.forename else None

    def celebrateBirthday(self) -> None:
        self.age += 1
        
    def addJob(self, title: str) -> None:
        self.jobs.append(title)  

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
    
    
    loc = weather_data['location']['name']
    actualTemp = weather_data['current']['temp_c']
    textWeather =weather_data['current']['condition']['text']

    
    return loc, actualTemp, textWeather