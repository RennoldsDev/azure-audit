from datetime import date as date
import pagination


def get_user_list(graph_call, client):
    result = client.get(graph_call)
    query_results = result.json()

    # Uses pagination within the graph call to get all users
    pagination.pagination(query_results)
    # Sets User list for appending information
    user_list = []

    for user in query_results['value']:
        if user['accountEnabled'] is True and user['jobTitle'] is not None:
            user_list.append(
                {
                    'upn': user['displayName'],
                    'displayName': user['userPrincipalName'],
                    'dateRan': date.today(),
                }
            )
    return user_list
