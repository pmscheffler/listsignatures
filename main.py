
from math import fabs
from xml.etree.ElementInclude import include
import requests
import json
import pprint
import re 
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

bigip_host = "BIG-IP.Host_or_IP"
username = "admin"
hiddenpassword = "SuperSecretPassword"
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
      # pull the signature reference link and parse out the ID from the end
      fullSignatureUrl = sig['signatureReference']['link']
      stepOne = re.split('[?]', fullSignatureUrl)
      stepTwo = re.split('[/]', stepOne[0])
      signatureId = stepTwo.pop()

      sigurl  = "https://" + bigip_host + "/mgmt/tm/asm/signatures/" + signatureId

      payload = ""
      sigResponse = requests.request("GET", sigurl, headers=headers, data=payload, verify=False)
      sigData = json.loads(sigResponse.text)

      print(policy['name'] + " -- Signature: " + sig['signatureReference']['name'] + ":" + str(sig['signatureReference']['signatureId']) + ": Attack Type: " + str(sigData["attackTypeReference"]["name"]) + ": Accuracy: " + str(sigData["accuracy"]) + " (blocking=" + str(sig['block']) + ")" )
