
from website.getAPIdata import getApiKey, getWeather, getForecast, getApiData

def test_get_weather():
    city = "Prague"
    weather_data = getWeather(city)
    assert 'error' not in weather_data

def test_get_forecast():
    city = "Prague"
    weather_data = getForecast(city)
    assert 'error' not in weather_data

# def test_get_history():
#     city = "Prague"
#     days_num = 7
#     weather_history = get_history(city, days_num)
#     assert isinstance(weather_history, list)
