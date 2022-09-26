from math import fabs
from xml.etree.ElementInclude import include
import requests
import json
import pprint
import urllib3
import datetime

urllib3.disable_warnings()

bigip_host = "you hostname or IP"
username = "admin"
hiddenpassword = "SomePassword"
policyName = ""
# Format is policyName = "?$filter=name eq policy-name"
# Leave it blank and it will iterate thru all of the policies
# or if you use a wildcard it will go thru a subset
# or the actual name will pull one policy


url = "https://" + bigip_host + "/mgmt/shared/authn/login"

payload = json.dumps({
    "username": username,
    "password": hiddenpassword,
    "loginProviderName": "tmos"
})
headers = {
    'Content-Type': 'application/json'
}

response = requests.request(
    "POST", url, headers=headers, data=payload, verify=False)

data = json.loads(response.text)
# pprint.pprint(data['token']['token'])

authToken = data['token']['token']

url = "https://" + bigip_host + "/mgmt/tm/asm/policies" + policyName

payload = {}
headers = {
    'Content-type': 'application/json',
    'X-F5-Auth-Token': authToken
}

response = requests.request(
    "GET", url, headers=headers, data=payload, verify=False)
policyData = json.loads(response.text)

for policy in policyData['items']:
    policyID = policy['id']
    policyName = policy['name']
    print("\n*********\nPolicy: " + policyName)
    url = "https://" + bigip_host + "/mgmt/tm/asm/policies/" + policyID + "/audit-logs/"

    payload = ""

    response = requests.request("GET", url, headers=headers, data=payload, verify=False, timeout=3600)

    auditRecs = json.loads(response.text)
    for auditItem in auditRecs['items']:
        pcDescription = auditItem['description']
        pcEventType = auditItem['eventType']
        pcTimeStamp = policy['lastUpdateMicros']

        print("\nPolicy change info (" + pcEventType + "): " + "\nChange Detail:" + pcDescription + "\nOn: " + str(datetime.datetime.fromtimestamp(pcTimeStamp/1000.0)))

