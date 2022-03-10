from datetime import date as date
from azure.identity import EnvironmentCredential
from msgraph.core import GraphClient, APIVersion
from dotenv import load_dotenv

load_dotenv()

credential = EnvironmentCredential()
client = GraphClient(credential=credential, api_version=APIVersion.beta)

today = date.today()


# Gets all managed devices and encryption states in JSON
windows_devices = client.get('/deviceManagement/managedDeviceEncryptionStates/')
devices_json = windows_devices.json()

# Uses pagination within the graph call to get all users
while '@odata.nextLink' in devices_json.keys():
    paginated_query = client.get(devices_json['@odata.nextLink'])
    paginated_results = paginated_query.json()
    if '@odata.nextLink' in paginated_results:
        devices_json['@odata.nextLink'] = paginated_results['@odata.nextLink']
    else:
        del devices_json['@odata.nextLink']
    devices_json['value'].extend(paginated_results['value'])


def get_device_encryption():
    # Sets device list for appending information
    devices = []

    for device in devices_json['value']:
        devices.append(
            {
                'upn': device['userPrincipalName'],
                'device': device['deviceName'],
                'encrypted': device['encryptionState'],
                'dateRan': today,
            })

    return devices
