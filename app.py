#!/usr/bin/env python
from importlib import import_module
from flask import Flask, render_template, Response, request, flash, session, redirect, url_for, current_app 

from utils import mail, setting 
import os 

is_os_arm = ( os.uname()[4][:3] == 'arm' ) 

webcam = Flask(__name__)

@webcam.route('/', methods=['GET', 'POST'])
def home():
    """Video streaming home page."""
    if request.method == 'GET': 
        return render_template('index.html')
    elif request.method == 'POST':
        return redirect(url_for('login'))
    else: 
        return "Unsupported method"


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# check x86 or raspberry pi 
if is_os_arm:
    from camera_opencv import Camera
else: 
    from camera_pc import Camera
@webcam.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')




@webcam.route('/login', methods=['GET', 'POST'])
def login(): 
    """Login page"""
    if request.method == 'GET': 
        return render_template('login.html')
    elif request.method == 'POST':        
        if request.form['password'] == setting.getAdminConfig()["passwd"] and request.form['username'] == setting.getAdminConfig()["user"]:   
            if not current_app.admin_is_logged:      
                current_app.admin_is_logged = True
                session['logged_in'] = True 
                return redirect(url_for('home'))
            else: 
                flash('Another administrator has already logged in. Only one person can log in every time')
                return redirect(url_for('login'))
        else: 
            flash('Wrong username or password!')
            return redirect(url_for('login'))
    else: 
        return "Unsupported method"


@webcam.route('/logout', methods=['POST'])
def logout():
    current_app.admin_is_logged = False
    session['logged_in'] = False
    return redirect(url_for('home'))


if __name__ == '__main__':
    if is_os_arm:
        mail.mailSend(setting.getGamilConfig())
    # used for session 
    webcam.secret_key = os.urandom(12)
    if is_os_arm:
        host = "0.0.0.0" 
        debug = False
    else: 
        host = "127.0.0.1"
        debug = True

    # activate application context 
    with webcam.app_context():
        current_app.admin_is_logged = False 

    webcam.run(host=host, debug=debug, port=setting.getPortNum(), threaded=True)
