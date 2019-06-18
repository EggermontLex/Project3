from google.oauth2 import service_account
from googleapiclient import discovery
import json


def list_devices(request):
    """List all devices in the registry."""
    # [START iot_list_devices]
    client = get_client('Project3-ML6-420c2216d454.json')
    registry_path = 'projects/{}/locations/{}/registries/{}'.format('''project3-ml6''', '''europe-west1''', '''project3core''')
    print("start")
    deviceslist = client.projects().locations().registries().devices().list(parent=registry_path).execute().get('devices', [])
    devices = client.projects().locations().registries().devices()
    response = []
    for device in deviceslist:
        metadata = str(get_metadata(device.get('id'), devices, registry_path))
        device_info = {
            "id": device.get('numId'),
            "name": device.get('id'),
            "train": metadata
        }
        response.append(device_info)

    headers = {
        'Access-Control-Allow-Origin': '*'
    }
    return (json.dumps(response), 200, headers)


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

def get_metadata(device_id,devices,registry_path):
    device_name = '{}/devices/{}'.format(registry_path, device_id)
    return devices.get(name=device_name).execute().get('metadata')['Train']
