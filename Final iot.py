import RPi.GPIO as GPIO
from time import sleep
import datetime
import time
from firebase import firebase
import Adafruit_DHT

import urllib2, urllib, httplib
import json
import os 
from functools import partial

#Air quality
import RPi.GPIO as GPIO
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.IN)
GPIO.setup(27, GPIO.OUT)
#air quality


#rain
from time import sleep

from gpiozero import InputDevice
 
no_rain = InputDevice(18)
 
#rain

GPIO.setmode(GPIO.BCM)


GPIO.setwarnings(False)

# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
sensor = Adafruit_DHT.DHT22

# Example using a Beaglebone Black with DHT sensor
# connected to pin P8_11.
pin = 4

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)


firebase = firebase.FirebaseApplication('https://iotraspi-4f2aa.firebaseio.com/', None)
#firebase.put("/dht", "/temp", "0.00")
#firebase.put("/dht", "/humidity", "0.00")

def update_firebase():

    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        sleep(5)
        str_temp = ' {0:0.2f} *C '.format(temperature)  
        str_hum  = ' {0:0.2f} %'.format(humidity)
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        
        
            
    else:
        print('Failed to get reading. Try again!')  
        sleep(10)

    data = {"temp": temperature, "humidity": humidity}
    firebase.post('sensor', data)
    
    #rain   
    if not no_rain.is_active:
        print("It's raining - get the washing in!")  
        sleep(1)
        
        data1 = {"rain": 'its raining'}
        firebase.post('sensor', data1)
        
       #air 
    if GPIO.input(20):
         print('Cool environment')
         time.sleep(1)
    if GPIO.input(20)!=1:
         print('Detection de GAS')
         GPIO.output(27, False)
         time.sleep(0.1)
         GPIO.output(27, True)
         data2 = {"air": 'Detecting de gas'}
         firebase.post('sensor', data2)
    

while True:
        update_firebase()
        
        #sleepTime = int(sleepTime)
        sleep(3)