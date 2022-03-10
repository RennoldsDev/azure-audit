from pagination import pagination_query


def get_user_list(graph_call, client, date):
    result = client.get(graph_call)
    query_results = result.json()

    # Uses pagination within the graph call to get all users
    pagination_query(query_results)
    # Sets User list for appending information
    users = []

    for user in query_results['value']:
        if user['accountEnabled'] is True and user['jobTitle'] is not None:
            users.append(
                {
                    'upn': user['displayName'],
                    'displayName': user['userPrincipalName'],
                    'dateRan': date,
                }
            )
    return users
