#!/usr/bin/python3

# install sense_hat via apt install sense-hat
# install paho-mqtt via pip3 install paho-mqtt
from sense_hat import SenseHat
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import json
import sys
import requests
import time
import math
import threading

def gyro_payload():
    sense.set_imu_config(False, True, False)  # gyroscope only
    gyro = sense.get_gyroscope()
    gyroConf = configuration['gyroscope']
    gyroConf['measures'] = [ gyro['pitch'], gyro['roll'], gyro['yaw'] ]
    return gyroConf

def environment_payload():
    env = configuration['barometer']
    env['measures'] = [ sense.get_humidity(), sense.get_temperature(), sense.get_pressure()/1000 ]
    return env
    
def post_data(payload):
    data = json.dumps(payload())
    headers = {'content-type': 'application/json'}
    r = requests.post(post_address,data=data, headers = headers,cert=(pem_file, 'certificate.key'), timeout=5)
    r.raise_for_status()
 
def has_connection():
    try:
        _ = requests.get(post_address, timeout=5)
        return True
    except requests.ConnectionError:
        pass
    return False

norm = lambda x: math.floor(255*((x + 1) / 2))

def wobble():
    speed = 0
    while on:
        for x in range(0,8):
            for y in range(0, 8):
                x1 = x * 16
                y1 = y * 16
                x2 = 128 + 128*(math.sin(speed)+math.cos(-speed*0.4))
                y2 = 256 + 128*(math.sin(-speed*0.7)-math.cos(speed*0.3))
                dist = math.sqrt((x1-x2)**2+(y1-y2)**2)
                v = math.sin(x1/40.74 + speed) + math.sin(dist/40.74)
                pixels[(y*8)+x] = palette[round(norm(v/2))]
        speed += 0.15
        sense.set_pixels(pixels)
        time.sleep(0.1)

with open('configuration.json') as json_file:
    configuration = json.load(json_file)
    pem_file = configuration['pemFile']

# decrypt private key
with open(pem_file, 'rb') as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=configuration['secret'].encode('utf-8'),
        backend=default_backend()
    )
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open('certificate.key', 'wb') as cert_file:
        cert_file.write(pem)
                
sense = SenseHat()
post_address = configuration['tenant'] + configuration['deviceAlternateId']
while not has_connection():
    sense.show_message('Waiting for connection... ', text_colour = [255,0,0])

pixels = [0 for i in range(64)]
palette = [(norm(math.cos(math.pi*i/128)), norm(math.sin(math.pi*i/128)), 128) for i in range(256)]
on = True
try:
    wobbler = threading.Thread(target=wobble)
    wobbler.start()
    while True:
        post_data(environment_payload)
        post_data(gyro_payload)
        time.sleep(1)
except Exception as err:
    on = False
    wobbler.join()
    sense.show_message("Aborting due to error: {0}".format(err), text_colour = [255,0,0]) 
