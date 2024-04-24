import os
from dotenv import load_dotenv
import unittest
from unittest.mock import patch, MagicMock

import requests_mock

from website.getAPIdata import get_api_key, get_weather, get_forecast, getApiData

def test_get_weather():
    city = "Prague"
    weather_data = get_weather(city)
    assert weather_data


def test_get_api_key_with_valid_env_variable():
    os.getenv = MagicMock().return_value('valid_api_key')
    api_key = get_api_key()
    assert(api_key)


def test_get_api_key_with_missing_env_variable():
    load_dotenv = MagicMock().return_value(None)
    api_key = get_api_key()
    assert(api_key)


if __name__ == '__main__':
    unittest.main()
  