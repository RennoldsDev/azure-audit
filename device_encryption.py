from pagination import pagination_query


def get_device_encryption(graph_call, client, date):
    result = client.get(graph_call)
    query_results = result.json()

    pagination_query(query_results)
    devices = []

    for device in query_results['value']:
        devices.append(
            {
                'upn': device['userPrincipalName'],
                'device': device['deviceName'],
                'encrypted': device['encryptionState'],
                'dateRan': date,
            })

    return devices
