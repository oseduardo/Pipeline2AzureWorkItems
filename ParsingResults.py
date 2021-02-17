import sys
import json
import argparse

flaws = {}
vulns = {}
vsum = {}
vulnlist = []
topflawlist = []
top25list = ['79', '787', '20', '125', '119', '89', '200', '416', '352', '78', '190', '22', '476', '287', '434', '732',
             '94', '522', '611', '798', '502', '269', '400', '306', '862']

jsonfile = "results.json"


# if str(jsonfile) == "None":
#	jsonfile = 'results.json'
# else:
#	jsonfile = str(args.f)

#
# IMPORT JSON AND CAPTURE DATA
#
def getJSONdata():
    try:
        with open(jsonfile) as json_file:
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
                        [str(cweid), str(sevname), str(title), str(issuetype), str(file), str(line), str(scope), str(issueid)])
                    vulncount = vulncount + 1
            else:
                sys.exit("Pipeline scan status not successful")
    except:
        sys.exit("Error within capturing JSON data (see getJSONdata)")

def processAzureWorkItems():
	try:
		for x in vulnlist:
			createWorkItem(x[0],x[1],x[3],x[5],x[4],x[6],x[7])
	except:
		sys.exit("Error while creating work items - See createWorkItem")

def createWorkItem(cwe_id,severity_name,issue_type,code_line,file_name,scope,issue_id):
	try:
		#INCLUDE HERE API CALL TO CREATE WORK ITEM IN AZURE DEVOPS -
		reqBody=prepareRequestBody(cwe_id,severity_name,issue_type,code_line,file_name,scope,issue_id)
		print reqBody
		#print "[\"" + issue_id + "\", \"" + cwe_id + "\", \"" + severity_name + "\", \"" + issue_type + "\", \"" + code_line + "\", \"" + \
		#	  file_name + "\", \"" + scope + "\"]"
	except:
		sys.exit("Error while creating work item in Azure DevOps!")

def prepareRequestBody(cwe_id,severity_name,issue_type,code_line,file_name,scope,issue_id):
	#
	#We are defining only Title and Description for Work Item.
	#Additional info can be added taking into account project scope.
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
			"value": "CWE: " + cwe_id + " - Severity: " + severity_name + " - Issue Type: " + issue_type + \
					 " - File: " + file_name + " - Line: " + code_line + " - Scope: " + scope
		}
	]
	return rB

def main():
    #
    # Load JSON data
    #
    getJSONdata()

    processAzureWorkItems()

main()
