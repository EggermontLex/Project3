# Code adapted from Tensorflow Object Detection Framework
# https://github.com/tensorflow/models/blob/master/research/object_detection/object_detection_tutorial.ipynb
# Tensorflow Object Detection Detector

from collections import deque
from pyimagesearch.centroidtracker import CentroidTracker
import numpy as np
import cv2
from detectorapi import DetectorAPI


if __name__ == "__main__":
    model_path = 'ssd_mobilenet_v2_coco/frozen_inference_graph.pb'
    odapi = DetectorAPI(path_to_ckpt=model_path)
    threshold = 0.7
    hysterese = 10
    width, height = 1280, 720
    line1 = height/2
    ct = CentroidTracker()
    cap = cv2.VideoCapture(0)
    line_trail = dict()
    line_order = dict()
    persons_in = 0
    path = ('test.avi')
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    video_writer = cv2.VideoWriter(path, fourcc, 20.0, (1280, 720))

    while True:
        _, img = cap.read()
        img = cv2.resize(img, (width, height))
        rects = []
        boxes, scores, classes, num = odapi.process_frame(img)

        for i in range(len(boxes)):
            # Class 1 represents human
            if classes[i] == 1 and scores[i] > threshold:
                box = boxes[i]
                cv2.rectangle(img, (box[1], box[0]), (box[3], box[2]), (0, 255, 0), 5)
                cv2.putText(img, '{0:.2f}'.format(scores[i]), (box[1], box[0]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 4)
                rects.append(np.array(box))

        objects = ct.update(rects)
        print(objects.items())

        for (objectID, centroid) in objects.items():
            print(centroid)
            line_order[objectID] = deque(maxlen=2)
            if objectID not in line_trail.keys():
                line_trail[objectID] = deque(maxlen=32)
            text = "ID {}".format(objectID)
            cv2.putText(img, text, (centroid[1] - 10, centroid[0] - 10),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 4)
            cv2.circle(img, (centroid[1], centroid[0]), 4, (0, 255, 0), -1)
            cv2.line(img, (0, centroid[2]), (width, centroid[2]), (255, 0, 0), 2)
            center = (centroid[1], centroid[2])
            line_trail[objectID].appendleft(center)
            try:
                if line_trail[objectID][0][1] < int(line1) and line_trail[objectID][1][1] > int(line1 ):
                    persons_in -= 1
                elif line_trail[objectID][1][1] < int(line1) and line_trail[objectID][0][1] > int(line1 ):
                    persons_in += 1
            except Exception as Ex:
                pass

            #drawing line
            #for i in np.arange(1, len(line_trail[objectID])):
            #    if line_trail[objectID][i - 1] is None or line_trail[objectID][i] is None:
            #        continue
            #    cv2.line(img, line_trail[objectID][i - 1], line_trail[objectID][i], (0, 0, 255), 2)




            #if centroid[0] <= int(line1): print("Voorzone 1 ", end="")
            #elif centroid[0] > int(line1) and centroid[0] < int(line2): print("Center",end="")
            #elif centroid[0] >= int(line2): print("Voorzone 2 ",end="")
            #print(centroid[0])

        cv2.line(img, (0, int(line1)), (width, int(line1)), (255, 0, 0), 5)
        #cv2.line(img, (0, int(line1+hysterese)), (width, int(line1+hysterese)), (255, 0, 0), 2)
        #cv2.line(img, (0, int(line1 - hysterese)), (width, int(line1 -hysterese)), (255, 0, 0), 2)
        cv2.putText(img, "Binnen: " + str(persons_in), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA)
        print(persons_in)
        video_writer.write(img)
        cv2.imshow("preview", img)


        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break

