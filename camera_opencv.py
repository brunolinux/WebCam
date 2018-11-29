import cv2
import time 
import numpy as np
from base_camera import BaseCamera
from pivideoStream import PiVideoStream
from detection import Detection

detector = Detection("./model/detect.tflite", "./model/coco_labels_list.txt", 4)
img_buf = np.zeros((detector.height(),detector.width(), 3), dtype=np.uint8)


class Camera(BaseCamera):   
    piCam = PiVideoStream(resolution=(640, 480))
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
            if img.shape[0] != 480 and img.shape[1] != 640: 
                continue

            img_buf = cv2.resize(img, (300, 300))
            detector.frameDetect(img_buf)
            #print("OK")
            out = detector.output()
            #print("OK1")
            for n in range(out.numbers): 
                ymin = max(int(out.locations[4 * n] * img.shape[0]), 0);
                xmin = max(int(out.locations[4 * n + 1] * img.shape[1]), 0);
                ymax = min(int(out.locations[4 * n + 2] * img.shape[0]), img.shape[0]);
                xmax = min(int(out.locations[4 * n + 3] * img.shape[1]), img.shape[1]);
                cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (255, 0, 0), thickness=1);
                cv2.putText(img, out.classes[n], (xmin, ymin - 5),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0));
            # encode as a jpeg image and return it
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR);
            yield cv2.imencode('.jpg', img)[1].tobytes()


    @staticmethod
    def stopCamera():
        Camera.piCam.stop()
