from math import fabs
from xml.etree.ElementInclude import include
import requests
import json
import pprint

bigip_host = "yourhost"
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

    policyName = policy['name']
    policyLastChange = policy['versionLastChange']
    policyTimeStamp = policy['versionDatetime']

    print("\n*********\n\nPolicy change info: " + policyName + "\nChange Detail:" + policyLastChange + "\nOn: " + policyTimeStamp)

