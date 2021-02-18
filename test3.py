import sys
import json
import requests
import argparse

parser = argparse.ArgumentParser(description='Accept flags from CLI')
parser.add_argument('-t', action='store', help='Azure Pipeline Token', type=str)
args = parser.parse_args()

if str(args.t) == "None":
    sys.exit("ERROR. A token is required!")
else:
    myToken = str(args.t)

myUrl='https://dev.azure.com/oscarrodriguezarias/PipelineScan2AzureWorkItems/_apis/wit/workitems/$bug?api-version=6.0'
myHeader={'Content-Type': 'application/json-patch+json', 'Authorization': 'Bearer ' + myToken}
data=[
    {
        "op": "add",
        "path": "/fields/System.Title",
        "value": "Sample Bug"
    }
]

def createWorkItem():
    myResponse = requests.post(myUrl,json=data,headers=myHeader)
    #print(myResponse.json())
    print(myResponse.text)

def main():
    createWorkItem()

main()