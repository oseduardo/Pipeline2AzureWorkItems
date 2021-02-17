import requests
import json
import argparse
import sys

#This script is based on Azure DevOps Services REST API 6.0
authorize_url = "https://app.vssps.visualstudio.com/oauth2/authorize"
token_url = "https://app.vssps.visualstudio.com/oauth2/token"

##############################################################################
# Setup CLI Parser
# CLI Call (Usage): $python Pipeline2AzureWorkItems.py [-o Organization Name in Azure DevOps] [-p Project Name in Azure DevOps]
#                                                       [-t Work Item Type to Create] [-c Callback URI]
#                                                       [-a App ID to connect to Azure DevOps]
#                                                       [-i Client ID to connect to Azure DevOps]
#                                                       [-s Client Secret to connect to Azure DevOps]
#                                                       [-sc Scope configured when App was registered in Azure DeVops]
parser = argparse.ArgumentParser(description='Accept flags from CLI')
parser.add_argument('-o', action='store', help='Azure DevOps Organization where the Work item will be created', type=str)
parser.add_argument('-p', action='store', help='Azure DevOps Project where the Work item will be created', type=str)
parser.add_argument('-t', action='store', help='Azure DevOps Work item type', type=str, default='Task')
parser.add_argument('-c', action='store', help='Callback URI when the application was defined in Azure DevOps', type=str)
parser.add_argument('-a', action='store', help='App ID', type=str)
parser.add_argument('-i', action='store', help='Client ID', type=str)
parser.add_argument('-s', action='store', help='Client Secret', type=str)
parser.add_argument('-sc', action='store', help='Scope for App registered in Azure DevOps', type=str)
parser.add_argument('-pat', action='store', help='Personal Token Authentication to access to Azure Services APIs', type=str)
args = parser.parse_args()

organization = "oscarrodriguezarias"
#if str(args.o) == "None":
#    sys.exit("ERROR. A DevOps Organization is required!")
#else:
#    organization = str(args.o)

project = "verademo"
#if str(args.p) == "None":
#    sys.exit("ERROR. A DevOps Project is required!")
#else:
#    project = str(args.p)

type = "task"
#if str(args.t) == "None":
#    sys.exit("ERROR. A Work Item Type is required!")
#else:
#    type = str(args.t)

#callback url specified when the application was defined
callback_uri = "https://www.veracode.com"
#if str(args.c) == "None":
#    sys.exit("ERROR. A Callback URI is required!")
#else:
#    callback_uri = str(args.c)

#App ID for connecting to Azure DevOps
app_id = "77EFB79A-99CA-4485-BF0F-5E469FE24B5D"
#if str(args.a) == "None":
#    sys.exit("ERROR. App ID is required!")
#else:
#    app_id = str(args.a)

#Client ID for connecting to Azure DevOps
client_id = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIs"
#if str(args.i) == "None":
#    sys.exit("ERROR. Client ID is required!")
#else:
#    client_id = str(args.i)

#Client Secret for connecting to Azure DevOps
client_secret = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Im9PdmN6NU1fN3AtSGpJS2xGWHo5M3VfVjBabyJ9.eyJjaWQiOiI3N2VmYjc5YS05OWNhLTQ0ODUtYmYwZi01ZTQ2OWZlMjRiNWQiLCJjc2kiOiI2M2ViNWY1OS01YzMxLTQzN2QtYWRmNi1hM2E5MmVjNTAzMDEiLCJuYW1laWQiOiJhNGMzNmVjNi01ZmNkLTY0NjYtYmU1Mi1iZjBhMTI2M2JmZDYiLCJpc3MiOiJhcHAudnN0b2tlbi52aXN1YWxzdHVkaW8uY29tIiwiYXVkIjoiYXBwLnZzdG9rZW4udmlzdWFsc3R1ZGlvLmNvbSIsIm5iZiI6MTYwODU2ODkyMywiZXhwIjoxNzY2MzM1MzIzfQ.JKN8opuv-xNb1xUxfWl6dwhR8gh77yFg0V7RmGzO9QFq5F14AOIWpsVDHRM4Gi3_Wue07qV1r30CukQpWYd20OLIvZYzr4O4UVB5-5q54Ou1hxaVBczVorAuuG_zJUa0PDfY_yuu2LmeUlDVmmSLr7Ibx5B9gbq7i7mpT3HzRAnlbxY0eDc0UaMrBvuwKFJeGmHdzxsAlAp9oUVNVZ1mcgZP7Pr02txjKIDwJ9ssRSQu4NbvxjM8OHZcv4ozos6LtB9kK1dLZOoo23zaqQirgkR-DsCglwSuANNcg8RsQPp5e1_KsKcPGrl-nHwYEVqbdfcPUpLqqJzdcZ7SiuWegQ"
#if str(args.s) == "None":
#    sys.exit("ERROR. Client Secret is required!")
#else:
#    client_secret = str(args.s)

