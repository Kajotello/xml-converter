import pytest
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


def test_make_conversion_different_root(converter):

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
    res = io.StringIO('')
    with pytest.raises(json.JSONDecodeError):
        converter._make_conversion(corrupted_input_file_missing_bracket, res)


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


def test_make_conversion_corrupted_file_no_root_dict(converter):

    corrupted_input_file_no_root_dict = io.StringIO('''{}''')

    result = io.StringIO('')
    with pytest.raises(TypeError):
        converter._make_conversion(corrupted_input_file_no_root_dict, result)


def test_make_conversion_corrupted_file_no_root_list(converter):

    corrupted_input_file_no_root_list = io.StringIO('''[]''')

    result = io.StringIO('')
    with pytest.raises(TypeError):
        converter._make_conversion(corrupted_input_file_no_root_list, result)


def test_make_conversion_corrupted_two_top_level(converter):

    corrupted_input_file_two_top_level = io.StringIO('''{
     "FLIGHT": {
        "AIRCRAFT_REGISTRATION": "SPLSA",
        "FLIGHT_NUMBER": 458,
        "FLIGHT_DATE": "2024-03-20",
        "DEPARTURE_AIRPORT": "WAW",
        "ARRIVAL_AIRPORT": "JFK",
        "SCHEDULE_DEPARTURE_TIME": "2024-03-20 13:00:00",
        "REFUELED_AT": "2024-03-20 12:30:00"
        },
    "FLIGHT2": {
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
    with pytest.raises(TypeError):
        converter._make_conversion(corrupted_input_file_two_top_level, result)
