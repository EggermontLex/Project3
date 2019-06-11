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
from tools.util import load_mot, iou
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



from tools import generate_detections as gdet


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
    max_cosine_distance = 1
    nn_budget = None
    nms_max_overlap = 1.0
    fps = 0.0
    persons_in = 0
    line_trail = dict()

    # Initialize engine.
    engine = DetectionEngine('model_tflite/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite')
    labels = ReadLabelFile('model_tflite/coco_labels.txt')

    # Deep sort
    metric = nn_matching.NearestNeighborDistanceMetric("cosine", max_cosine_distance, nn_budget)
    tracker = Tracker(metric)
    #centroid tracker
    ct = CentroidTracker()
    cap = cv2.VideoCapture(1)

    writeVideo_flag = True
    if writeVideo_flag:
        w = int(cap.get(3))
        h = int(cap.get(4))
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        out = cv2.VideoWriter('output.avi', fourcc, 15, (w, h))
        list_file = open('detection.txt', 'w')
        frame_index = -1


    invert = True



    model_filename = 'model_data/mars-small128.pb'
    encoder = gdet.create_box_encoder(model_filename, batch_size=1)  # tensorflow nodig!

    while True:
        data = ""
        ret, frame = cap.read()
        t1 = time.time()
        if ret:

            cv2_im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2_im)
            width, height = img.size
            line1 = height/2 - 50
            draw = ImageDraw.Draw(img)

            # Run inference.
            ans = engine.DetectWithImage(img, threshold=0.6, keep_aspect_ratio=True, relative_coord=False, top_k=10)
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

            features = encoder(frame, boxs)

            # score to 1.0 here).
            detections = [Detection(bbox, 1.0, feature) for bbox, feature in zip(boxs, features)]
            print(track_iou(detections,0.5,0.9,0.6,5))
            objects = ct.update(boxs)

            draw.line((0, line1, width, line1), fill=10, width=5)
            img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

            for (objectID, centroid) in objects.items():
                #line_order[objectID] = deque(maxlen=2)
                if objectID not in line_trail.keys():
                    line_trail[objectID] = deque(maxlen=2)
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
                            #binnen() if invert else buiten()
                            if invert:
                                persons_in += 1
                                binnen()
                            else:
                                persons_in -= 1
                                buiten()
                        elif line_trail[objectID][1][1] < int(line1) and line_trail[objectID][0][1] > int(line1):
                            if invert:
                                buiten()
                                persons_in -= 1
                            else:
                                binnen()
                                persons_in += 1
                except Exception as Ex:
                    pass

            fps = (fps + (1. / (time.time() - t1))) / 2
            cv2.putText(img, "Binnen: " + str(persons_in), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255),lineType=cv2.LINE_AA)
            cv2.putText(img, "fps: " + str(int(fps)), (260, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255),lineType=cv2.LINE_AA)

            if writeVideo_flag:
                # save a frame
                out.write(img)


            cv2.imshow('preview', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

def callback(message_future):
    # When timeout is unspecified, the exception method waits indefinitely.
    if message_future.exception(timeout=1):
        print('Publishing message on {} threw an Exception {}.'.format(
            topic_name, message_future.exception()))
        f.write(data + ",")
    else:
        print("---------------------------------------")
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


def track_iou(detections, sigma_l, sigma_h, sigma_iou, t_min):
    """
    Simple IOU based tracker.
    See "High-Speed Tracking-by-Detection Without Using Image Information by E. Bochinski, V. Eiselein, T. Sikora" for
    more information.
    Args:
         detections (list): list of detections per frame, usually generated by util.load_mot
         sigma_l (float): low detection threshold.
         sigma_h (float): high detection threshold.
         sigma_iou (float): IOU threshold.
         t_min (float): minimum track length in frames.
    Returns:
        list: list of tracks.
    """

    tracks_active = []
    tracks_finished = []

    for frame_num, detections_frame in enumerate(detections, start=1):
        # apply low threshold to detections
        dets = [det for det in detections_frame if det['score'] >= sigma_l]

        updated_tracks = []
        for track in tracks_active:
            if len(dets) > 0:
                # get det with highest iou
                best_match = max(dets, key=lambda x: iou(track['bboxes'][-1], x['bbox']))
                if iou(track['bboxes'][-1], best_match['bbox']) >= sigma_iou:
                    track['bboxes'].append(best_match['bbox'])
                    track['max_score'] = max(track['max_score'], best_match['score'])

                    updated_tracks.append(track)

                    # remove from best matching detection from detections
                    del dets[dets.index(best_match)]

            # if track was not updated
            if len(updated_tracks) == 0 or track is not updated_tracks[-1]:
                # finish track when the conditions are met
                if track['max_score'] >= sigma_h and len(track['bboxes']) >= t_min:
                    tracks_finished.append(track)

        # create new tracks
        new_tracks = [{'bboxes': [det['bbox']], 'max_score': det['score'], 'start_frame': frame_num} for det in dets]
        tracks_active = updated_tracks + new_tracks

    # finish all remaining active tracks
    tracks_finished += [track for track in tracks_active
                        if track['max_score'] >= sigma_h and len(track['bboxes']) >= t_min]

    return tracks_finished



if __name__ == '__main__':
    main()
