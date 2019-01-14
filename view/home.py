#!/usr/bin/python
# -*- coding: UTF-8 -*-

from flask import Blueprint, render_template, Response, request, session, redirect, url_for, current_app
from utils.os_info import isARMOS 

webcam = Blueprint('webcam', __name__)

_para = {} 
_para["resolution"] = "200x200"
_para["drc"] = "off"
_para["brightness"] = 50
_para["contrast"] = 0

# check x86 or raspberry pi 
if isARMOS():
    from camera.camera_opencv import Camera
else: 
    from camera.camera_pc import Camera


_camera = Camera()
if isARMOS():
    _camera.setCamera(_para)

@webcam.route('/', methods=['GET', 'POST'])
def home():
    """Video streaming home page."""
    if request.method == 'GET': 
        return render_template('index.html', para=_para)
    elif request.method == 'POST':
        return redirect(url_for('login.handlelogin'))
    else: 
        return "Unsupported method"



@webcam.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def gen(camera):
    """Video streaming generator function."""
    camera.start()
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



@webcam.route('/config', methods=['POST'])
def config():
    """Configuration"""
    _para["resolution"] = request.form.get("resolution", "200x200")
    _para["drc"] = request.form.get("drc", "off") 
    _para["brightness"] = int(request.form.get("brightness", 50))
    _para["contrast"] = int(request.form.get("contrast", 0))
    #print(current_app.para)
    return redirect(url_for('.home'))


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
    return "nothing"
