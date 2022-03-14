from pagination import pagination_query


def get_membership_list(client, group_id, group_name, date):
    graph_call = f'/groups/{group_id}/members'
    result = client.get(graph_call)
    query_results = result.json()

    # Uses pagination within the graph call to get all users
    pagination_query(query_results)
    # Sets User list for appending information
    users = []

    for user in query_results['value']:
        users.append(
            {
                'upn': user['displayName'],
                'displayName': user['userPrincipalName'],
                'group': group_name,
                'dateRan': date,

            }
        )
    return users
