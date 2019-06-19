from google.oauth2 import service_account
from googleapiclient import discovery
import os
import io

registry_path = 'projects/{}/locations/{}/registries/{}'.format('''project3-ml6''', '''europe-west1''',
                                                                '''project3core''')


def create_device():
    client = get_client(str(os.environ['GOOGLE_APPLICATION_CREDENTIALS']))

    with io.open(str(os.environ['RSA_CERT'])) as f:
        certificate = f.read()

    device_template = {
        'id': str(os.environ['DEVICE_ID']),
        'credentials': [{
            'publicKey': {
                'format': 'RSA_X509_PEM',
                'key': certificate
            }
        }]
    }

    devices = client.projects().locations().registries().devices()
    devices.create(parent=registry_path, body=device_template).execute()
    device_name = '{}/devices/{}'.format(registry_path, str(os.environ['DEVICE_ID']))
    client.projects().locations().registries().devices().patch(name=device_name, updateMask='metadata', body={"metadata": {"Train": ""}}).execute()


def get_client(service_account_json):
    api_scopes = ['https://www.googleapis.com/auth/cloud-platform']
    api_version = 'v1'
    credentials = service_account.Credentials.from_service_account_file(service_account_json)

    return discovery.build(
            'cloudiotcore',
            api_version,
            discoveryServiceUrl='{}?version={}'.format('https://cloudiot.googleapis.com/$discovery/rest', api_version),
            credentials=credentials.with_scopes(api_scopes))


if __name__ == '__main__':
    create_device()
