source /home/pi/.virtualenvs/cv/bin/activate
#workon cv 
gunicorn --workers 3 --bind unix:webcam.sock -m 007 src:webcam
deactivate
