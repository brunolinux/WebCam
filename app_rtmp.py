import cv2
import subprocess as sp

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

cap = cv2.VideoCapture()
cap.open("rtmp://0.0.0.0/flvplayback/myStream live=1")

ffmpeg = 'ffmpeg'
dimension = '{}x{}'.format(640, 480)
f_format = 'bgr24' # remember OpenCV uses bgr format
fps = str(cap.get(cv2.CAP_PROP_FPS))

command = [ffmpeg,
    '-y',
    '-f', 'rawvideo',
    '-vcodec','rawvideo',
    '-pix_fmt', f_format,
    '-s', dimension,
    '-i', '-',
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    '-preset', 'ultrafast',
    '-f', 'flv',
    'rtmp://a.rtmp.youtube.com/live2/w47r-svem-wyxh-2sk5']

proc = sp.Popen(command, stdin=sp.PIPE,shell=False)

while True:
    err,img = cap.read()
    if not err:
        break
    # face detection
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30))

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    proc.stdin.write(frame.tostring())

cap.release()
proc.stdin.close()
proc.stderr.close()
proc.wait()
