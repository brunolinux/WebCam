#!/usr/bin/env python
from importlib import import_module
from flask import Flask, render_template, Response
from camera_opencv import Camera	
from utils import mail

webcam = Flask(__name__)

username = "your@email.com"
password = "yourpasswd"

@webcam.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@webcam.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    mail.mailSend(username, password)
    webcam.run(host="0.0.0.0", debug=False, port=8000, threaded=True)