#Scope for App registered in Azure DevOps
scope = "vso.work_full"
#if str(args.sc) == "None":
#    sys.exit("ERROR. Scope is required!")
#else:
#    scope = str(args.sc)

#Personal Token Access to authenticate to Azure DevOps Service APIs
pat = "hnalx7h7w4no6tk54tqwc25rsgztcqc6qzfuipnykb3bj5zznpaq"
#if str(args.pat) == "None":
#    sys.exit("ERROR. Personal Access Token is required!")
#else:
#    pat = str(args.pat)
##############################################################################

#token_url_payload = str.format("client_assertion_type=urn:ietf:params:oauth:client-assertion-type:jwt-bearer&client_assertion={0}&grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer&assertion={1}&redirect_uri={2}", client_secret.encode(encoding="ascii",errors="strict"))

json_body = "[  {    '"'op'"': '"'add'"',    '"'path'"': '"'/fields/System.Title'"',    '"'from'"': null,    '"'value'"': '"'Sample task'"'  }  ]"

create_work_item_api_url = "https://dev.azure.com/" + organization.encode(encoding="ascii",errors="strict") + "/" + project.encode(encoding="ascii",errors="strict") + "/_apis/wit/workitems/$" + type.encode(encoding="ascii",errors="strict") + "?validateOnly=false&bypassRules=false&suppressNotifications=false&$expand=none&api-version=6.0"
create_work_item_response = requests.post(create_work_item_api_url, headers={"Content-Type": "application/json"}, json=json.dumps(json_body), auth=('',pat.encode(encoding="base64_codec",errors="strict")))
print create_work_item_response.status_code

#step A - simulate a request from a browser on the authorize_url - will return an authorization code after the user is
# prompted for credentials.

#authorization_redirect_url = authorize_url.encode(encoding="ascii",errors="strict") + '?response_type=Assertion&client_id=' + app_id.encode(encoding="ascii",errors="strict") + '&redirect_uri=' + callback_uri.encode(encoding="ascii",errors="strict") + '&scope=' + scope.encode(encoding="ascii",errors="strict")
#authorization_response = requests.get(authorization_redirect_url)
#print "Results of authorization response.... Authorization URL: " + authorization_redirect_url
#print authorization_response.status_code
#print authorization_response.text

#print "go to the following url on the browser and enter the code from the returned url: "
#print "---  " + authorization_redirect_url + "  ---"
#authorization_code = raw_input('code: ')

# step I, J - turn the authorization code into a access token, etc
data = {'grant_type': 'authorization_code', 'code': authorization_code, 'redirect_uri': callback_uri}
print "requesting access token"
access_token_response = requests.post(token_url, data=data, verify=False, allow_redirects=False, auth=(client_id, client_secret))

#print "response"
#print access_token_response.headers
#print 'body: ' + access_token_response.text

# we can now use the access_token as much as we want to access protected resources.
#tokens = json.loads(access_token_response.text)
#access_token = tokens['access_token']
#print "access token: " + access_token

#api_call_headers = {'Authorization': 'Bearer ' + access_token}
#api_call_response = requests.get(create_work_item_api_url, headers=api_call_headers, verify=False)

#print api_call_response.text
