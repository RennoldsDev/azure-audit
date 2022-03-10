from datetime import date as date

from pandas import DataFrame
from azure.identity import EnvironmentCredential
from dotenv import load_dotenv
from msgraph.core import GraphClient, APIVersion

from atp import get_atp_status
from device_encryption import get_device_encryption
from directory_roles import get_directory_roles
from user_list import get_user_list

load_dotenv()
credential = EnvironmentCredential()
client = GraphClient(credential=credential, api_version=APIVersion.beta)

today = date.today()


def get_csv_files():
    # Uses Pandas to cleanly export lists to csv
    DataFrame(get_directory_roles('/directoryRoles', client, today)).to_csv(
        f'DirectoryRoles.csv-{today}.csv',
        index=False)

    DataFrame(get_user_list('/users', client, today)).to_csv(
        f'UserList.csv-{today}.csv',
        index=False)

    DataFrame(get_device_encryption('/deviceManagement/managedDeviceEncryptionStates/', client, today)).to_csv(
        f'DeviceEncryption.csv-{today}.csv',
        index=False)

    DataFrame(get_atp_status(today)).to_csv(
        f'DefenderStatus.csv-{today}.csv',
        index=False)

    return None
