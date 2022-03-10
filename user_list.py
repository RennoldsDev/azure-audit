from datetime import date as date
from azure.identity import EnvironmentCredential
from msgraph.core import GraphClient, APIVersion
from dotenv import load_dotenv

load_dotenv()

credential = EnvironmentCredential()
client = GraphClient(credential=credential, api_version=APIVersion.beta)

today = date.today()

# Gets all users (top 999 for now) from MS Graph and formats in JSON
result = client.get('/users?$top=999')
query_results = result.json()


def get_user_list():
    # Sets User list for appending information
    user_list = []
    for user in query_results['value']:
        if user['accountEnabled'] is True and user['jobTitle'] is not None:
            user_list.append(
                {
                    'upn': user['displayName'],
                    'displayName': user['userPrincipalName'],
                    'dateRan': today,
                }
            )
    return user_list
