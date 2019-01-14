#!/usr/bin/python
# -*- coding: UTF-8 -*-

from flask import Blueprint, render_template, request, current_app, session, redirect, url_for,flash 
from utils import setting 

login = Blueprint('login', __name__)


@login.route('/login', methods=['GET', 'POST'])
def handlelogin(): 
    """Login page"""
    if request.method == 'GET': 
        return render_template('login.html')
    elif request.method == 'POST':        
        if request.form['password'] == setting.getAdminConfig()["passwd"] and request.form['username'] == setting.getAdminConfig()["user"]:   
            if not current_app.admin_is_logged:      
                current_app.admin_is_logged = True
                session['logged_in'] = True 
                return redirect(url_for('webcam.home'))
            else: 
                flash('Another administrator has already logged in. Only one person can log in every time')
                return redirect(url_for('.handlelogin'))
        else: 
            flash('Wrong username or password!')
            return redirect(url_for('.handlelogin'))
    else: 
        return "Unsupported method"
