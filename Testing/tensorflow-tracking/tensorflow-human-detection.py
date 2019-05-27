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
    width, height = 1280, 720
    ct = CentroidTracker()
    cap = cv2.VideoCapture(1)
    line_trail = dict()

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
                cv2.putText(img, '{0:.2f}'.format(scores[i]), (box[1], box[0]),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 4)
                rects.append(np.array(box))

        objects = ct.update(rects)

        for (objectID, centroid) in objects.items():
            if objectID not in line_trail.keys():
                line_trail[objectID] = deque(maxlen=32)
            text = "ID {}".format(objectID)
            cv2.putText(img, text, (centroid[1] - 10, centroid[0] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 4)
            cv2.circle(img, (centroid[1], centroid[0]), 4, (0, 255, 0), -1)
            center = (centroid[1], centroid[0])
            line_trail[objectID].appendleft(center)
            for i in np.arange(1, len(line_trail[objectID])):
                if line_trail[objectID][i - 1] is None or line_trail[objectID][i] is None:
                    continue
                cv2.line(img, line_trail[objectID][i - 1], line_trail[objectID][i], (0, 0, 255), 2)
            # ptslen = len(pts)
            # if ptslen > 6:
            #     print(center[0])
            #     if center[0] > int(1280 / 2):
            #         print("Onder")
            #     else:
            #         print("Boven")

        cv2.line(img, (0, int(height / 2)), (width, int(height / 2)), (255, 0, 0), 5)
        cv2.imshow("preview", img)
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break
