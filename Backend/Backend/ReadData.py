from base64 import b64decode
import uuid
from firebase_admin import initialize_app, credentials, firestore
import datetime

cred = credentials.ApplicationDefault()
initialize_app(cred, {'projectId': "project3-ml6"})
db = firestore.client()


def push_data(event, context):
    doc_ref = db.collection(u'realtime').document(u'IC_70')
    doc = doc_ref.get().to_dict()
    value = doc['current_value']

    # Use the application default credentials

    pubsub_message = b64decode(event['data']).decode('utf-8')
    lst_message = pubsub_message.split(",")
    date_time_obj = datetime.datetime.strptime(lst_message[1], '%Y-%m-%d %H:%M:%S.%f')
    upd = value + int(lst_message[0])
    doc_ref.update({
        u'current_value': upd,
        u'last_updated': date_time_obj})
    data_history = {
        u'timestamp':date_time_obj,
        u'train': u'IC_70',
        u'value': upd}
    db.collection(u'history').document(str(uuid.uuid4())).set(data_history)