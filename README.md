# python-rest-sensehat

Make a [Raspberry Pi](https://www.raspberrypi.org) with [Sense HAT](https://projects.raspberrypi.org/en/projects/getting-started-with-the-sense-hat) a simple [SAP Leonardo IoT Device](https://www.sap.com/products/leonardo.html)

This python script was created as a showcase for the SAP Leonardo IoT capabilities. It reads some sensor data (enviroment data and gyrsocope data) from Sense HAT and sends the data to the SAP Cloud Platform's IoT service. 

The script is prepared to run the Raspberry in headless mode, once an internet connection is confgured. Errors will be displayed on the Sense HAT's 8x8 LED matrix. If the script runs ok, a  plasma effect will be shown on the LED matrix.

![SAP Leonardo Cockpit](https://github.com/jenska/python-rest-sensehat/blob/master/images/rasp001.JPG "SAP Leonardo Cockpit")

Annotations
+ The script uses the IoT REST gateway service because I had problems with the paho-mqtt library to establish a secure connection. Vice versa I wasn't able to access Sense HAT's sensor data when using NodeJS while mqtt works fine with NodeJS.
+ The device certificate contains an encrypted private key and is therefore decrypted with the secret. The decrypted key is stored locally  in 'certificate.key'.

## Precondition 

+ a Raspberry Pi with a Sense HAT and Raspbian installed
+ SAP Leonardo IoT subscription for Cloud Foundry subaccounot. The showcase should also work with a [free trial account](https://developers.sap.com/tutorials/hcp-create-trial-account.html). 

## Setup 

### Leonardo

Follow the instructions in https://developers.sap.com/tutorials/iot-express-2-create-device-model.html to create a simple IoT device model.
Create your device with 2 sensors and capabilities as shown below. Use the REST gateway for your device! 

![raspberry1](https://github.com/jenska/python-rest-sensehat/blob/master/images/rasp002.JPG "raspberry1")

![env](https://github.com/jenska/python-rest-sensehat/blob/master/images/rasp003.JPG "env")

![gyro](https://github.com/jenska/python-rest-sensehat/blob/master/images/rasp004.JPG "gyro")

### Python

Type this command into the terminal to install the Sense HAT package:

```bash
sudo apt install sense-hat
```
Download your certificate as a pem file and place it into the script's folder.

![pem](https://github.com/jenska/python-rest-sensehat/blob/master/images/rasp005.JPG "pem")

Rename 'configuration.json.bak ' to 'configuration.json' and enter your alternate ID's of your device and sensors.
Also replace the pem file name.

## Run

```bash
python3 leonardo.py
```
