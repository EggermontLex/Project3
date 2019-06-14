from edgetpu.detection.engine import DetectionEngine
from PIL import Image
from timeit import time
from PIL import ImageDraw
import numpy as np
import cv2
import warnings
import datetime



from tools.centroidtracker import CentroidTracker
from collections import deque
warnings.filterwarnings('ignore')

from tools.cloud_manager import CloudManager


#aanmaken cloud manager
project_id = "Project3-ML6"
topic_name = "data_register"
publisher = CloudManager(project_id,topic_name)

#management flags
flag_invert=True
flag_video = False
flag_fps = True

def main():

    #declaratie gebruikte variabelen
    t1 =0.0
    fps = 0.0
    persons_in = 0
    line_trail = dict()

    #Initialize engine.
    engine = DetectionEngine('model_tflite/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite')

    #instantie aanmaken van de centroid tracker
    ct = CentroidTracker()

    #capture videocamera
    cap = cv2.VideoCapture(1)

    if flag_video:
        w = int(cap.get(3))
        h = int(cap.get(4))
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        video = cv2.VideoWriter('output.avi', fourcc, 15, (w, h))


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
            ans = engine.DetectWithImage(img, threshold=0.65, keep_aspect_ratio=True, relative_coord=False, top_k=10,resample=Image.BICUBIC)
            boxs =[]

            # Display result.
            if ans:
                for obj in ans:
                    box = obj.bounding_box.flatten().tolist()
                    if flag_video: draw.rectangle(box, outline='red')
                    boxs.append(box)

            objects = ct.update(boxs)

            if flag_video:
                draw.line((0, line1, width, line1), fill=10, width=5)
                img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

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
                            #binnen() if invert else buiten()
                            if flag_invert:
                                persons_in += 1
                                publisher.publish_to_topic_new(data = ("+1,%s" % datetime.datetime.now()))
                            else:
                                persons_in -= 1
                                publisher.publish_to_topic_new(data = ("-1,%s" % datetime.datetime.now()))
                        elif line_trail[objectID][1][1] < int(line1) and line_trail[objectID][0][1] > int(line1):
                            if flag_invert:
                                publisher.publish_to_topic_new(data = ("-1,%s" % datetime.datetime.now()))
                                persons_in -= 1
                            else:
                                publisher.publish_to_topic_new(data = ("+1,%s" % datetime.datetime.now()))
                                persons_in += 1
                except Exception as Ex:
                    pass

            if flag_fps: print("fps : %d" % ((fps + (1. / (time.time() - t1))) / 2))
            if flag_video:
                cv2.putText(img, "Binnen: " + str(persons_in), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255),lineType=cv2.LINE_AA)
                cv2.putText(img, "fps: " + str(int(fps)), (260, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255),lineType=cv2.LINE_AA)

            if flag_video:
                video.write(img)
                cv2.imshow('preview', img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
