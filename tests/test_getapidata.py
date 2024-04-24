
from website.getAPIdata import get_weather, get_forecast, get_history, show_weather, current_location, get_api_key

def test_get_weather():
    city = "Prague"
    weather_data = get_weather(city)
    assert 'error' not in weather_data

def test_get_forecast():
    get_api_key()
    city = "Prague"
    weather_data = get_forecast(city)
    assert 'error' not in weather_data

def test_get_history():
    get_api_key()
    city = "Prague"
    days_num = 7
    weather_history = get_history(city, days_num)
    assert isinstance(weather_history, list)

def test_show_weather():
    get_api_key()
    city = "Prague"
    weather_data, weather_forecast, weather_history, error, loc = show_weather(city)
    assert error is None

def test_current_location():
    result = current_location()
    assert result == None