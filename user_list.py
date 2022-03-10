from datetime import date as date
from azure.identity import EnvironmentCredential
from msgraph.core import GraphClient, APIVersion
from dotenv import load_dotenv
import pagination

load_dotenv()

credential = EnvironmentCredential()
client = GraphClient(credential=credential, api_version=APIVersion.beta)

today = date.today()

# Gets first 100 users, pagination used to grab the rest
result = client.get('/users')
query_results = result.json()

# Uses pagination within the graph call to get all users
pagination.pagination(query_results)


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
