from google.oauth2 import service_account
from googleapiclient import discovery
import time
import argparse

registry_path = 'projects/{}/locations/{}/registries/{}'.format('''project3-ml6''', '''europe-west1''',
                                                                '''project3core''')


def create_device(options):
    client = get_client('Project3-ML6-8f539587a27f.json')

    # Note: You can have multiple credentials associated with a device.
    device_template = {
        'id': options.deviceId,
        'credentials': [{
            'publicKey': {
                'format': 'RSA_X509_PEM',
                'key':  [line.rstrip("\n") for line in open(options.filename)]
            }
        }]
    }

    devices = client.projects().locations().registries().devices()
    devices.create(parent=registry_path, body=device_template).execute()
    time.sleep(3)
    client.projects().locations().registries().devices().patch(name=options.deviceId, updateMask='metadata', body={"metadata": {"Train": None}}).\
        execute()


def get_client(service_account_json):
    api_scopes = ['https://www.googleapis.com/auth/cloud-platform']
    api_version = 'v1'
    credentials = service_account.Credentials.from_service_account_file(service_account_json)

    return discovery.build(
            'cloudiotcore',
            api_version,
            discoveryServiceUrl='{}?version={}'.format( 'https://cloudiot.googleapis.com/$discovery/rest', api_version),
            credentials=credentials.with_scopes(api_scopes))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', type=str, required=True)
    parser.add_argument('--deviceId', type=str, required=True)
    options = parser.parse_args()
    create_device(options)
