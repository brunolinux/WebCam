## WebCam for Raspberry pi 

This repo is a web camera app with object dection based on raspberry pi 

**Software Stack**: Flask + Tensorflow lite + OpenCV 

**Hardware requirement**: 

- respberry pi 3b 
- picamera module 



## 1. How to run 

### 1.1 create virtual environment

```shell
$ cd ~
$ virtualenv env_webcam --python=python3 
$ source env_webcam/bin/activate
```

### 1.2 clone the repo and install required libraries

```shell
(env_webcam) $ cd ~
(env_webcam) $ git clone https://github.com/brunolinux/WebCam.git
(env_webcam) $ cd WebCam
(env_webcam) $ pip install -r requirements.txt
```

**Note:** If you want to run this demo on your raspberry pi board, the **opencv** library is obligatory. You can reference to the steps below. 

### 1.3 create a `.config` file  in the `<root of repo>` folder

the format is like below: 

- WEBSITE: flask port number 
- GMAIL: send raspberry pi's IP address  by mail
- ADMIN: administrator name and password

```python
[WEBSITE]
Port = portnumber

[GMAIL]
Username = your.mail@gmail.com
Password = passwd
Sender = sender.mail@gmail.com
Receivers = receivers.mail@mail.com

[ADMIN]
Username = user
Password = passwd 
```

### 1.4 OpenCV Native Compilation

Reference: [Install Opencv 4 on your Raspberry Pi](https://www.pyimagesearch.com/2018/09/26/install-opencv-4-on-your-raspberry-pi/) 

Note: For the consideration of stability, here we use the 3.4.3 version. But the procedure of compilation is same.  

You can make sure whether the compilation is successful by running the following code 



### 1.5 start up the app 

```shell
(env_webcam) $ python app.py
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:8000/ (Press CTRL+C to quit)
```

Then you can open a browser and input the ip address of your raspberry pi borad (with port `8000`). You can see the image with object detection results

Note: if you want to use the port `80`, run the script using administrator account 

```shell
$ cd ~/WebCam
$ sudo ../env_webcam/bin/python app.py
```





### 1.6 using uwsgi and supervisor to self-start after power

```shell
$ sudo apt-get install supervisor
$ cd ~/WebCam
$ sudo cp ./conf/supervisor_webcam.conf /etc/supervisor/conf.d/
```

The reboot the board. 



## 2. Compilation

### 2.1 Tensorflow Lite native compilation 

Reference: [TensorFlow Lite for Raspberry Pi](https://www.tensorflow.org/lite/rpi) 

Note: Because the tensorflow lite is not stable yet, we found a bug in the file `<root dir of tensorflow code>/tensorflow/lite/tools/make/Makefile` : 

In my board, the root directory of tensorflow source code is `/home/pi/tensorflow/` 



~~Below is the modified code:~~ 

```makefile
CORE_CC_ALL_SRCS := \
$(wildcard tensorflow/lite/*.cc) \
$(wildcard tensorflow/lite/*.c) \
$(wildcard tensorflow/lite/c/*.c) \
$(wildcard tensorflow/lite/core/*.cc) \
$(wildcard tensorflow/lite/core/api/*.cc)
```

~~The developer ignores one line: `$(wildcard tensorflow/lite/core/*.cc) \` , so just add it.~~ 

This bug has been fixed



The just follow the step of **native compiling**  of the above article. 

If the compilation succeeds,  you can find the static library `libtensorflow-lite.a` in the directory `<root dir of tensorflow code>/tensorflow/lite/tools/make/gen/rpi_armv7l/lib/libtensorflow-lite.a`. That's what we need. 

Note: 

1. If you have more interests, you can also test the binary file `label_image` and `benchmark_model` on the raspberry pi board.  
2. I have tried to compile the runtime python library of tensorflow lite. But there is still many bugs by present. So I decided to test firstly the C++ version of tensorflow lite. 