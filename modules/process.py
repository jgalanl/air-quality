#!/usr/bin/env python3

from db import extract

def get_data():
    print("--- INICIANDO EXTRACCIÓN DE DATOS ---")
    try:
        result = extract()

    except Exception as exc:
        print(exc)

    print(result.val())
    print("--- EXTRACCIÓN DE DATOS CORRECTA")

if __name__ == "__main__":
    get_data()