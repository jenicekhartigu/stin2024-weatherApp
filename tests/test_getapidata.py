
from website.getAPIdata import get_weather, get_forecast, get_history, show_weather, current_location

def test_get_weather():
    city = "Prague"
    weather_data = get_weather(city)
    assert 'error' not in weather_data

def test_get_forecast():
    city = "Prague"
    weather_data = get_forecast(city)
    assert 'error' not in weather_data

def test_get_history():
    city = "Prague"
    days_num = 7
    weather_history = get_history(city, days_num)
    assert isinstance(weather_history, list)

def test_show_weather():
    city = "Prague"
    weather_data, weather_forecast, weather_history, error, loc = show_weather(city)
    assert error is None
