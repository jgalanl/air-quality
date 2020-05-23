import requests
import datetime
import json
from db import insert_api

def get_api():
    resp = requests.get('https://api.openweathermap.org/data/2.5/onecall?lat=40.33&lon=-3.76&exclude=minutely&daily&units=metric&appid=97652d6130c871e828dd201730ec6f06')
    if resp.status_code != 200:
        # This means something went wrong.
        raise ApiError('Error GET /tasks/ {}'.format(resp.status_code))
    
    data_hourly = resp.json()['hourly']
    for data in data_hourly:
        date = datetime.datetime.fromtimestamp(int(data["dt"])).strftime('%d-%m/%H:00')
        weather = data["weather"][0]
        insert_api(date, data, weather)