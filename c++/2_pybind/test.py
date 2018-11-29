import detection
import cv2 

detector = detection.Detection("../../model/detect.tflite", "../../model/coco_labels_list.txt", 1)

img = cv2.imread("../test.bmp")

img_1 = cv2.resize(img, (300, 300))
img_1 = cv2.cvtColor(img_1, cv2.COLOR_BGR2RGB)

for i in range(200):
    detector.frameDetect(img_1)
    out = detector.output();
    print("Finished: ", i)

for n in range(out.numbers): 
    ymin = int(out.locations[4 * n] * img.shape[0]);
    xmin = int(out.locations[4 * n + 1] * img.shape[1]);
    ymax = int(out.locations[4 * n + 2] * img.shape[0]);
    xmax = int(out.locations[4 * n + 3] * img.shape[1]);
    cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (255, 0, 0), thickness=1);
    cv2.putText(img, out.classes[n], (xmin, ymin - 5),
                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0));

cv2.imwrite("posttest.bmp", img)
