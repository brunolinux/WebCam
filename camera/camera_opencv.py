#!/usr/bin/python
# -*- coding: UTF-8 -*-

from . import cv2
import time 
import numpy as np
import pickle as pkl
import random
from .base_camera import BaseCamera
from .pivideoStream import PiVideoStream
from .detection import Detection, OutputInfo

detector = Detection("./camera/model/detect.tflite", "./camera/model/coco_labels_list.txt", 4)
img_buf = np.zeros((detector.height(),detector.width(), 3), dtype=np.uint8)

out = OutputInfo()
colors = pkl.load(open("./camera/pallete", "rb"))


class Camera(BaseCamera):   
    _resolution = (640, 480)
    piCam = PiVideoStream(resolution=_resolution)
    startup_frame = 0 

    @staticmethod
    def frames():
        try:
            # start a thread to read continously read the camera 
            Camera.piCam.start()
        except: 
            print("Error! Can not read frames from the PiCamera!")  
            return    
      
        # let camera warm up
        time.sleep(2)
        while True:            
            # always take the first image
            img = Camera.piCam.read()
            if img.shape[0] != Camera._resolution[1] or img.shape[1] != Camera._resolution[0]: 
                continue

            img_buf = cv2.resize(img, (300, 300))
            detector.frameDetect(img_buf, out)
            #print("OK")
            for n in range(out.numbers): 
                ymin = max(int(out.locations[4 * n] * img.shape[0]), 0);
                xmin = max(int(out.locations[4 * n + 1] * img.shape[1]), 0);
                ymax = min(int(out.locations[4 * n + 2] * img.shape[0]), img.shape[0]);
                xmax = min(int(out.locations[4 * n + 3] * img.shape[1]), img.shape[1]);
                color = random.choice(colors)
                cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color, thickness=1);
                cv2.putText(img, out.classes[n], (xmin, ymin + 12),
                            cv2.FONT_HERSHEY_PLAIN, 1, (225, 255, 255));
            # encode as a jpeg image and return it
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR);
            yield cv2.imencode('.jpg', img)[1].tobytes()


    @staticmethod
    def stopCamera():
        Camera.piCam.stop()


    @staticmethod
    def setCamera(para):
        Camera.piCam.brightness = para["brightness"]
        Camera.piCam.contrast = para["contrast"]
        Camera.piCam.saturation = para["saturation"] 
        Camera.piCam.awb_mode = para["awb_mode"]
        Camera.piCam.exposure_mode = para["exposure_mode"] 

        #width, height = para["resolution"].split('x')
        #Camera._resolution = (int(width), int(height)) 
        #Camera.piCam.resolution = Camera._resolution
        #print(Camera.piCam.awb_mode)
