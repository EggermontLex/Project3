import numpy as np
import cv2
from edgetpu.detection.engine import DetectionEngine

cap = cv2.VideoCapture(0)
edgetpu.basic.basic_engine.BasicEngine('mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite')

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()