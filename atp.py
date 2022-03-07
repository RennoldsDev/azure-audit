from dotenv import load_dotenv
import os
import json
import urllib.request
import urllib.parse
import requests
from datetime import date

load_dotenv()


def get_atp_status():
    tenant_id = os.getenv('TENANTID')
    app_id = os.getenv('APPID')
    app_secret = os.getenv('SECRET')

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

    url = "https://api.securitycenter.microsoft.com/api/machines"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': "Bearer " + aad_token
    }

    response = requests.get(url, headers=headers)
    response_json = response.json()

    user_dict = []

    for device in response_json['value']:
        user_dict.append(
            {
                'device': device['computerDnsName'],
                'defenderStatus': device['onboardingStatus'],
                'dateRan': date.today()
            })
    return user_dict
