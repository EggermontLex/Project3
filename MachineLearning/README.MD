# Machine Learning
In dit gedeelte zal er iets dieper ingegaan worden op de code die geschreven is en wat er nodig is voor dit gedeelte.

## Inhoudstafel

## Python packages
**Edgetpu:** pre-installed computervision library van google zelf

**Argparse**: `pip install argparse` deze library word gebruikt om parameters mee te geven aan python files

**Pillow**: `pip install Pillow` een library voor afbeeldingen te bewerken.

**Numpy**: `pip install numpy` een python library voor het verwerken van arrays

**Requests**: `pip install requests` een library voor het uitvoeren van web requests 

**Google cloud**: `pip install google-cloud` een library van google zelf voor verscheiden zaken gerelateerd met google cloud


## De code

Eerst overlopen we de code voor het uitlezen van de webcam, aangezien dat dit het hart is van ons project.

#### Imports

De volgend imports zijn nodig voor het kunnen uitvoeren van het programma:
```
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
from tools.centroidtracker import CentroidTracker
from collections import deque
from tools.cloud_manager import CloudManager
```


#### `if __name__ = '__main__':`

De onderstaande code geeft de mogelijkheid dat er andere parameters gebruikt worden tijdens het uitvoeren van de code, zo kan je hier bijvoorbeeld enkele parameters aanpassen. 

`--invert` word gebruikt voor het aanpassen van de richting binnen <> buiten

`--resample`met deze flag kan je de resampeling instellen, default staat deze op `NEAREST`, maar met `BICUBIC`

`--fps` hiermee kan je de fps laten printen

`--video` je kan de video output hiermee inschakelen

`--threshold` hier mee kan je de minimaal waarde instellen, deze waarde is de zekerheid dat het daadwerkelijk een persoon is.

```
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--invert', type=bool, default=True, help='binnen <-> buiten --> buiten <-> binnen')
    parser.add_argument('--resample', type=str, default="NEAREST", help='what form of image detection you want, NEAREST or BICUBIC')
    parser.add_argument('--fps', type=bool, default=False, help='Print fps counter')
    parser.add_argument('--video', type=bool, default=False,help='Do you want to display and save video from the actions going on in the backgroud')
    parser.add_argument('--threshold', type=int, default=0.65,help='minimum allowed value for the threshold')
    options = parser.parse_args()
    main(options)
```
### Variabelen aanmaken

Voor het wegschrijven van het binnen en buiten gaan van personen moet er connectie gemaakt worden met de cloud, de onderstaande code initializeerd de `CloudManager`, dit is een zelfgeschreve klasse waarover er later meer informatie over gegeven wordt. 
```
project_id = "Project3-ML6"
topic_name = "data_register"
publisher = CloudManager(project_id,topic_name)
```

Voor een vlotte werking van de code is het belangrijk dat er gebruik gemaakt word van enkele 'flags' deze flags worden ingegeven door de gebruiker bij het opstarten van het script.
```
device = str(os.environ['device_id'])
flag_invert = options.invert
flag_video = options.video
flag_fps = options.fps
```

