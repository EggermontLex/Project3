#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import

from timeit import time
import warnings
import cv2
import numpy as np
#from yolo import YOLO

from collections import deque
from deep_sort import preprocessing
from deep_sort import nn_matching
from deep_sort.detection import Detection
from deep_sort.tracker import Tracker
from tools import generate_detections as gdet

warnings.filterwarnings('ignore')


from ssd_mobilenet_v2_coco.detectorapi import DetectorAPI


#threshold = 0.7
def start(model_name):

   # Definition of the parameters
    max_cosine_distance = 0.3
    nn_budget = None
    nms_max_overlap = 1.0
    
   # deep_sort 
    model_filename = 'model_data/mars-small128.pb'
    encoder = gdet.create_box_encoder(model_filename,batch_size=1)
    
    metric = nn_matching.NearestNeighborDistanceMetric("cosine", max_cosine_distance, nn_budget)
    tracker = Tracker(metric)

    writeVideo_flag = True 
    
    video_capture = cv2.VideoCapture(0)

    if writeVideo_flag:
    # Define the codec and create VideoWriter object
        w = int(video_capture.get(3))
        h = int(video_capture.get(4))
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        out = cv2.VideoWriter('output.avi', fourcc, 15, (w, h))
        list_file = open('detection.txt', 'w')
        frame_index = -1


    #model_yolo = YOLO()
    model_path = 'ssd_mobilenet_v2_coco/frozen_inference_graph.pb'
    model_coco = DetectorAPI(path_to_ckpt=model_path)



    fps = 0.0
    persons_in = 0
    while True:
        ret, frame = video_capture.read()  # frame shape 640*480*3
        height, width = frame.shape[:2]
        line1 = int(height /2)
        if ret != True:
            break
        t1 = time.time()
        cv2.line(frame, (0, line1), (width, line1), (255, 0, 0), 5)

        #if model_name == "Yolo":
        #    image = Image.fromarray(frame)
        #    image = Image.fromarray(frame[..., ::-1])  # bgr to rgb
        #    boxs = model_yolo.detect_image(image)
        #else:
        boxs = []
        boxes, scores, classes, num = model_coco.process_frame(frame)
        for box in boxes:
            if not box == (0,0,0,0):
                boxs.append((box[1],box[0],int(box[3]),int(box[2])))

        print(boxs)
        features = encoder(frame,boxs)
        
        # score to 1.0 here).
        detections = [Detection(bbox, 1.0, feature) for bbox, feature in zip(boxs, features)]
        
        # Run non-maxima suppression.
        boxes = np.array([d.tlwh for d in detections])
        scores = np.array([d.confidence for d in detections])
        indices = preprocessing.non_max_suppression(boxes, nms_max_overlap, scores)
        detections = [detections[i] for i in [preprocessing.non_max_suppression(boxes, nms_max_overlap, scores)]]

        #or this fancy oneliner :)
        #detections = [detections[i] for i in [preprocessing.non_max_suppression([np.array([d.tlwh for d in [Detection(bbox, 1.0, feature) for bbox, feature in zip(boxs, features)]])], nms_max_overlap, [np.array([d.confidence for d in [Detection(bbox, 1.0, feature) for bbox, feature in zip(boxs, features)]])])]]
        
        # Call the tracker
        tracker.predict()
        tracker.update(detections)
        
        for track in tracker.tracks:
            if not track.is_confirmed() or track.time_since_update > 1:
                continue
            if track.track_id not in line_trail.keys():
                line_trail[track.track_id] = deque(maxlen=2)
            bbox = track.to_tlbr()
            cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])),(255,255,255), 2)
            cv2.putText(frame, str(track.track_id),(int(bbox[0]), int(bbox[1])),0, 5e-3 * 200, (0,255,0),2)
            cv2.line(frame, (0, int(bbox[1])), (width, int(bbox[1])), (255, 0, 0), 2)


            line_trail[track.track_id].appendleft(bbox[1])
            try:
                if line_trail[track.track_id][0] < int(line1) and line_trail[track.track_id][1] > int(line1 ):
                    persons_in -= 1
                elif line_trail[track.track_id][1] < int(line1) and line_trail[track.track_id][0] > int(line1 ):
                    persons_in += 1
            except Exception as Ex:
                pass

        #for det in detections:
        #    bbox = det.to_tlbr()
        #    cv2.rectangle(frame,(int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])),(255,0,0), 2)
        cv2.putText(frame, "Binnen: " + str(persons_in), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA)
        cv2.putText(frame, "fps: " + str(int(fps)), (260, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA)
        cv2.putText(frame, "Clasifier: " + str(model_name), (410, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), lineType=cv2.LINE_AA)
        cv2.imshow('', frame)
        
        if writeVideo_flag:
            # save a frame
            out.write(frame)
            frame_index += 1
            list_file.write(str(frame_index)+' ')
            if len(boxs) != 0:
                for i in range(0,len(boxs)):
                    list_file.write(str(boxs[i][0]) + ' '+str(boxs[i][1]) + ' '+str(boxs[i][2]) + ' '+str(boxs[i][3]) + ' ')
            list_file.write('\n')
            
        fps  = ( fps + (1./(time.time()-t1)) ) / 2

        user_input = cv2.waitKey(1)
        if user_input == ord('q'):
            break
        elif user_input == ord('y'):
            model_name = "Yolo"
        elif user_input == ord('c'):
            model_name = "Coco"

    video_capture.release()
    if writeVideo_flag:
        out.release()
        list_file.close()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    line_trail = dict()
    start("Yolo")
    #start("")