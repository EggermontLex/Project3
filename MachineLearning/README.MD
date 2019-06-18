# Machine Learning
In this README we will have a closer look on how this code works, this will be done by going over the code step by step. 

## Inhoudstafel

## Python packages
**Edgetpu:** pre-installed computervision library created by google.

**Argparse**: `pip install argparse` this library is used to create parameters that can be given to a certain python script, why this could be helpfull we will discuss later.

**Pillow**: `pip install Pillow` a library for image editing/processing, we use this library to draw lines, boxes, etc on the video.

**Numpy**: `pip install numpy` a well known library used to perform any operations surrounding arrays.

**Requests**: `pip install requests` this library is mainly used for doing web related things, such as requesting the page and creating web requests. However we only need this library to check if there is internet connectivity.

**Google cloud**: `pip install google-cloud` another library created by google itself, this library is used to communicate with google cloud. In this case we only need it to communicate with the publisher of google pubsub.

**OpenCV**: sadly you have to build this library from source, you can find how you do this online.


## The code
First things first, we will need to start by analyzing the code in the `CentroidTracking.py` since this is the heart of our project, next we will have a closer look in certain 'tools' we used, these tools are the self written class `CloudManager` and the imported class `CentroidTracking`

### `CentroidTracking.py`
#### Imports
Like every python program ever, we first need to import our essential libraries, without these it would not be possible to run our code.
```
from edgetpu.detection.engine import DetectionEngine
import argparse
from PIL import Image
from timeit import time
from PIL import ImageDraw
import numpy as np
import cv2
import warnings
import os
import datetime
from tools.centroidtracker import CentroidTracker
from collections import deque
from tools.cloud_manager import CloudManager
```

#### `if __name__ = '__main__':`
As cited before, we added the possiblity for users to give extra parameters to the code, with this the user can change some basic things in the code which might better match it to theire needs. This makes it easier for users of our program to get the best out of it without having to change any actual code. beneeth we have our `flags`

`--invert` this flag is used to inver the order in which the program tracks, for example, if the flag is `True` it might be In-->Out if you run one way, however if the flag was `False` in that case it would have been Out-->In. Default this is set to `False`.

`--resample` with this flag you can configure the resampling, by default this is configured on NEAREST, however you could also use BICUBIC. BICUBIC will improve the accuracy and decrease the performance of the program.

`--fps` if this would be `True` the user will see the framerate in the command output. Default this is set to `False`.

`--video` this is an important flag, this one will turn the video output on or off. If this is `True` it wil have a video saved to a videofile and a live visual in case you connect a screen. Default this is set to `False`.

As final flag we have `--threshold`, this one will change the minimum allowed accuracy to be clasified as a person (as float). Default this one is set to 0.65

```
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--invert', type=bool, default=True, help='binnen <-> buiten --> buiten <-> binnen')
    parser.add_argument('--resample', type=str, default="NEAREST", help='what form of image detection you want, NEAREST or BICUBIC')
    parser.add_argument('--fps', type=bool, default=False, help='Print fps counter')
    parser.add_argument('--video', type=bool, default=False,help='Do you want to display and save video from the actions going on in the backgroud')
    parser.add_argument('--threshold', type=int, default=0.65,help='minimum allowed value for the threshold')
    options = parser.parse_args()
    main(options)
```
### Creating variables
In order to handle the values of people comming in and going out, we have to establish a connection with the cloud. The code beneath initialises the `CloudManager`, as mentioned before, this is a self written class that will communicate with the cloud and has a basic implementation of **offline caching**

Keep in mind that you will have to change the `project_id` and `topic_name` to the once you use for your project, since this example uses the once we used for our project.
```
project_id = "Project3-ML6"
topic_name = "data_register"
publisher = CloudManager(project_id,topic_name)
```
As cited before, we used flags to give the user of the script more personalisation possiblilities, with the following code you can see how we retrieved the value out of the argparser. **Be aware**: we used environment variables during our deployment to get our devicename. This because we wanted to automate deployment, feel free to hardcode a devicename if you dont need this.
```
device = str(os.environ['device_id'])
flag_invert = options.invert
flag_video = options.video
flag_fps = options.fps
```

