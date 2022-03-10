import device_encryption, directory_roles, user_list, atp
import pandas as pd
from datetime import date as date
from azure.identity import EnvironmentCredential
from msgraph.core import GraphClient, APIVersion
from dotenv import load_dotenv

load_dotenv()
credential = EnvironmentCredential()
client = GraphClient(credential=credential, api_version=APIVersion.beta)

today = date.today()


def get_csv_files():
    dir_roles = directory_roles.get_directory_roles('/directoryRoles', client)
    users = user_list.get_user_list('/users', client)
    device_list = device_encryption.get_device_encryption('/deviceManagement/managedDeviceEncryptionStates/', client)
    atp_devices = atp.get_atp_status()

    # Uses Pandas to cleanly export lists to csv
    directory_roles_csv = pd.DataFrame(dir_roles)
    directory_roles_csv.to_csv(f'DirectoryRoles.csv-{today}.csv', index=False)

    user_list_csv = pd.DataFrame(users)
    user_list_csv.to_csv(f'UserList.csv-{today}.csv', index=False)

    device_list_csv = pd.DataFrame(device_list)
    device_list_csv.to_csv(f'DeviceEncryption.csv-{today}.csv', index=False)

    atp_devices_csv = pd.DataFrame(atp_devices)
    atp_devices_csv.to_csv(f'DefenderStatus.csv-{today}.csv', index=False)

    return None
