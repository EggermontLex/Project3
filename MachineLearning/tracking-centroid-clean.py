from edgetpu.detection.engine import DetectionEngine
from PIL import Image
from timeit import time
from PIL import ImageDraw
import numpy as np
import cv2
import warnings
from google.cloud import pubsub_v1
import os
import datetime
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/mendel/project3/Project3-ML6-515024366790.json"
data = ""
f= open("cache.txt","w+")


from pyimagesearch.centroidtracker import CentroidTracker
from collections import deque
from deep_sort import preprocessing
from deep_sort import nn_matching
from deep_sort.detection import Detection
from deep_sort.tracker import Tracker
#from tools import generate_detections as gdet
from deep_sort.detection import Detection as ddet
warnings.filterwarnings('ignore')


project_id = "Project3-ML6"
topic_name = "data_register"
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_name)


# Function to read labels from text files.
def ReadLabelFile(file_path):
    with open(file_path, 'r', encoding="utf-8") as f:
        lines = f.readlines()
    ret = {}
    for line in lines:
        pair = line.strip().split(maxsplit=1)
        ret[int(pair[0])] = pair[1].strip()
    return ret


def main():
    #google cloud variables

    max_cosine_distance = 0.3
    nn_budget = None
    nms_max_overlap = 1.0
    fps = 0.0
    persons_in = 0
    line_trail = dict()

    # Initialize engine.
    engine = DetectionEngine('model_tflite/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite')
    labels = ReadLabelFile('model_tflite/coco_labels.txt')

    #deep sort
    metric = nn_matching.NearestNeighborDistanceMetric("cosine", max_cosine_distance, nn_budget)
    tracker = Tracker(metric)

    #centroid tracker
    ct = CentroidTracker()
    cap = cv2.VideoCapture(1)
    invert = True

    while True:
        data = ""
        ret, frame = cap.read()
        if ret:

            cv2_im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2_im)
            width, height = img.size
            line1 = height/2 - 50
            draw = ImageDraw.Draw(img)

            # Run inference.
            ans = engine.DetectWithImage(img, threshold=0.5, keep_aspect_ratio=True, relative_coord=False, top_k=10)
            boxs =[]
            # Display result.

            #reformat boxes
            [boxs.append(obj.bounding_box.flatten().tolist()) for obj in ans] if ans else None
            objects = ct.update(boxs)

            img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

            for (objectID, centroid) in objects.items():
                if objectID not in line_trail.keys(): line_trail[objectID] = deque(maxlen=2)
                text = "ID {}".format(objectID)
                center = (centroid[1], centroid[2])
                line_trail[objectID].appendleft(center)
                try:
                    diff = abs(line_trail[objectID][0][0] - line_trail[objectID][1][0])
                    print(diff)
                    if diff < 250:
                        if line_trail[objectID][0][1] < int(line1) and line_trail[objectID][1][1] > int(line1):
                            binnen() if invert else buiten()
                        elif line_trail[objectID][1][1] < int(line1) and line_trail[objectID][0][1] > int(line1):
                            buiten() if invert else binnen()

                except Exception as Ex:
                    pass

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

def callback(message_future):
    # When timeout is unspecified, the exception method waits indefinitely.
    if message_future.exception(timeout=30):
        print('Publishing message on {} threw an Exception {}.'.format(
            topic_name, message_future.exception()))
        f.write(data + ",")
    else:
        print("Confirmation: " + message_future.result())
        lines = [send_message(line) for line in [line.rstrip(',') for line in open('cache.txt')]]

def send_message(data):
    message_future = publisher.publish(topic_path, data=data)
    message_future.add_done_callback(callback)


def binnen():
    data = ("+1,%s" % datetime.datetime.now())
    data = data.encode('utf-8')
    message_future = publisher.publish(topic_path, data=data)
    message_future.add_done_callback(callback)
    print("in")

def buiten():
    data = ("-1,%s" % datetime.datetime.now())
    data = data.encode('utf-8')
    message_future = publisher.publish(topic_path, data=data)
    message_future.add_done_callback(callback)
    print("out")


if __name__ == '__main__':
    main()