The next bit of code is probably the least importand part of our code, this just creates some basic variables we use throughout the program.
```
t1 =0.0
fps = 0.0
persons_in = 0
line_trail = dict()
```
Though the initialisation of the `DetectionEngine` is way more important, this engine requires a converted tensorflow light model in order to function on the TPU (tensorflow processing unit). How you can convert the moddel is wel documented, I suggest you visit the tensorflow [site](https://www.tensorflow.org/lite). The model we used is a pre build online available model, called `mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite`. This model is capable of detecting over 90 diffrent objects, although we only need to detect humans, its also fun to play around with. Some interesting fact about this model is that it can detect humans by only showing it a foot or a hand, because this is possible, we can conlude that they had a very balanced training dataset when the created the model.
```
engine = DetectionEngine('model_tflite/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite')
```
We have experimented quite a lot with diffrent tracking software, we have used(CentroidTracking, cv2.Mossy, iou tracking and deepsort). By testing all these trackers we have concluded that CentroidTracker is the best tracker for our project, since it is the most light weight one that doesnt freeze up the google devboard when it detects something. However if processing power isnt the problem, I would suggest that you use the deep sort. This is one of the most accurate trackers you can implement, since this tracker was so good, i have left a `tracking-deep-sort.py` in this repository so you can also test it. However we cant use it on the google coral devboard since our framerate drops to 2-5 when there is only 1 person that has to be tracked.

```
ct = CentroidTracker()
```
The code beneath is one of the many times when check if the `--video` flag is `True` and if that is the case we excecute the required code to create a videofile. Here we will get the width and height followed by initializing what type of videoformat you want, once you have don this tiny pre setup you want to create the videofile itself.
```
if flag_video:
    w = int(cap.get(3))
    h = int(cap.get(4))
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    video = cv2.VideoWriter('output.avi', fourcc, 15, (w, h))
```
### `while true:`

At last we have ended up in the core of the code, here we process and edit the retrieved live images. Ever time we loop we get a new image from the webcam, this is achieved by running the next code `ret, frame = cap.read()` in `ret` will represent if the frame was succesfully captured, if this isnt the case you can easily catch this by doing `if ret:`. The next step is decoding the frame from BGR , which is the opencv default, to RGB, which is the Pillow default. We need this because the `DetectionEngine` requires the `Frame` in RGB color encoding. Also you need to decode the image into an array like this `img = Image.fromarray(cv2_im)` no we can easily extract the widht and height like this `width, height = img.size`. Now the penultimate step is to create the variable that declares the seperation between in and out `line1 = height/2 - 50`. Last, we create a drawable object using PIL like this `draw = ImageDraw.Draw(img)` so we can draw boxes and lines.

##### Object detection
Now it is time to let the object tracking lose on the `frame`, this happens with a simple line of code
Nu is het tijd om de object detection los te laten gaan op de frame, dit gebeurd aan de hand van deze simpele lijn code:
```
ans = engine.DetectWithImage(img, threshold=options.threshold, keep_aspect_ratio=True, relative_coord=False, top_k=10,resample=Image.NEAREST) #BICUBIC
```

Here the parameter `threshold` is the minimum allowed value that is allowed for the detections to be shown, `keep_aspect_ratio` is always `True`, since this could drasticly decrease the accuracy of the detections, since this could cause the image to compress into a wrong format (which is obviously not representative with the reality), `relative_coord` is when you want to keep the coordinates of your pixels in the same place, just like the previous parameter this one is always on `True` so it doesnt decrease the detection accuracy. 
Another parameter is `top_k` which I decided to keep on 10, since this will search for 10 detections in this case. making this a greate number will increase the latency required to do the object detection, lowering this number will lower the latency and the amount of possible tracked objects. Which in that case might not be the best of idea's since there could be more actual objects in the `frame`.
The last parameter, `resample` is quite important in case the image is rescaled before processing, using `NEAREST` will increase your performance (22fps) and using `BICUBIC` will slightly increase the detection accuracy however the framrate will decrease (12fps).

Up next we will reformat the `ans` object to a more ussable format where we can just send it to the tracker, in order to do this we just have a simple for loop which gets all the detections and draws the detection box if the  `--vidieo` flag equel is to`True`.
```
if ans:
    for obj in ans:
        box = obj.bounding_box.flatten().tolist()
        if flag_video: draw.rectangle(box, outline='red')
        boxs.append(box)
```
##### Object tracking

The converted list of detections will be passed along to the Centroid Tracker with the following line of code `objects = ct.update(boxs)`, this tracker will determine which detection in the current `frame` is the same detected object in the previous `frame`. As mentioned before this isnt the most accurate tracker however it has great performance. 

Next we will loop over all the objects one by one and handle if they left or entered the building by passing the seperation line.
```
for (objectID, centroid) in objects.items():
    #line_order[objectID] = deque(maxlen=2)
    if objectID not in line_trail.keys():
        line_trail[objectID] = deque(maxlen=2)
    if flag_video:
        text = "ID {}".format(objectID)
        cv2.putText(img, text, (centroid[0] - 10, centroid[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255),4)
        cv2.circle(img, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
        cv2.line(img, (0, centroid[2]), (width, centroid[2]), (255, 0, 0), 2)
    center = (centroid[1], centroid[2])
    line_trail[objectID].appendleft(center)
    try:
        diff = abs(line_trail[objectID][0][0] - line_trail[objectID][1][0])
        if diff < 60:
            if line_trail[objectID][0][1] < int(line1) and line_trail[objectID][1][1] > int(line1):
                if flag_invert:
                    persons_in += 1
                    publisher.publish_to_topic(data = ("+1,%s,%s" % (datetime.datetime.now(),device)))
                else:
                    persons_in -= 1
                    publisher.publish_to_topic(data = ("-1,%s,%s" % (datetime.datetime.now(),device)))
            elif line_trail[objectID][1][1] < int(line1) and line_trail[objectID][0][1] > int(line1):
                if flag_invert:
                    publisher.publish_to_topic(data = ("-1,%s,%s" % (datetime.datetime.now(),device)))
                    persons_in -= 1
                else:
                    publisher.publish_to_topic(data = ("+1,%s,%s" % (datetime.datetime.now(),device)))
                    persons_in += 1
    except Exception as Ex: #deque not long eneough error, niet nodig om op te vangen
        pass
```
The variable `line_trail` contains the previous locoation of the centroid of the previous object location, this is saved so we can check if the object has crossed the line, again there is a `--video` flag which in this case will show the object id in the centre of the object bounding box and a line that clearifies the top of the bounding box. Also I added in a error correction, where I simply maximize the diffrence between two points `diff = abs(line_trail[objectID][0][0] - line_trail[objectID][1][0])` so it doesnt misfire its object tracking when it misdetects on an other object that might be at the other side of the box. After we have checked that, there is one more check we have to do, which is to verify if the previous centroid was at the other side of the line. If this was the case, The code jst checks which direction the object went and sends the confirmation to the `CloudManager` as followed `publisher.publish_to_topic(data = ("+1,%s,%s" % (datetime.datetime.now(),device)))`

Previous to last, we have 2 more flags, the `--fps` and `--video`, at this point i dont think this needs any explenation anymore.
```
if flag_fps: print("fps : %d" % ((fps + (1. / (time.time() - t1))) / 2))
if flag_video:
    cv2.putText(img, "Binnen: " + str(persons_in), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255),lineType=cv2.LINE_AA)
    cv2.putText(img, "fps: " + str(int(fps)), (260, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255),lineType=cv2.LINE_AA)
    video.write(img)
    cv2.imshow('preview', img)
```

When you quit the code there will always have to be a `cap.release()` just so the webcam is available to other services again

### CloudManager

The CloudManager class is located in the tools folder, this class is quite important for the cloud communication. For example, if our project doesn't have internt connectivity, this class will automaticly store it in the local cache. Once there is a request which was succesfully handeld, the cached data will automaticly be uploaded. For further information you can have a look in the `CloudManager.py` class itself, since I tried to document quite well.
