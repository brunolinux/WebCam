import cv2
from base_camera import BaseCamera

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)


class Camera(BaseCamera):
    @staticmethod
    def frames():
        cap = cv2.VideoCapture()
        cap.set(cv2.CAP_PROP_FRAME_WIDTH,640);
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480);
        cap.open(0)
        while True:
            err,img = cap.read()
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


            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()



