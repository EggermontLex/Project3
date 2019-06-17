# Backend
Here we'll go deeper on the backend part of the project and the specific functions that will run on google cloud and on the device.
## Python packages
```firestore_push.py```, ```list_devices.py``` and ```update_train.py``` are run on the cloud so they don't require you to manually install python packages, all you have to do is add the packages you intend to use to the ```requirements.txt``` file. For our project we use:
**google-api-python-client>=1.7.9**
