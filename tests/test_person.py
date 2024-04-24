import os
from website import person

import pytest

# @pytest.fixture()
# def person():
#     return Person("Jan Hartig", 26, jobs = ["MicroNova Developer"])

# def test_init(person: Person):
#     assert person.name == "Jan Hartig"
#     assert person.age == 26
#     assert person.jobs == ["MicroNova Developer"]
    
# def test_forname(person: Person):
#     assert person.forename == "Jan"
    
# def test_surname(person: Person):
#     assert person.surname == "Hartig"
    
# def test_no_surname(person: Person):
#     person.name = "Jan"
#     assert not person.surname
    
# def test_celebrateBirthday(person: Person):
#     person.celebrateBirthday()
#     assert person.age == 27
    
# def test_addJob(person: Person):
#     person.addJob("Profesionalní alkoholik")
#     assert person.jobs == ["MicroNova Developer", "Profesionalní alkoholik"]

import unittest
from unittest.mock import patch, MagicMock

from website.person import get_api_key


class TestGetApiKey(unittest.TestCase):

  @patch('os.getenv')
  def test_get_api_key_with_valid_env_variable(self, mock_getenv):
    """Tests if the function retrieves the API key from a valid environment variable."""
    mock_getenv.return_value = 'valid_api_key'
    api_key = get_api_key()
    self.assertEqual(api_key, 'valid_api_key')

  @patch('os.getenv')
  def test_get_api_key_with_missing_env_variable(self, mock_getenv):
    """Tests if the function returns None when the environment variable is missing."""
    mock_getenv.return_value = None
    api_key = get_api_key()
    self.assertIsNone(api_key)


if __name__ == '__main__':
  unittest.main()