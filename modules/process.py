#!/usr/bin python3

import time
from sensor import read_data
from api import get_api


if __name__ == "__main__":

    while True:
        print('\n--- INICIO DE EJECUCCIÓN ---')
        # 1º llamamos a la Weather API
        get_api()

        # Llamar al read_data del sensor
        read_data()
        
        # time.sleep(3600) No hace falta. utilizar Crontab

    # TODO Llamar a la clase predictive para realizar la predicción del modelo

    