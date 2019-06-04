from edgetpu.detection.engine import DetectionEngine
from PIL import Image
from PIL import ImageDraw
import numpy as np
import cv2


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
    # Initialize engine.
    engine = DetectionEngine('mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite')
    labels = ReadLabelFile('coco_labels.txt')

    # Open video
    cap = cv2.VideoCapture(1)

    while True:
        _, frame = cap.read()
        cv2_im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2_im)
        draw = ImageDraw.Draw(img)

        # Run inference.
        ans = engine.DetectWithImage(img, threshold=0.5, keep_aspect_ratio=True,
                                     relative_coord=False, top_k=10)

        # Display result.
        if ans:
            for obj in ans:
                if labels:
                    print(labels[obj.label_id])
                box = obj.bounding_box.flatten().tolist()
                # Draw a rectangle.
                print(box)
                draw.rectangle(box, outline='red')
                draw.text((box[0], box[1]), labels[obj.label_id])
                draw.text((box[0], box[1]+10), str(obj.score))

        opencv_image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        cv2.imshow('preview', opencv_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
