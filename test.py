import json
val = {
    "FLIGHT": {
       "AIRCRAFT_REGISTRATION": "SPLSA",
       "FLIGHT_NUMBER": 458,
       "FLIGHT_DATE": "2024-03-20",
       "DEPARTURE_AIRPORT": "WAW",
       "ARRIVAL_AIRPORT": "JFK",
       "SCHEDULE_DEPARTURE_TIME": "2024-03-20 13:00:00",
       "REFUELED_AT": "2024-03-20 12:30:00"
    }
   }

with open('./source/test22.json', 'w') as fh:
    json.dump(val, fh)
