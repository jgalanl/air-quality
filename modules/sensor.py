#!/usr/bin/env python3

import bme680
import time
import sys

from db import insert

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except IOError:
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

def read_data():
    print('\n\nIniciando lectura:')
    try:
        if sensor.get_sensor_data():
            insert(sensor.data.temperature, sensor.data.pressure, 
            sensor.data.humidity, sensor.data.gas_resistance)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    read_data()