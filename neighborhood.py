#!/usr/bin/python


#    r = requests.get('http://api-m2x.att.com/v2/devices/c5b6287c390e0550fb45dda5c46268b4/streams/gate_photos/value')
#    headers = { 'X-M2X-KEY': 'bfc8f2fa2d51975d7757a1fa510e9b97', 'Content-Type': 'application/json' }
#    files = { 'file': open("opencv.png", "rb") }
#    r = requests.post('http://api-m2x.att.com/v2/devices/c5b6287c390e0550fb45dda5c46268b4/streams/gate_photos/value', headers=headers, files=files)
#    print "response: {0}".format(r.text)
import termios, fcntl, sys, os
import time
import requests
import json
import cv2
from imgurpython import ImgurClient
from gpio_96boards import GPIO


client_id = '7144c0f3e16f6f5'
client_secret = 'ac2a4630fa1e21dd5695f9d7a539de74bae7ed40'
client = ImgurClient(client_id, client_secret)
url = None

GPIO_A = GPIO.gpio_id('GPIO_A')
pins = (
    (GPIO_A, 'in'),
)

def sendPicture():
    path = "opencv.png"
    status = client.upload_from_path(path, config=None, anon=True)
    print "status {0}".format(status)
    url = status['link']
    print "url {0}".format(url)
    sendAlert(url)

    
def sendAlert(url):
    r = requests.get('http://api-m2x.att.com/v2/devices/c5b6287c390e0550fb45dda5c46268b4/streams/gate_photos/value')
    headers = { 'X-M2X-KEY': 'bfc8f2fa2d51975d7757a1fa510e9b97', 'Content-Type': 'application/json' }
    payload = { 'value': url }
    r = requests.put('http://api-m2x.att.com/v2/devices/c5b6287c390e0550fb45dda5c46268b4/streams/gate_photos/value', headers=headers, data=json.dumps(payload))
    print "response: {0}".format(r.text)    

def takePicture():
    camera_port = 0
    camera = cv2.VideoCapture(camera_port)
    return_value, image = camera.read()
    cv2.imwrite("opencv.png", image)
    del(camera)  # so that others can use the camera as soon as possible
    sendPicture()

    
def detect(gpio):
    initialize = True
    val = 0
    while True:
        val = gpio.digital_read(GPIO_A)
#        if (False):
        if ( initialize == True ):
            initialize = False
            print "Initializing for 10 seconds {0} {1}".format(gpio.HIGH, gpio.LOW)
            takePicture()
            time.sleep(10)
        else:
            print "val is {0}".format(val)
            if ( val == 1 ):
                print "Picture taken! %d" % val
            else:
                print "No action"
            time.sleep(3)

if __name__ == '__main__':
    while True:
            c = sys.stdin.read(1)
            if c == 'x':
                break
            print 'key pressed'
            takePicture()
#    with GPIO(pins) as gpio:
#        detect(gpio)
