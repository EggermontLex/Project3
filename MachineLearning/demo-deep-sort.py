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



from pyimagesearch.centroidtracker import CentroidTracker
from collections import deque
from deep_sort import preprocessing
from deep_sort import nn_matching
from deep_sort.detection import Detection
from deep_sort.tracker import Tracker
from tools import generate_detections as gdet
from deep_sort.detection import Detection as ddet
warnings.filterwarnings('ignore')


project_id = "Project3-ML6"
topic_name = "telemetry-topic"
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
    engine = DetectionEngine('mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite')
    labels = ReadLabelFile('coco_labels.txt')

    #deep sort
    model_filename = 'model_data/mars-small128.pb'
    encoder = gdet.create_box_encoder(model_filename,batch_size=1)

    metric = nn_matching.NearestNeighborDistanceMetric("cosine", max_cosine_distance, nn_budget)
    tracker = Tracker(metric)

    cap = cv2.VideoCapture(1)

    writeVideo_flag = False
    if writeVideo_flag:
    # Define the codec and create VideoWriter object
        w = int(cap.get(3))
        h = int(cap.get(4))
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        out = cv2.VideoWriter('output.avi', fourcc, 15, (w, h))
        list_file = open('detection.txt', 'w')
        frame_index = -1
    # Open video


    invert = True

    while True:
        data = ""
        ret, frame = cap.read()
        t1 = time.time()
        if ret:

            cv2_im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2_im)
            width, height = img.size
            line1 = height/2 - 100
            draw = ImageDraw.Draw(img)

            # Run inference.
            ans = engine.DetectWithImage(img, threshold=0.5, keep_aspect_ratio=True, relative_coord=False, top_k=10)
            boxs =[]
            # Display result.
            if ans:
                for obj in ans:
                    #if labels: print(labels[obj.label_id])
                    box = obj.bounding_box.flatten().tolist()
                    # Draw a rectangle.
                    draw.rectangle(box, outline='red')
                    #draw.text((box[0], box[1]), labels[obj.label_id])
                    #draw.text((box[0], box[1] + 10), str(obj.score))
                    boxs.append(box)

            objects = ct.update(boxs)

            draw.line((0, line1, width, line1), fill=10, width=5)
            img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

            for (objectID, centroid) in objects.items():
                #line_order[objectID] = deque(maxlen=2)
                if objectID not in line_trail.keys():
                    line_trail[objectID] = deque(maxlen=32)
                text = "ID {}".format(objectID)
                cv2.putText(img, text, (centroid[0] - 10, centroid[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255),4)
                cv2.circle(img, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
                cv2.line(img, (0, centroid[2]), (width, centroid[2]), (255, 0, 0), 2)
                center = (centroid[1], centroid[2])
                line_trail[objectID].appendleft(center)
                try:
                    if line_trail[objectID][0][1] < int(line1) and line_trail[objectID][1][1] > int(line1):
                        if invert:
                            persons_in += 1
                            #binnen()
                        else:
                            persons_in -= 1
                            #buiten()
                    elif line_trail[objectID][1][1] < int(line1) and line_trail[objectID][0][1] > int(line1):
                        if invert:
                            #buiten()
                            persons_in -= 1
                        else:
                            #binnen()
                            persons_in += 1
                except Exception as Ex:
                    pass

            fps = (fps + (1. / (time.time() - t1))) / 2
            cv2.putText(img, "Binnen: " + str(persons_in), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255),
                        lineType=cv2.LINE_AA)
            cv2.putText(img, "fps: " + str(int(fps)), (260, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255),
                        lineType=cv2.LINE_AA)

            if writeVideo_flag:
                # save a frame
                out.write(img)


            cv2.imshow('preview', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


def binnen():
    data = ("+1,%s" % datetime.datetime.now())
    data = data.encode('utf-8')
    publisher.publish(topic_path, data=data)
    print("in")

def buiten():
    data = ("-1,%s" % datetime.datetime.now())
    data = data.encode('utf-8')
    publisher.publish(topic_path, data=data)
    print("out")


if __name__ == '__main__':
    main()
