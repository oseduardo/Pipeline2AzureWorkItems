import sys
import json
import requests

myUrl='https://dev.azure.com/oscarrodriguezarias/PipelineScan2AzureWorkItems/_apis/wit/workitems/${type}?api-version=6.0'
myHeader={'Content-Type': 'application/json-patch+json'}
data=[
    {
        "op": "add",
        "path": "/fields/System.Title",
        "value": "Sample Task"
    }
]

def createWorkItem():
    try:
        myResponse = requests.post(myUrl,json=data,headers=myHeader)
        print(myResponse.json())
    except:
        sys.exit('Error while creating Work Item!')

def main():
    createWorkItem()

main()