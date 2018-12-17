#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib 
import subprocess
import os 

from email.mime.text import MIMEText
from email.header import Header

smtp_ssl_host = 'smtp.gmail.com'  # smtp.mail.yahoo.com
smtp_ssl_port = 587
 
sender = 'bruno.liuk@gmail.com'
receivers = ['bruno.liuk@gmail.com']  
 


def checkPingStatus():
    hostname = "google.com"
    response = os.system("ping -c 1 " + hostname)
    if response == 0:
        return True
    else:
        return False


def getIPAddress(): 
    ips = subprocess.check_output(['hostname', '--all-ip-addresses'])
    ips = ips.decode("utf-8")
    ip = ips.split(' ')[0]
    return ip


def mailSend(username, password):
    while True: 
        status = checkPingStatus()
        if status:
            break 
    ip = getIPAddress()

    mail_msg = "<a href={}>HTML Address: {}</a>".format(ip, ip)

    message = MIMEText(mail_msg, 'html', 'utf-8')
    message['From'] = Header("raspberry", 'utf-8')  
    message['To'] =  Header("admin", 'utf-8')        
 
    subject = 'Raspiberry Pi IP address'
    message['Subject'] = Header(subject, 'utf-8')
 
    try:
        smtpObj = smtplib.SMTP(smtp_ssl_host, smtp_ssl_port)
        smtpObj.starttls() 
        smtpObj.login(username, password)
        smtpObj.sendmail(sender, receivers, message.as_string())
        smtpObj.quit()
        print("mail send success")
    except smtplib.SMTPException:
        print("Error")
