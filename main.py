import os

from azure.identity import InteractiveBrowserCredential
from msgraph.core import GraphClient, APIVersion
import pandas as pd
from datetime import date as date
import atp as atp
from dotenv import load_dotenv

load_dotenv()

today = date.today()

# Uses Azure Identity to sign in user and MS Graph to run all queries
browser_credential = InteractiveBrowserCredential(client_id=os.getenv('APPID'))
client = GraphClient(credential=browser_credential, api_version=APIVersion.beta)


# Sets blank list and gets all Azure Directory Roles. If members exist in a role it will append information
roles = []
DirectoryRoles = client.get('/directoryRoles')

for role in DirectoryRoles.json()['value']:
    members = client.get(f'/directoryRoles/{role["id"]}/members')

    # Will only run if members exist within the role, any role with 0 members is excluded
    if len(members.json()['value']) > 0:
        for i in range(len(members.json()['value'])):
            # Way to check if 'userPrincipalName' is within the key, will error if excluded
            if 'userPrincipalName' in members.json()['value'][i].keys():
                roles.append(
                    {
                        'role': role['displayName'],
                        'id': role['id'],
                        'upn': members.json()['value'][i]['userPrincipalName'],
                        'dateRan': today,
                    }

                )

# Gets all managed devices and encryption states in JSON
WindowsDevices = client.get('/deviceManagement/managedDeviceEncryptionStates/')
devices_json = WindowsDevices.json()

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

# Gets all users (top 999 for now) from MS Graph and formats in JSON
result = client.get('/users?$top=999')
QueryResults = result.json()

# TODO add pagination instead of 'top' call

# Sets User list for appending information
UserList = []
for user in QueryResults['value']:
    if user['accountEnabled'] is True and user['jobTitle'] is not None:
        UserList.append(
            {
                'upn': user['displayName'],
                'displayName': user['userPrincipalName'],
                'dateRan': today,
            }
        )

# Imported from atp.py - this uses environment variables to graph onboarding status of ATP.
AtpDevices = atp.get_atp_status()


# Uses Pandas to cleanly export lists to csv
DirectoryRolesCsv = pd.DataFrame(roles)
DirectoryRolesCsv.to_csv(f'DirectoryRoles.csv-{today}.csv', index=False)

UserListCsv = pd.DataFrame(UserList)
UserListCsv.to_csv(f'UserList.csv-{today}.csv', index=False)

DevicesCsv = pd.DataFrame(devices)
DevicesCsv.to_csv(f'DeviceEncryption.csv-{today}.csv', index=False)

AtpDevicesCsv = pd.DataFrame(AtpDevices)
AtpDevicesCsv.to_csv(f'EncryptionStatus.csv-{today}.csv', index=False)
