import requests
import json
import argparse
import sys

flaws = {}
vulns = {}
vsum = {}
vulnlist = []

#
# This script is based on Azure DevOps Services REST API 6.0
##############################################################################
# Setup CLI Parser
# CLI Call (Usage): $python Pipeline2AzureWorkItems.py [-o Organization Name in Azure DevOps]
#                                                       [-p Project Name in Azure DevOps]
#                                                       [-t Work Item Type to Create] [-c Callback URI]
#                                                       [-a App ID to connect to Azure DevOps]
#                                                       [-i Client ID to connect to Azure DevOps]
#                                                       [-s Client Secret to connect to Azure DevOps]
#                                                       [-sc Scope configured when App was registered in Azure DeVops]
parser = argparse.ArgumentParser(description='Accept flags from CLI')
parser.add_argument('-o', action='store', help='Azure DevOps Organization where the Work item will '
                                               'be created', type=str)
parser.add_argument('-p', action='store', help='Azure DevOps Project where the Work item will be created', type=str)
parser.add_argument('-t', action='store', help='Azure DevOps Work item type. It is necessary to be '
                                               'sure that your Azure Project is created supporting '
                                               'the specified Work Item Type', type=str, default='task')
parser.add_argument('-token', action='store', help='Azure Pipeline Token used in pipeline execution', type=str)
parser.add_argument('-f', action='store', help='Full path to json file gotten from Pipeline Scan execution', type=str)
args = parser.parse_args()

if str(args.o) == "None":
    sys.exit("ERROR. A DevOps Organization is required!")
else:
    organization = str(args.o)

if str(args.p) == "None":
    sys.exit("ERROR. A DevOps Project is required!")
else:
    project = str(args.p)

if str(args.t) == "None":
    sys.exit("ERROR. A Work Item Type is required!")
else:
    myType = str(args.t)

if str(args.token) == "None":
    sys.exit("ERROR. A token is required!")
else:
    myToken = str(args.token)

if str(args.f) == "None":
    jsonFile = 'results.json'
else:
    jsonFile = str(args.f)

myUrl = 'https://dev.azure.com/' + organization + '/' + project + '/_apis/wit/workitems/$' + myType + '?api-version=6.0'
myHeader = {'Content-Type': 'application/json-patch+json', 'Authorization': 'Bearer ' + myToken}


def getjsondata():
    try:
        with open(jsonFile) as json_file:
            pipelinedata = json.load(json_file)
            # data2 = json.dumps(pipelinedata, indent=4)
            # print(data2)
            vulncount = 0
            if pipelinedata['scan_status'] == "SUCCESS":
                for v in pipelinedata['findings']:
                    title = v['title']
                    issueid = str(v['issue_id'])
                    severity = str(v['severity'])
                    if severity == "5":
                        sevname = "Very High"
                    elif severity == "4":
                        sevname = "High"
                    elif severity == "3":
                        sevname = "Medium"
                    elif severity == "2":
                        sevname = "Low"
                    elif severity == "1":
                        sevname = "Very Low"
                    elif severity == "0":
                        sevname = "Informational"
                    issuetype = v['issue_type']
                    cweid = v['cwe_id']
                    displaytext = v['display_text']
                    src = v['files']['source_file']['file']
                    if "/" in src:
                        src_file = src.split('/')
                        src_file_len = len(src_file)
                        file = ''.join(src_file[src_file_len - 1:])
                    elif "\\" in src:
                        src_file = src.split('\\')
                        src_file_len = len(src_file)
                        file = ''.join(src_file[src_file_len - 1:])
                    else:
                        src_file = src
                        file = src_file
                    path = src.replace(file, '')
                    line = str(v['files']['source_file']['line'])
                    qualifiedfunctionname = v['files']['source_file']['qualified_function_name']
                    functionprototype = v['files']['source_file']['function_prototype']
                    scope = v['files']['source_file']['scope']
                    flaws[vulncount] = {'title': title, 'issueid': issueid, 'severity': severity,
                                        'issuetype': issuetype, 'cweid': cweid, 'displaytext': displaytext,
                                        'file': file, 'path': path, 'line': line,
                                        'qualifiedfunctionname': qualifiedfunctionname,
                                        'functionprototype': functionprototype, 'scope': scope}
                    vulns[vulncount] = {'title': title, 'issueid': issueid, 'severity': sevname, 'issuetype': issuetype,
                                        'cweid': cweid, 'displaytext': displaytext, 'file': file, 'path': path,
                                        'line': line, 'qualifiedfunctionname': qualifiedfunctionname,
                                        'functionprototype': functionprototype, 'scope': scope}
                    vulnlist.append(
                        [str(cweid), str(sevname), str(title), str(issuetype), str(file), str(line), str(scope),
                         str(issueid)])
                    vulncount = vulncount + 1
            else:
                sys.exit("Pipeline scan status not successful")
    except:
        sys.exit("Error within capturing JSON data (see getjsondata)")


def processazureworkitems():
    try:
        for x in vulnlist:
            createworkitem(x[0], x[1], x[3], x[5], x[4], x[6], x[7])
    except:
        sys.exit("Error while creating work items - See createWorkItem")


def preparerequestbody(cwe_id, severity_name, issue_type, code_line, file_name, scope, issue_id):
    #
    # We are defining only Title and Description for Work Item.
    # Additional info can be added taking into account project scope.
    #
    rB = [
        {
            "op": "add",
            "path": "/fields/System.Title",
            "value": "Veracode Pipeline Scan - Flaw ID: " + issue_id
        },
        {
            "op": "add",
            "path": "/fields/System.Description",
            "value": "CWE: " + cwe_id + " - Severity: " + severity_name + " - Issue Type: " + issue_type +
                     " - File: " + file_name + " - Line: " + code_line + " - Scope: " + scope
        }
    ]
    return rB


def createworkitem(cwe_id, severity_name, issue_type, code_line, file_name, scope, issue_id):
#    try:
        # INCLUDE HERE API CALL TO CREATE WORK ITEM IN AZURE DEVOPS
        reqBody = preparerequestbody(cwe_id, severity_name, issue_type, code_line, file_name, scope, issue_id)
        myResponse = requests.post(myUrl, json=reqBody, headers=myHeader)
        print(myResponse.status_code)
#    except:
#        sys.exit("Error while creating work item in Azure DevOps!")


def main():
    #
    # Load JSON data
    #
    getjsondata()

    processazureworkitems()


main()
