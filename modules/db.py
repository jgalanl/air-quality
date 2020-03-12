import pyrebase
import json
from datetime import date

with open('config.json') as config_file:
    firebaseConfig = json.load(config_file)

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()

def insert(temperature, pressure, humidity, gas_resistance):
    try:
        data = {
            "Date": {
                "day": date.today().strftime("%H:%M:%S, %d/%m/%Y")
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