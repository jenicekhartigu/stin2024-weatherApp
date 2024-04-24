import os
from dotenv import load_dotenv

import unittest
from unittest.mock import patch, MagicMock


from website.getAPIdata import getApiKey, getWeather, getForecast, getApiData


def test_getApiKey_return():
    assert getApiKey() == os.getenv('API_KEY')

    


