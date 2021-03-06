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
from tools.CentroidTracker import CentroidTracker
from collections import deque
from tools.CloudManager import CloudManager
import threading

warnings.filterwarnings('ignore')

#aanmaken cloud manager
project_id = "Project3-ML6"
topic_name = "data_register"
publisher = CloudManager(project_id,topic_name)



def main(options):
    # management flags
    device = str(os.environ['device_id'])
    if not device:
        print("Warning: There is no device specified %s"% device)
        device = "Coral-1"
    flag_invert = options.invert
    flag_video = options.video
    flag_fps = options.fps
    if flag_video: flag_fps = True

    #declaratie gebruikte variabelen
    t1 =0.0
    fps = 0.0
    persons_in = 0
    line_trail = dict()
    publish = None

    engine = DetectionEngine('model_tflite/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite')

    ct = CentroidTracker()

    #capture videocamera
    cap = cv2.VideoCapture(1)

    if flag_video:
        w = int(cap.get(3))
        h = int(cap.get(4))
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        video = cv2.VideoWriter('Output.avi', fourcc, 30, (w, h))


    while True:
        ret, frame = cap.read()
        if flag_fps: t1 = time.time()

        if ret:
            cv2_im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2_im)
            width, height = img.size
            line1 = height/2 - 50
            draw = ImageDraw.Draw(img)

            # Run inference.
            detections = engine.DetectWithImage(img, threshold=options.threshold, keep_aspect_ratio=True, relative_coord=False, top_k=10,resample=Image.NEAREST) #BICUBIC
            boxs =[]

            # Display result.
            for obj in detections:
                box = obj.bounding_box.flatten().tolist()
                draw.rectangle(box, outline='red')
                boxs.append(box)

            objects = ct.update(boxs)

            if flag_video:
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
                            if flag_invert:
                                persons_in += 1
                                publish = threading.Thread(target=(lambda: publisher.publish_to_topic(data = ("+1,%s,%s" % (datetime.datetime.now(),device)))))
                            else:
                                persons_in -= 1
                                publish = threading.Thread(target=(lambda: publisher.publish_to_topic(data = ("-1,%s,%s" % (datetime.datetime.now(),device)))))

                        elif line_trail[objectID][1][1] < int(line1) and line_trail[objectID][0][1] > int(line1):
                            if flag_invert:
                                persons_in -= 1
                                publish = threading.Thread(target=(lambda: publisher.publish_to_topic(data = ("-1,%s,%s" % (datetime.datetime.now(),device)))))
                            else:
                                persons_in += 1
                                publish = threading.Thread(target=(lambda: publisher.publish_to_topic(data = ("+1,%s,%s" % (datetime.datetime.now(),device)))))
                        if publish:
                            publish.start()
                            publish = None
                except Exception as Ex: #deque not long eneough error, niet nodig om op te vangen
                    if not "deque" in "%s" %Ex:
                        print("Exception: %s" %Ex)

            if flag_fps or flag_video:
                fps = (1. / (time.time() - t1))
            if flag_fps: print("fps : %d" % fps)
            if flag_video:
                video.write(img)
            cv2.putText(img, "Binnen: %s" % persons_in, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255),lineType=cv2.LINE_AA)
            cv2.putText(img, "fps: %d" % fps, (260, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255),lineType=cv2.LINE_AA)
            cv2.imshow('Output', img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--invert', type=bool, default=True, help='binnen <-> buiten --> buiten <-> binnen')
    parser.add_argument('--resample', type=str, default="NEAREST", help='what form of image detection you want, NEAREST or BICUBIC')
    parser.add_argument('--fps', type=bool, default=False, help='Print fps counter')
    parser.add_argument('--video', type=bool, default=False,help='Do you want to display and save video from the actions going on in the backgroud')
    parser.add_argument('--threshold', type=int, default=0.65,help='minimum allowed value for the threshold')
    options = parser.parse_args()
    main(options)
