# Backend
Here we'll go deeper on the backend part of the project and the specific functions that will run on google cloud and on the device.
## Python packages
```firestore_push.py```, ```list_devices.py``` and ```update_train.py``` are run on the cloud so they don't require you to manually install python packages, all you have to do is add the packages you intend to use to the ```requirements.txt``` file. For our project we use:

**google API python client** ```google-api-python-client>=1.7.9``` library that makes it easier to work with your service accounts.

**firebase admin** ```firebase-admin>=2.17.0``` library that you need to communicate with google firebase.

**google cloud pubsub** ```google-cloud-pubsub>=0.41.0``` library that you need send and recieve data from google pubsub.

```create_device.py``` runs on the device itself so the following packages you'll have to install or build yourself:

**Argparse** ```pip install argparse``` this library is used to add arguments to python files.

**google API python client** ```pip install google-api-python-client``` library that makes it easier to work with your service accounts.

## The code

First I'll discuss the ```get_client()``` and the ```get_metadata()``` function, because we use those in multiple python files.

```
def get_client(service_account_json):
    api_scopes = ['https://www.googleapis.com/auth/cloud-platform']
    api_version = 'v1'
    credentials = service_account.Credentials.from_service_account_file(service_account_json)

    return discovery.build(
            'cloudiotcore',
            api_version,
            discoveryServiceUrl='{}?version={}'.format( 'https://cloudiot.googleapis.com/$discovery/rest', api_version),
            credentials=credentials.with_scopes(api_scopes))
```

The ```get_client()``` function is needed to allow cloud functions to acces certain data on other parts of the google cloud, we mainly use  it to get acces to firebase and Iot core metadata.

```
def get_metadata(device_id):
    client = get_client('Project3-ML6-420c2216d454.json')
    registry_path = 'projects/{}/locations/{}/registries/{}'.format('''project3-ml6''', '''europe-west1''',
                                                                    '''project3core''')
    devices = client.projects().locations().registries().devices()
    device_name = '{}/devices/{}'.format(registry_path, device_id)
    return devices.get(name=device_name).execute().get('metadata')['Train']
```

The ```get_metadata()``` function is needed to get the metadata of the device from google cloud Iot Core.

### firestore_push.py

Sends the data that is being received in the cloud pubsub topic to the firestore database.

```


```
