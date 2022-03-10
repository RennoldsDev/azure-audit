import device_encryption as device
import directory_roles as directory
import user_list as user
import pandas as pd
import atp as atp
from datetime import date as date

today = date.today()


def get_csv_files():
    directory_roles = directory.get_directory_roles()
    user_list = user.get_user_list()
    device_list = device.get_device_encryption()
    atp_devices = atp.get_atp_status()

    # Uses Pandas to cleanly export lists to csv
    directory_roles_csv = pd.DataFrame(directory_roles)
    directory_roles_csv.to_csv(f'DirectoryRoles.csv-{today}.csv', index=False)

    user_list_csv = pd.DataFrame(user_list)
    user_list_csv.to_csv(f'UserList.csv-{today}.csv', index=False)

    device_list_csv = pd.DataFrame(device_list)
    device_list_csv.to_csv(f'DeviceEncryption.csv-{today}.csv', index=False)

    atp_devices_csv = pd.DataFrame(atp_devices)
    atp_devices_csv.to_csv(f'DefenderStatus.csv-{today}.csv', index=False)

    return None
