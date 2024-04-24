import os
from dotenv import load_dotenv

import unittest
from unittest.mock import patch, MagicMock


from website.getAPIdata import getApiKey, getWeather, getForecast, getApiData


def test_getApiKey_return():
    assert getApiKey() == os.getenv('API_KEY')

    
def test_get_weather_valid_city():
    city = 'London'
    loc, actualTemp, textWeather = getApiData(city)
    assert loc == 'London'
    assert isinstance(actualTemp, float)
    assert isinstance(textWeather, str)


def test_get_forecast_valid_city():
    city = 'London'
    forecast_data = getForecast(city)
    # assert 'error' not in forecast_data
    assert 'forecast' in forecast_data
    assert forecast_data['location']['name'] == city
    assert len(forecast_data['forecast']['forecastday']) == 7
