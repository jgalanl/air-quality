#!/usr/bin/env python3

import pyrebase
import json
from datetime import datetime

with open('../config.json') as config_file:
    firebaseConfig = json.load(config_file)

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()

def insert(temperature, pressure, humidity, gas_resistance):
    try:
        data = {
            "Date": {
                "day": datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            },
            "Data": {
                "temperature": temperature,
                "pressure": pressure,
                "humidity": humidity,
                "gas_resistance": gas_resistance
            }
        }
        
        db.child("/Raspberry/00000000a44b23f9").push(data)

    except Exception as exc:
        print(exc)