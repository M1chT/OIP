import threading
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, abort, jsonify, make_response
import time
import serial  # need to pip install pyserial
import time
import pygame  # need to pip3 install pygame
from picamera import PiCamera
import cv2
from xmlrpc.client import ServerProxy
import xmlrpc.client

app = Flask(__name__)
# Server ip address
proxy = ServerProxy("http://192.168.120.227:8001")

humidity = ""
result = ""
countrinse = 0
countdry = 0

# take picture


def takepic():
    print("[INFO]Taking Picture...")
    camera = PiCamera()
    camera.capture("/home/pi/ml/img.jpg")
    print("[INFO]Picture Taken...")

    # close the camera after taking picture
    camera.stop_preview()
    camera.close()

    # send image over to server
    with open("/home/pi/ml/img.jpg", "rb") as handle:
        binary_data = xmlrpc.client.Binary(handle.read())
    proxy.server_receive_file(binary_data)


def playMusic():
    pygame.mixer.init()
    pygame.mixer.music.load("endingalarm.wav")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue


@app.route('/')
@app.route('/index')
def index():
    proxy.loadmodel()
    threading.Thread(target=getHumidity).start()
    return render_template("landingpage.html")


def getHumidity():
    global humidity
    ser.flush()

    while True:
        ser.write(b"d")
        time.sleep(0.5)
        line = ser.readline().decode('utf-8').rstrip()
        ser.flush()
        print("Humidity: "+line)
        if line == "Low" or line == "Normal" or line == "High":
            humidity = line
        time.sleep(30)


@app.route('/update', methods=['POST'])
def update():
    global humidity
    return jsonify({
        'humidity': humidity
    })


@app.route('/start')
def start():
    global humidity
    ser.flush()
    ser.write(b"a")  # send 'Start' to Arduino
    print("Raspberry Pi: Send 'Start' to Arduino")
    return render_template("rinse.html")


@app.route("/stain")
def stain():
    global humidity
    global result

    ser.flush()
    while True:
        #line = ser.readline().decode('utf-8').rstrip()
        line = "Done Washing"
        print("Arduino: Send " + line + " to Raspberry Pi")
        time.sleep(0.5)
        if line == "Done Washing":
            ser.write(b"e")
            takepic()
            result = proxy.predicting()
            print("Machine Learning Detected: " + result)
            break
    return render_template("stain.html")


@app.route("/sterilizedry", methods=['GET'])
def sterilizedry():
    global humidity
    global result
    global countrinse
    if result == 'Dirty' and countrinse == 0:
        ser.write(b"a")
        print("Raspberry Pi: Send 'a' to Arduino to start wash cycle")
        countrinse = countrinse + 1
        return render_template("extrarinse.html")
    else:
        ser.write(b"b")  # send to Arduino
        print("Raspberry Pi: Send 'b' to Arduino to start sterilizing and drying")
        return render_template("sterilizedry.html")


@app.route('/checkdry')
def checkdry():
    global humidity
    global result

    ser.flush()
    while True:
        #line = ser.readline().decode('utf-8').rstrip()
        line = "Done Drying"
        humidity = "Low"
        print("Arduino: Send " + line + " to Raspberry Pi")
        time.sleep(0.5)
        if line == "Done Drying" and humidity == 'Low':
            ser.write(b"e")  # send to arduino to on led
            print("Raspberry Pi: Send 'e' to Arduino to on LED for ML Camera")
            takepic()
            result = proxy.predicting()
            break
    print("check dry: " + line)
    return render_template("checkdry.html")


@app.route('/dryextend')
def dryextend():
    global humidity
    ser.write("c")  # send to arduino
    print("Raspberry Pi: Send 'c' to Arduino to extend drying time")
    return render_template("dryextend.html")


@app.route('/end')
def end():
    global humidity
    global result
    global countdry, countrinse
    if result == 'Wet' and countdry == 0:
        countdry = countdry + 1
        return render_template("dryextend.html")
    else:
        threading.Thread(target=playMusic).start()
        countdry = 0
        countrinse = 0
        return render_template("complete.html")


if __name__ == '__main__':
    # to change based on which usb serial port its connected to
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()

    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=8001)
    print("[INFO] App Running")
