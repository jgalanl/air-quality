from firebase import firebase
from datetime import date

def insert(temperature, pressure, humidity, gas_resistance):
    try:
        firebase_api = firebase.FirebaseApplication('https://air-quality-2ab4d.firebaseio.com/', None)

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
        
        result = firebase_api.post('/Raspberry/00000000a44b23f9', data)
        print(result)

    except Exception as exc:
        print(exc)