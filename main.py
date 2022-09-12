
from math import fabs
from xml.etree.ElementInclude import include
import requests
import json
import pprint

bigip_host = "HostName_or_IP"
username = "admin"
hiddenpassword = "SetYourPassword"
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

response = requests.request("POST", url, headers=headers, data=payload, verify=False)

data = json.loads(response.text)
# pprint.pprint(data['token']['token'])

authToken = data['token']['token']

# print(authToken)

# Get the Policy / Policies

url = "https://" + bigip_host + "/mgmt/tm/asm/policies" + policyName

payload={}
headers = {
  'Content-Type': 'application/json',
  'X-F5-Auth-Token' : authToken
}
response = requests.request("GET", url, headers=headers, data=payload, verify=False)
policyData = json.loads(response.text)

for policy in policyData['items']:
    policyID = policy['id']
    url = "https://" + bigip_host + "/mgmt/tm/asm/policies/" + policyID + "/signatures/"

    payload = ""

    response = requests.request("GET", url, headers=headers, data=payload, verify=False)

    sigs = json.loads(response.text)
    for sig in sigs['items']:
        print(policy['name'] + " -- Signature: " + sig['signatureReference']['name'] + ":" + str(sig['signatureReference']['signatureId']) + " (blocking=" + str(sig['block']) + ")" )

