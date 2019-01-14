#!/usr/bin/python
# -*- coding: UTF-8 -*-


from flask import Flask, current_app
import os 
from utils import mail, setting
from utils.os_info import isARMOS
from view.login import login 
from view.home import webcam

app = Flask(__name__)
app.register_blueprint(login)
app.register_blueprint(webcam)

if __name__ == '__main__':
    # read configuration file 
    setting.initialization()

    # send email 
    if isARMOS():
        mail.mailSend(setting.getGamilConfig())

    # used for session 
    app.secret_key = os.urandom(12)

    if isARMOS():
        host = "0.0.0.0" 
        debug = False
    else: 
        host = "127.0.0.1"
        debug = True

    # activate application context 
    with app.app_context():
        current_app.admin_is_logged = False 

    app.run(host=host, debug=debug, port=setting.getPortNum(), threaded=True)
