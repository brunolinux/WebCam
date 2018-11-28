#source /home/pi/.virtualenvs/cv/bin/activate
workon cv 
gunicorn --bind localhost:8000 src:webcam
deactivate
