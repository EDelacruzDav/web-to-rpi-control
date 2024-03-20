import RPi.GPIO as GPIO
from time import sleep
from flask import Flask, render_template, Response, stream_with_context, request
from flask import request
import cv2
import numpy

video = cv2.VideoCapture(0)
app = Flask(__name__)

in1 = 24
in2 = 23
en = 25
temp1=1

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en,100)

def video_stream():
    while True:
        ret, frame = video.read()
        if not ret:
            break
        else:
            ret, buffer = cv2.imencode('.jpeg', frame)
            frame = buffer.tobytes()
            yield (b' --frame\r\n' b'Content-type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route("/video_feed")
def video_feed():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/set_speed")
def set_speed():
    speed = request.args.get("speed")
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    if int(speed) < 0:
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
    p.ChangeDutyCycle(abs(int(speed)))

    return "Recieved " + str(speed)


@app.route("/")
def web():
    html = open("web.html")
    response = html.read().replace('\n', '')
    html.close()
    p.start(0)
    return response
app.run(host = '172.17.21.24')

