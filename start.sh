source /home/pi/.virtualenvs/cv/bin/activate 
gunicorn --bind unix:webcam.sock -m 007 src:webcam
deactivate
