from datetime import date as date
from azure.identity import EnvironmentCredential
from msgraph.core import GraphClient, APIVersion
from dotenv import load_dotenv

load_dotenv()

credential = EnvironmentCredential()
client = GraphClient(credential=credential, api_version=APIVersion.beta)

today = date.today()


def get_directory_roles():
    directory_roles = client.get('/directoryRoles')

    # Sets blank list and gets all Azure Directory Roles. If members exist in a role it will append information
    roles = []

    for role in directory_roles.json()['value']:
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
    return roles
