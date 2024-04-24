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

def test_get_api_key():
    assert os.getenv("KEY")