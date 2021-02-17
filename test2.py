import requests
import os
import base64
import json

personal_access_token = "hnalx7h7w4no6tk54tqwc25rsgztcqc6qzfuipnykb3bj5zznpaq"
headers = {}
headers['Content-type'] = "application/json"
headers['Authorization'] = b'Basic ' + base64.b64encode(personal_access_token.encode('utf-8'))

#Get a list of agent pools.
instance = "dev.azure.com/oscarrodriguezarias"
project = "verademo"
work_items_ids = "1"
api_version = "6.0"
url = ("https://%s/%s/_apis/wit/workitems?ids=%s&api-version=%s" % (instance, project, work_items_ids, api_version))

r = requests.get(url, headers=headers)

print("r.status_code is: ", r.status_code)
print r.content