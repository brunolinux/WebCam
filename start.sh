source /home/pi/.virtualenvs/cv/bin/activate
#workon cv 
gunicorn --workers 1 --bind 127.0.0.1:8000 -m 007 src:webcam
deactivate
