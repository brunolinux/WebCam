#!/usr/bin/python
# -*- coding: UTF-8 -*-

from flask import Blueprint, render_template, Response, request, flash, session, redirect, url_for, current_app
from utils.os_info import isARMOS 

webcam = Blueprint('webcam', __name__)


@webcam.route('/', methods=['GET', 'POST'])
def home():
    """Video streaming home page."""
    if request.method == 'GET': 
        return render_template('index.html')
    elif request.method == 'POST':
        return redirect(url_for('login.handlelogin'))
    else: 
        return "Unsupported method"




# check x86 or raspberry pi 
if isARMOS():
    from camera.camera_opencv import Camera
else: 
    from camera.camera_pc import Camera
@webcam.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



@webcam.route('/config', methods=['POST'])
def config():
    """Configuration"""

    print("config")
    print(request.form.get("resolution"))



@webcam.route('/logout', methods=['POST'])
def logout():
    current_app.admin_is_logged = False
    session['logged_in'] = False
    return redirect(url_for('.home'))


@webcam.route('/onbeforeunload')
def onUnLoadEvent():
    if session.get('logged_in', False):
        session.clear()
        current_app.admin_is_logged = False
        #print("cleared")
    return "nothing"
