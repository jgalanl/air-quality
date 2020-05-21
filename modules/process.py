#!/usr/bin/env python3

from db import extract, insert
# from sensor import read_data
from api import get_api

def get_data():
    print("--- INICIANDO EXTRACCIÓN DE DATOS ---")
    try:
        result = extract()

    except Exception as exc:
        print(exc)

    print(result.val())
    print("--- EXTRACCIÓN DE DATOS CORRECTA ---")

    # TODO Llamar al read_data del sensor para coger sus datos


    # Weather API
    api_data = get_api()
    print("--- Leganés Weather Data ---\n", api_data) # Important values: weather, main & clouds

    # TODO Unir datos del sensor y del API


    # TODO Llamar al insert de db para guardar el nuevo objeto en Firebase


if __name__ == "__main__":
    get_data()