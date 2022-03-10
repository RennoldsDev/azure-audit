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


# TODO add pagination instead of 'top' call
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
