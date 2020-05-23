import bme680
import time
import sys

from db import insert_sensor

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except IOError:
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

hum_weighting = 0.25
gas_weighting = 0.75

gas_reference = 2500
hum_reference = 40
getgasreference_count = 0
gas_lower_limit = 10000
gas_upper_limit = 300000

def getHumidityScore():
    humidity_score = 0
    current_humidity = sensor.data.humidity
    if current_humidity >= 38 and current_humidity <= 42:
        humidity_score = 0.25 * 100
    else:
        if current_humidity < 38:
            humidity_score = 0,25 / hum_reference * current_humidity * 100
        else:
            humidity_score = ((-0.25 / (100 - hum_reference) * current_humidity) + 0.416666) * 100

    return humidity_score

def getGasScore():
    gas_score = 0
    gas_score = (0.75 / (gas_upper_limit - gas_lower_limit) * gas_reference - (gas_lower_limit * (0.75 / (gas_upper_limit - gas_lower_limit)))) * 100.00
    if (gas_score > 75):
        gas_score = 75
    if (gas_score < 0):
        gas_score = 0
    return gas_score

def calculateIAQ(score):
    score = (100 - score) * 5
    if score >= 301:
        return 5
    elif score >= 201 and score <= 300:
        return 4
    elif score >= 151 and score <= 200:
        return 3
    elif score >= 101 and score <= 150:
        return 2
    elif score >= 51 and score <= 100:
        return 1
    elif score >= 0 and score <= 50:
        return 0 

def read_data():
    print('\n\nIniciando lectura...:')
    try:
        if sensor.get_sensor_data():
            humidity_score = getHumidityScore()
            gas_score = getGasScore()
            air_quality_score = humidity_score + gas_score
            iaq_class = calculateIAQ(air_quality_score)

            insert_sensor(sensor.data.temperature, sensor.data.pressure, 
            sensor.data.humidity, sensor.data.gas_resistance,
            air_quality_score, iaq_class)
            
            print("Lectura finalizada!")
            return data
    except KeyboardInterrupt:
        pass