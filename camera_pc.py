#!/usr/bin/env python
import cv2
from base_camera import BaseCamera


class Camera(BaseCamera):
    video_source = 0
    stop = True 

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')
        
        Camera.stop = False
        while True:
            if Camera.stop == True:
                break
            # read current frame
            _, img = camera.read()

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()
       
    @staticmethod
    def stopCamera():
        Camera.stop = True
