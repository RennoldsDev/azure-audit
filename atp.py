from dotenv import load_dotenv
import os
import json
import urllib.request
import urllib.parse
import requests


load_dotenv()


# Function imported within main.py
def get_atp_status(date):
    # Uses environment variables stored in .env
    tenant_id = os.getenv('AZURE_TENANT_ID')
    app_id = os.getenv('AZURE_CLIENT_ID')
    app_secret = os.getenv('AZURE_CLIENT_SECRET')

    # The following until url was set from Microsoft Documentation here:
    # https://docs.microsoft.com/en-us/microsoft-365/security/defender-endpoint/run-advanced-query-sample-python?view=o365-worldwide)

    url = "https://login.microsoftonline.com/%s/oauth2/token" % (tenant_id)

    resource_app_id_uri = 'https://api.securitycenter.microsoft.com'

    body = {
        'resource': resource_app_id_uri,
        'client_id': app_id,
        'client_secret': app_secret,
        'grant_type': 'client_credentials'
    }

    data = urllib.parse.urlencode(body).encode("utf-8")

    req = urllib.request.Request(url, data)
    response = urllib.request.urlopen(req)
    json_response = json.loads(response.read())
    aad_token = json_response["access_token"]

    # End of documentation guide
    url = "https://api.securitycenter.microsoft.com/api/machines"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': "Bearer " + aad_token
    }

    response = requests.get(url, headers=headers)
    response_json = response.json()

    device_list = []

    for device in response_json['value']:
        device_list.append(
            {
                'device': device['computerDnsName'],
                'defenderStatus': device['onboardingStatus'],
                'dateRan': date
            })
    # Return device_list to be used in main.py
    return device_list
