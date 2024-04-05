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
in3 = 17
in4 = 27
enA = 25
enB = 22
temp1=1

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(enA, GPIO.OUT)
GPIO.setup(enB, GPIO.OUT)

GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
GPIO.output(in3, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)
pA=GPIO.PWM(enA,25)
pB=GPIO.PWM(enB,25)

def video_stream():
    while True:
        ret, frame = video.read()
	#cv2.flip("172.17.21.24:5000/video_feed", 90)
        if not ret:
            break
        else:
            ret, buffer = cv2.imencode('.jpeg', frame)
            frame = buffer.tobytes()
            yield (b' --frame\r\n' b'Content-type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route("/video_feed")
def video_feed():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/set_dir")
def set_dir():
	key = request.args.get("key").lower()
	if key == "w":
		GPIO.output(in1, GPIO.HIGH)
		GPIO.output(in2, GPIO.LOW)
		GPIO.output(in3, GPIO.HIGH)
		GPIO.output(in4, GPIO.LOW)
	if key == "a":
		GPIO.output(in1, GPIO.HIGH)
		GPIO.output(in2, GPIO.LOW)
		GPIO.output(in3, GPIO.LOW)
		GPIO.output(in4, GPIO.HIGH)
	if key == "d":
		GPIO.output(in1, GPIO.LOW)
		GPIO.output(in2, GPIO.HIGH)
		GPIO.output(in3, GPIO.HIGH)
		GPIO.output(in4, GPIO.LOW)
	if key == "s":
		GPIO.output(in1, GPIO.LOW)
		GPIO.output(in2, GPIO.HIGH)
		GPIO.output(in3, GPIO.LOW)
		GPIO.output(in4, GPIO.HIGH)
	if key == "l":
		pA.ChangeDutyCycle(25)
		pB.ChangeDutyCycle(25)
	if key == "m":
		pA.ChangeDutyCycle(50)
		pB.ChangeDutyCycle(50)
	if key == "h":
		pA.ChangeDutyCycle(100)
		pB.ChangeDutyCycle(100)
	return "Recieved " + key

@app.route("/stop_dir")
def stop_dir():
	key = request.args.get("key").lower()
	if key = 'w' or 'a' or 's' or 'd':
		GPIO.output(in1, GPIO.LOW)
		GPIO.output(in2, GPIO.LOW)
		GPIO.output(in3, GPIO.LOW)
		GPIO.output(in4, GPIO.LOW)

@app.route("/")
def web():
    html = open("/home/pi/new-web-to-rpi-control/web-to-rpi-control/templates/web.html")
    response = html.read().replace('\n', '')
    html.close()
    pA.start(100)
    pB.start(100)
    return response
if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug=True)


