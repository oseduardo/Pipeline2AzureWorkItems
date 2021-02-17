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
    myResponse = requests.post(myUrl,json=data,headers=myHeader)
    #print(myResponse.json())
    print(myResponse.text)

def main():
    createWorkItem()

main()