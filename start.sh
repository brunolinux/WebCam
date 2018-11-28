source /home/pi/.virtualenvs/cv/bin/activate 
gunicorn --workers 5 --bind unix:webcam.sock -m 007 src:app
deactivate
