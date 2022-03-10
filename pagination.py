from azure.identity import EnvironmentCredential
from msgraph.core import GraphClient, APIVersion
from dotenv import load_dotenv

load_dotenv()
credential = EnvironmentCredential()
client = GraphClient(credential=credential, api_version=APIVersion.beta)


# Uses pagination within the graph call to get all users
def pagination_query(initial_result):

    while '@odata.nextLink' in initial_result.keys():
        paginated_query = client.get(initial_result['@odata.nextLink'])
        paginated_results = paginated_query.json()
        if '@odata.nextLink' in paginated_results:
            initial_result['@odata.nextLink'] = paginated_results['@odata.nextLink']
        else:
            del initial_result['@odata.nextLink']
        initial_result['value'].extend(paginated_results['value'])
