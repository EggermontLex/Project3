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

```
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--invert', type=bool, default=True, help='binnen <-> buiten --> buiten <-> binnen')
    parser.add_argument('--resample', type=str, default="NEAREST", help='what form of image detection you want, NEAREST or BICUBIC')
    parser.add_argument('--fps', type=bool, default=False, help='Print fps counter')
    parser.add_argument('--video', type=bool, default=False,help='Do you want to display and save video from the actions going on in the backgroud')
    options = parser.parse_args()
    main(options)
```



 
