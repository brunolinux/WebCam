import cv2
import time 
from base_camera import BaseCamera
from pivideoStream import PiVideoStream
from detection import Detection

detector = Detection("./model/detect.tflite", "./model/coco_labels_list.txt")


class Camera(BaseCamera):   
    piCam = PiVideoStream(resolution=(640, 480))

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
            #print(img.shape)
            print("OK")
            img_1 = cv2.resize(img, (300, 300))
            print("OK1")
            out = detector.frameDetect(img_1)
            print("OK2")
            for n in range(out.numbers): 
                ymin = int(out.locations[4 * n] * img.shape[0]);
                xmin = int(out.locations[4 * n + 1] * img.shape[1]);
                ymax = int(out.locations[4 * n + 2] * img.shape[0]);
                xmax = int(out.locations[4 * n + 3] * img.shape[1]);
                cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (255, 0, 0), thickness=1);
                cv2.putText(img, out.classes[n], (xmin, ymin - 5),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0));
            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()


    @staticmethod
    def stopCamera():
        Camera.piCam.stop()
