#!/usr/bin python3

import pyrebase
import json
from datetime import datetime

with open('config.json') as config_file:
    firebaseConfig = json.load(config_file)

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()

def insert_sensor(temperature, pressure, humidity, gas_resistance, air_quality_score, iaq_class):
    try:

        date = datetime.now().strftime('%d-%m/%H:00')
        data = {
            "temperature_sensor": temperature,
            "pressure_sensor": pressure,
            "humidity_sensor": humidity,
            "gas_resistance_sensor": gas_resistance,
            "air_quality_score": air_quality_score,
            "iaq_class": iaq_class
        }

        print(date)
        
        db.child("/Raspberry/" + date).update(data)

    except Exception as exc:
        print(exc)

def insert_api(date_api, data_api, weather_api):
    try:

        data = {
            "date": date_api,
            "temperature": data_api["temp"],
            "feels_like": data_api["temp"],
            "pressure": data_api["pressure"],
            "humidity": data_api["humidity"],
            "dew_point": data_api["temp"],
            "clouds": data_api["clouds"],
            "wind_speed": data_api["wind_speed"],
            "wind_deg": data_api["wind_deg"],
            "id": weather_api["id"],
            "main": weather_api["main"],
            "description": weather_api["description"],
        }
        
        db.child("/Raspberry/" + date_api).update(data)

    except Exception as exc:
        print(exc)

def insert_predicted(date, air_quality_predicted):
    try:

        data = {
            "air_quality_predicted": air_quality_predicted
        }
        
        db.child("/Raspberry/" + date).update(data)

    except Exception as exc:
        print(exc)

def extract_all_data():
    try:
        result = db.child("/Raspberry").get()
    
    except Exception as exc:
        print(exc)

    return result

def extract_date(hour, date):
    try:
        result = db.child("/Raspberry/"+date+"/"+"/"+hour).get()
        
        return result.val()
        
    except Exception as exc:
        print(exc)

def extract_list(date):
    try:
        result = db.child("/Raspberry/"+date).get()

        data = []
        for i in result.each():
            data.append(i.val())

        data.sort(key=lambda x: x.get('air_quality_predicted'))

        return data[:5]

    except Exception as exc:
        print(exc)

if __name__ == "__main__":
    print(extract_list('25-05'))