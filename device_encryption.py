from datetime import date as date
import pagination


def get_device_encryption(graph_call, client):
    windows_devices = client.get(graph_call)
    devices_json = windows_devices.json()

    pagination.pagination(devices_json)
    devices = []

    for device in devices_json['value']:
        devices.append(
            {
                'upn': device['userPrincipalName'],
                'device': device['deviceName'],
                'encrypted': device['encryptionState'],
                'dateRan': date.today(),
            })

    return devices
