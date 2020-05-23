import json
from sensor import read_data
from api import get_api

if __name__ == "__main__":
    print('\n--- INICIO DE EJECUCCIÓN ---')

    # 1º llamamos a la Weather API
    get_api()

    # Llamar al read_data del sensor
    read_data()

    # TODO Llamar a la clase predictive para realizar la predicción del modelo

    #while True:
    #os.system('python3 sensor.py')
    #time.sleep(3600)