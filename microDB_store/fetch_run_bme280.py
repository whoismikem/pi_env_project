import requests
import json
from influxdb import InfluxDBClient


ADDRESS='microapi_bme280:5000' # docker-compose container_name
DB_ADDRESS='db' # docker-compose container_name
DB_NAME='sensor_db'

def to_point(payload):
    data = []
    measurement_name='bme280'
    data.append("{measurement},location={location} temperature={temperature},humidity={humidity},pressure={pressure}"
            .format(measurement=measurement_name,
                    location="closet1",
                    temperature=payload['ambient_temperature'],
                    humidity=payload['humidity'],
                    pressure=payload['pressure']))
    return data

def response_convert(response):
    json_res = response.json()
    point = to_point(json_res)
    print(f'POINT (bme280): {point}')
    return point


try:
    client = InfluxDBClient(host=DB_ADDRESS, port=8086)
    client.switch_database(DB_NAME)
except:
    print("DB Connection broken!")


try:
    url = 'http://' + ADDRESS + '/api/bme280'
    print(f'Connecting to sensor at: {url}')
    response = requests.get(url)
    print(f'RESPONSE (bem280): {response.json()}')
    point = response_convert(response)

    client.write(point, {'db':DB_NAME}, 204, 'line')
except:
    raise("Unable to fetch data")
