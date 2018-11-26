## Tensorflow Lite on Raspberry Pi 

This article describe how to use the object detection model based on the tensorflow lite and opencv ( C++ version )

### 1. OpenCV Native Compilation 

Reference: [Install Opencv 4 on your Raspberry Pi](https://www.pyimagesearch.com/2018/09/26/install-opencv-4-on-your-raspberry-pi/) 

Note: For the consideration of stability, here we use the 3.4.3 version. But the procedure of compilation is same.  

You can make sure whether the compilation is successful by following code 

```shell
$ workon cv  # virtualenv: cv
$ python 
Python 2.7.13 (default, Sep 26 2018, 18:42:22) 
[GCC 6.3.0 20170516] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import cv2
>>> cv2.__version__ 
'3.4.3'
```



### 2. Tensorflow Lite nativa compilation 

Reference: [TensorFlow Lite for Raspberry Pi](https://www.tensorflow.org/lite/rpi) 

Note: Because the tensorflow lite is not stable yet, we found a bug in the file `<root dir of tensorflow code>/tensorflow/lite/tools/make/Makefile` : 

In my board

Below is the modified code: 

```makefile
CORE_CC_ALL_SRCS := \
$(wildcard tensorflow/lite/*.cc) \
$(wildcard tensorflow/lite/*.c) \
$(wildcard tensorflow/lite/c/*.c) \
$(wildcard tensorflow/lite/core/*.cc) \
$(wildcard tensorflow/lite/core/api/*.cc)
```

The developer ignores one line: `$(wildcard tensorflow/lite/core/*.cc) \` , so just add it. 

The just follow the step of **native compiling**  of the above article. 

If the compilation succeeds,  you can find the static library `libtensorflow-lite.a` in the directory `<root dir of tensorflow code>/tensorflow/lite/tools/make/gen/rpi_armv7l/lib/libtensorflow-lite.a`

Note: 

1. If you have more interests, you can also test the binary file `label_image` and `benchmark_model` on the raspberry pi board.  
2. I have tried to compile the runtime python library of tensorflow lite. But there is still many bugs by present. So I decided to test firstly the C++ version of tensorflow lite. 

### 3. Native compile of the code

On the raspberry board, you should create a directory and copy all file of the directory `<top dir>/test/tf_lite` in my repo to this. 

Then execute the command below. 

``` shell
$ gcc -O3 -DNDEBUG --std=c++11 object_detection.cc libtensorflow-lite.a -ldl -lutil -lstdc++ -lpthread -lm -lz -lopencv_core -lopencv_imgcodecs -lopencv_imgproc -I/home/pi/tensorflow -I/home/pi/tensorflow/tensorflow/lite/tools/make/downloads/flatbuffers/include -o ssd_detection
```

If there is no problem, you will find a binary file `ssd_detection` 

Then just run it 

```shell
$ .\ssd_detection
```

You will find a image named `posttest.bmp` . That's what we need. Just copy it to our PC and open it. 

Tout parfait !!!





