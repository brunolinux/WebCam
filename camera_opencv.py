import cv2
from base_camera import BaseCamera
from pivideoStream import PiVideoStream

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)


class Camera(BaseCamera):   
    piCam = PiVideoStream(resolution=(640, 480))

    @staticmethod
    def frames(cls):
        try:
            # start a thread to read continously read the camera 
            cls.piCam.start()
        except: 
            print("Error! Can not read frames from the PiCamera!")  
            return          
    
        while True:
            # always take the first image
            img = piCam.read()
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

    @staticmethod
    def stopCamera(cls):
        cls.piCam.stop()
