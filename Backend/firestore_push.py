from base64 import b64decode
import uuid
from firebase_admin import initialize_app, credentials, firestore
import datetime
from google.oauth2 import service_account
from googleapiclient import discovery

cred = credentials.ApplicationDefault()
initialize_app(cred, {'projectId': "project3-ml6"})
db = firestore.client()

def push_data(event, request):
    pubsub_message = b64decode(event['data']).decode('utf-8')
    lst_message = pubsub_message.split(",")
    device_id = lst_message[2]
    metadata = get_metadata(device_id)


    doc_ref = db.collection(u'realtime').document(metadata)
    doc = doc_ref.get().to_dict()

    if doc == None:
        data ={
            u'current_value': 0,
            u'last_updated': datetime.datetime.strptime(lst_message[1], '%Y-%m-%d %H:%M:%S.%f')}
        db.collection(u'realtime').document(metadata).set(data)
        value = 0
    else:
        value = doc['current_value']

    date_time_obj = datetime.datetime.strptime(lst_message[1], '%Y-%m-%d %H:%M:%S.%f')
    upd = value + int(lst_message[0])
    if upd > 0:
        doc_ref.update({
            u'current_value': upd,
            u'last_updated': date_time_obj})
        data_history = {
            u'timestamp':date_time_obj,
            u'train': metadata,
            u'value': upd}
        db.collection(u'history').document(str(uuid.uuid4())).set(data_history)


def get_client(service_account_json):
    """Returns an authorized API client by discovering the IoT API and creating
    a service object using the service account credentials JSON."""
    api_scopes = ['https://www.googleapis.com/auth/cloud-platform']
    api_version = 'v1'
    discovery_api = 'https://cloudiot.googleapis.com/$discovery/rest'
    service_name = 'cloudiotcore'

    credentials = service_account.Credentials.from_service_account_file(
            service_account_json)
    scoped_credentials = credentials.with_scopes(api_scopes)

    discovery_url = '{}?version={}'.format(
            discovery_api, api_version)

    return discovery.build(
            service_name,
            api_version,
            discoveryServiceUrl=discovery_url,
            credentials=scoped_credentials)


def get_metadata(device_id):
    client = get_client('Project3-ML6-420c2216d454.json')
    registry_path = 'projects/{}/locations/{}/registries/{}'.format('''project3-ml6''', '''europe-west1''',
                                                                    '''project3core''')
    devices = client.projects().locations().registries().devices()
    device_name = '{}/devices/{}'.format(registry_path, device_id)

    a = devices.get(name=device_name).execute()
    b = a.get('metadata')
    return b['Train']
