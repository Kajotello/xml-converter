import pytest
from unittest.mock import patch, mock_open
from src.converter_class import Converter
import io
import json



@pytest.fixture
def converter():
    return Converter('test', 'test')


def test_make_conversion(converter):

    example_input_file = io.StringIO('''{
     "FLIGHT": {
        "AIRCRAFT_REGISTRATION": "SPLSA",
        "FLIGHT_NUMBER": 458,
        "FLIGHT_DATE": "2024-03-20",
        "DEPARTURE_AIRPORT": "WAW",
        "ARRIVAL_AIRPORT": "JFK",
        "SCHEDULE_DEPARTURE_TIME": "2024-03-20 13:00:00",
        "REFUELED_AT": "2024-03-20 12:30:00"
     }
    }''')

    result = io.StringIO('')
    converter._make_conversion(example_input_file, result)
    assert result.getvalue() == \
    """<FLIGHT>
\t<AIRCRAFT_REGISTRATION>SPLSA</AIRCRAFT_REGISTRATION>
\t<FLIGHT_NUMBER>458</FLIGHT_NUMBER>
\t<FLIGHT_DATE>2024-03-20</FLIGHT_DATE>
\t<DEPARTURE_AIRPORT>WAW</DEPARTURE_AIRPORT>
\t<ARRIVAL_AIRPORT>JFK</ARRIVAL_AIRPORT>
\t<SCHEDULE_DEPARTURE_TIME>2024-03-20 13:00:00</SCHEDULE_DEPARTURE_TIME>
\t<REFUELED_AT>2024-03-20 12:30:00</REFUELED_AT>
</FLIGHT>"""

def test_make_conversion_different_root():

    example_input_different_root = io.StringIO('''{
     "refueling": {
        "AIRCRAFT_REGISTRATION": "SPLSA",
        "FLIGHT_NUMBER": 458,
        "FLIGHT_DATE": "2024-03-20",
        "DEPARTURE_AIRPORT": "WAW",
        "ARRIVAL_AIRPORT": "JFK",
        "SCHEDULE_DEPARTURE_TIME": "2024-03-20 13:00:00",
        "REFUELED_AT": "2024-03-20 12:30:00"
     }
    }''')


    converter = Converter('test', 'test', 'refueling')
    result = io.StringIO('')
    converter._make_conversion(example_input_different_root, result)
    assert result.getvalue() == \
    """<refueling>
\t<AIRCRAFT_REGISTRATION>SPLSA</AIRCRAFT_REGISTRATION>
\t<FLIGHT_NUMBER>458</FLIGHT_NUMBER>
\t<FLIGHT_DATE>2024-03-20</FLIGHT_DATE>
\t<DEPARTURE_AIRPORT>WAW</DEPARTURE_AIRPORT>
\t<ARRIVAL_AIRPORT>JFK</ARRIVAL_AIRPORT>
\t<SCHEDULE_DEPARTURE_TIME>2024-03-20 13:00:00</SCHEDULE_DEPARTURE_TIME>
\t<REFUELED_AT>2024-03-20 12:30:00</REFUELED_AT>
</refueling>"""

def test_make_conversion_corrupted_file_missing_bracket(converter):

    corrupted_input_file_missing_bracket = io.StringIO('''{
     "FLIGHT": {
        "AIRCRAFT_REGISTRATION": "SPLSA",
        "FLIGHT_NUMBER": 458,
        "FLIGHT_DATE": "2024-03-20",
        "DEPARTURE_AIRPORT": "WAW",
        "ARRIVAL_AIRPORT": "JFK",
        "SCHEDULE_DEPARTURE_TIME": "2024-03-20 13:00:00",
        "REFUELED_AT": "2024-03-20 12:30:00"
    }''')
    result = io.StringIO('')
    with pytest.raises(json.JSONDecodeError):
        converter._make_conversion(corrupted_input_file_missing_bracket, result)
        

def test_make_conversion_corrupted_file_missing_comma(converter):

    corrupted_input_file_missing_comma = io.StringIO('''{
     "FLIGHT": {
        "AIRCRAFT_REGISTRATION": "SPLSA",
        "FLIGHT_NUMBER": 458,
        "FLIGHT_DATE": "2024-03-20",
        "DEPARTURE_AIRPORT": "WAW",
        "ARRIVAL_AIRPORT": "JFK",
        "SCHEDULE_DEPARTURE_TIME": "2024-03-20 13:00:00",
        "REFUELED_AT": "2024-03-20 12:30:00"
    }''')

    result = io.StringIO('')
    with pytest.raises(json.JSONDecodeError):
        converter._make_conversion(corrupted_input_file_missing_comma, result)