import os
from dotenv import load_dotenv

import unittest
from unittest.mock import patch, MagicMock


from website.getAPIdata import getApiKey, getWeather, getForecast, getApiData

class TestGetApiKey(unittest.TestCase):
    def test_getApiKey_return(self):
        self.assertEqual(getApiKey(), os.getenv('API_KEY'))

class TestGetWeather(unittest.TestCase):
    def test_get_weather_valid_city(self):
        city = 'London'
        loc, actualTemp, textWeather = getApiData(city)
        self.assertEqual(loc,'London')
        self.assertTrue(isinstance(actualTemp,float))
        self.assertTrue(isinstance(textWeather, str))

class TestGetForecast(unittest.TestCase):
    def test_get_forecast_valid_city(self):
        city = 'London'
        forecast_data = getForecast(city)
        self.assertTrue('error' not in forecast_data)
        self.assertTrue('forecast' in forecast_data)
        self.assertEqual(forecast_data['location']['name'],city)
        self.assertEqual(len(forecast_data['forecast']['forecastday']), 7)
        
if __name__ == '__main__':
    unittest.main() 

