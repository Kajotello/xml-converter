import pytest
from unittest.mock import patch, mock_open
from src.converter_class import Converter

@pytest.fixture
def source_file_content():
    return '''{
     "FLIGHT": {
        "AIRCRAFT_REGISTRATION": "SPLSA",
        "FLIGHT_NUMBER": 458,
        "FLIGHT_DATE": "2024-03-20",
        "DEPARTURE_AIRPORT": "WAW",
        "ARRIVAL_AIRPORT": "JFK",
        "SCHEDULE_DEPARTURE_TIME": "2024-03-20 13:00:00",
        "REFUELED_AT": "2024-03-20 12:30:00"
     }
    }'''

@pytest.fixture
def corrupter_source_file_content():
    return '''{
     "FLIGHT": {
        "AIRCRAFT_REGISTRATION": "SPLSA",
        "FLIGHT_NUMBER": 458,
        "FLIGHT_DATE": "2024-03-20",
        "DEPARTURE_AIRPORT": "WAW",
        "ARRIVAL_AIRPORT": "JFK",
        "SCHEDULE_DEPARTURE_TIME": "2024-03-20 13:00:00",
        "REFUELED_AT": "2024-03-20 12:30:00"
    }'''

@pytest.fixture
def converter():
    return Converter('test', 'test')



@patch("builtins.open", new_callable=mock_open, read_data="data")
def test_convert_file():
    