De onderstaande code bevat enkele niet zo belangrijke variabelen.
```
t1 =0.0
fps = 0.0
persons_in = 0
line_trail = dict()
```
Echter het initializeren van de `DetectionEngine` is een belangrijk gedeelte, de gebruikte Detection engine vereist een geconverteerd tensorflow light model. Het converteren van de modellen kan je makkelijk online vinden op de [site](https://www.tensorflow.org/lite) van tensorflow zelf. Het model dat wij gebruiken is pre build en online available. Met dit model  kan je meer dan 90 verschillende dingen detecteren, echter hebben we dit model gekozen aangezien het uiterst goed is om personen te detecteren. Zo detecteert het zelfs één voet of hand als onderdeel van een persoon, dit komt omdat ze een zeer goed gebalanceerde dataset ter beschikking hadden voor het trainen van het model.
```
engine = DetectionEngine('model_tflite/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite')
```

Als tracking software hebben we geexperimenteerd met meerdere trackers(CentroidTracker, cv2.Mossy tracker, iou tracker en deep sort), echter bleek uit onze tests dat enkel de CentroidTracker licht genoeg was om deftig te kunnen draaien op de gogole coral devboard

```
ct = CentroidTracker()
```
Onderstaande code wordt uitgevoerd als de gebruiker bij het opstarten de `--video` flag op true zet, deze haalt de width en height op uit een 'frame', vervoglens selecteer je de video encoder, `MJPG` in dit geval. Het laatste lijntje maakt de videofile aan met de verkregen parameters
```
if flag_video:
    w = int(cap.get(3))
    h = int(cap.get(4))
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    video = cv2.VideoWriter('output.avi', fourcc, 15, (w, h))
```
### `while true:`
Nu zijn we in het hart van de code beland, hier gebeurt het processen en verwerken van de verkregen live opnames. telkens al de code 1 maal looped, zal er ee nieuwe frame opgevraagd worden `ret, frame = cap.read()` in `ret` komt de status van de frame terecht, met andere woorden, is er een frame of niet. In `frame` komt dan de array die de afbeelding voorstelt. Om fouten te voorkomen kijken we of de frame wel succesvol gelukt is met een simpele if `if ret:`
Vervolgens decoden we de frame van BGR (dit is de default van opencv) naar RGB (default voor Pillow), dit is nodig omdat de `DetectionEngine` een pillow image verwacht.
Nadat we de frame gedecode hebben moeten we die terug converteren naar een image `img = Image.fromarray(cv2_im)` zodanig dat we de hoogte en breedte hiervan kunnen uitlezen `width, height = img.size` om dan weer een virtuele scheidingslijn te kunnen declareren: `line1 = height/2 - 50`. Deze virtuele scheidingslijn wordt zowel gebruikt om visueel weer te geven waneer iemand binnen of buiten gaat, als variabele scheidingslijn. Als laatste stap voordat we de object detection gaan uitvoeren op de image, gaan we aan de hand van pillow de afbeelding verwerken om er later de nodige lijnen en boxen op te tekenen `draw = ImageDraw.Draw(img)`

##### Object detection
Nu is het tijd om de object detection los te laten gaan op de frame, dit gebeurd aan de hand van deze simpele lijn code:
```
ans = engine.DetectWithImage(img, threshold=options.threshold, keep_aspect_ratio=True, relative_coord=False, top_k=10,resample=Image.NEAREST) #BICUBIC
```
Hierbij word de `threshold` ingesteld met de waarde die  meegegeven werd door de gebruiker, `keep_aspect_ratio` staat altijd op `True`, indien dit niet zo zou zijn zou dit de accuraatheid van de detections zwaar kunnen doen dalen, aangezien het dan een samengeperste afbeelding kan zijn (wat dus niet overeenkomt met de realiteit), `relative_coord` is of je de coordinaten van de punten op de image wilt herleiden naar een waarde tussen 0 en 1, deze flag maakt volgens ons niet zo een groot verschil, dus we hebben deze gewoon laten staan. `top_k` is ook default ingesteld op `10` dit omdat de code er effectief 10 zal proberen vinden, echter het simpelweg op 1 zetten zou de code van multitracking naar single person tracking brengen, aangezien het dan maar 1 persoon zoek. 10 leek ons de beste processingtime/realiteit verhouding. De `resample` is belangrijk indien de image rescaled word bij het processen, zo zal `NEAREST` je beter performance geven (22fps) en `BICUBIC` een net iets beter accuraatheid leveren (12fps).

Vervolgens krijg je dus de collectie met de detecties in `ans`, de onderstaande code leest alle gevonden 'objects' uit en maakt hiervaan een lijst van de box coordinaten. Ook indien de `--video` flag op `True` ingesteld is, zal hier ook een box rond de detectie getekend worden.
```
if ans:
    for obj in ans:
        box = obj.bounding_box.flatten().tolist()
        if flag_video: draw.rectangle(box, outline='red')
        boxs.append(box)
```
##### Object tracking
De verkregen lijst van detecties word vervolgens doorgegeven aan de 'Centroid Tracker', deze tracker analizeerd aan de hand van de locaties van de boxes welke box er in de vorige 'frame' gerelateerd is aan die in de huidige 'frame', dit is dus zeker niet de accuraatste tracker, echter heeft deze een goede performance.
Als je genoeg rekenkracht ter beschkking hebt (niet op een google devboard cpu'tje) raad ik aan om 'deep sort' te gebruiken, deze gebruikt een verzameling van technieken om zo efficient mogelijk de gerelateerde detectie te vinden in de nieuwe frame. hoe dit werkt zoek je best zelf even op, aangezien dit een behoorlijk lange uitleg is.(wel heb ik de tracking met deep sort implementatie ook toegevoegd aan de code)
```
objects = ct.update(boxs)
```
Vervolgens moeten we de objecten 1 voor 1 overlopen en afhandelen welke er binnen/buiten zijn gegaan en welke nog niet over de streep zijn.
```
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
                if flag_invert:
                    persons_in += 1
                    publisher.publish_to_topic(data = ("+1,%s,%s" % (datetime.datetime.now(),device)))
                else:
                    persons_in -= 1
                    publisher.publish_to_topic(data = ("-1,%s,%s" % (datetime.datetime.now(),device)))
            elif line_trail[objectID][1][1] < int(line1) and line_trail[objectID][0][1] > int(line1):
                if flag_invert:
                    publisher.publish_to_topic(data = ("-1,%s,%s" % (datetime.datetime.now(),device)))
                    persons_in -= 1
                else:
                    publisher.publish_to_topic(data = ("+1,%s,%s" % (datetime.datetime.now(),device)))
                    persons_in += 1
    except Exception as Ex: #deque not long eneough error, niet nodig om op te vangen
        pass
```
de variabele `line_trail` bevat de vorige locatie van het centrum van het object, deze word opgeslagen zodanig dat er later mee vergeleken kan worden. ook hier is er een `--video` flag aanwezig, hier zal de code de Id, het centrum en de bovenste lijn van de box tekenen. Zelf hebben we een kleine afhandeling geschreven zodanig dat de accuraatheid van de centroid tracker iets beter is, we hebben een maximum differentiaal ingesteld op 60px. Dit voorkomt dat als de origineel getrackte persoon het beeld verlaat en er een andere binnen komt dat er geen mistdetectie is. `diff = abs(line_trail[objectID][0][0] - line_trail[objectID][1][0])` . Vervolgens gaan we kijken of het vorige punt boven de lijn ligt en het huidige punt onder de lijn or omgekeerd `if line_trail[objectID][0][1] < int(line1) and line_trail[objectID][1][1] > int(line1):`, als dit niet het geval is gaan we gewoon verder naar het volgend object. indien dit wel het geval is, zal men aan de hand van de `CloudManager` klasse een getal (+1 of -1) samen met het exacte tijdstip en de toestelnaam verstuurd worden naar de cloud. `publisher.publish_to_topic(data = ("+1,%s,%s" % (datetime.datetime.now(),device)))`

Als het voorlaatste onderdeel van de code zijn er nogmaals 2 flags, de `--fps` en `--video` flag, deze code spreekt voor zichzelf
```
if flag_fps: print("fps : %d" % ((fps + (1. / (time.time() - t1))) / 2))
if flag_video:
    cv2.putText(img, "Binnen: " + str(persons_in), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255),lineType=cv2.LINE_AA)
    cv2.putText(img, "fps: " + str(int(fps)), (260, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255),lineType=cv2.LINE_AA)
    video.write(img)
    cv2.imshow('preview', img)
```

Bij het afsluiten van de code is het belangrijk dat je de camera weer vrijgeeft `cap.release()`
