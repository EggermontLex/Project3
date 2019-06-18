from google.oauth2 import service_account
from googleapiclient import discovery


def update_train(request):
    if request.method == 'OPTIONS':
        headers = {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': 'Content-Type',
                   'Access-Control-Allow-Methods': 'POST, OPTIONS'}
        return ("", 200, headers)
    if request.headers['Content-Type'] == 'application/json':
        request_json = request.get_json(silent=True)
        if request_json and 'name' in request_json:
            name = request_json['name']
            train = request_json['train']
            client = get_client('Project3-ML6-420c2216d454.json')
            registry_path = 'projects/{}/locations/{}/registries/{}'.format('''project3-ml6''', '''europe-west1''',
                                                                            '''project3core''')
            device_name = '{}/devices/{}'.format(registry_path, name)

            patch = {"metadata": {"Train": train}}
            client.projects().locations().registries().devices().patch(
                name=device_name, updateMask='metadata', body=patch).execute()
            headers = {'Access-Control-Allow-Origin': '*'}
            return ("Update successful", 200, headers)
        else:
            raise ValueError("JSON is invalid, or missing a 'name' property")
    else:
        raise ValueError("Unknown content type: {}".format(content_type))


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


def get_metadata(device_id, devices, registry_path):
    device_name = '{}/devices/{}'.format(registry_path, device_id)
    return devices.get(name=device_name).execute().get('metadata')['Train']
