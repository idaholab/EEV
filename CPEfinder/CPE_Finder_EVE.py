# Copyright 2026, Battelle Energy Alliance, LLC, ALL RIGHTS RESERVED

################### Modify NVD API Key as needed
API_KEY = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
####################################

import sys, nvdlib, os, json, re
maxDist = 5
searchLimit = 20

def searchNVD(searchString):
    print('Searching NVD for: ' + searchString)
        
    r = nvdlib.searchCPE(keywordSearch = searchString, key=API_KEY, delay=1, limit=searchLimit)

    cveList = []
    cpeList = []
    print(str(len(r)) + ' CPEs Found')
    for eachCPE in r:
        cpeList.append(eachCPE.cpeName)
        print('   ' + eachCPE.cpeName)      
        while True:
            try:
                q = nvdlib.searchCVE(cpeName = eachCPE.cpeName, key=API_KEY, delay=1, limit=searchLimit)
            except:
                print("      Timeout Error Occurred - Trying Again")
                continue
            break
        for eachCVE in q:
            cveList.append(eachCVE.id)

    cveList = list(set(cveList))
    print(str(len(cveList)) + ' CVEs Found')
    for cve in cveList:
        print('   ' + str(cve))
        
    print("-----------------------------------------------------------------")
    
    return cveList, list(set(cpeList))

def findall(pattern, string):
    i = string.find(pattern)
    while i != -1:
        yield i
        i = string.find(pattern, i+1)

def makeLists(inputDictPath):
    vendorList = []
    productList = []
    inFile = open(inputDictPath, "r", errors='replace')
    Lines = inFile.readlines()
    for line in Lines:
        vendorList.append(line.split("::")[0])
        productList.append(line.split("::")[1].strip())
        
    return vendorList, productList

def searchLists(descTemp, vendorList, productList):
    inTextString = descTemp.lower()
    
    fullMatchDict = {}
    combinedListofLists = []
    
    for i in range(0, len(vendorList)):
        if (re.search(r"\b" + re.escape(vendorList[i]) + r"\b", inTextString)) and (re.search(r"\b" + re.escape(productList[i]) + r"\b", inTextString)):
            v_start_pos = list(findall(vendorList[i], inTextString))
            p_start_pos = list(findall(productList[i], inTextString))
            v_end_pos = [int(x) + len(vendorList[i]) for x in v_start_pos]
            p_end_pos = [int(x) + len(productList[i]) for x in p_start_pos]
            
            smallestDist = 10000000000
            for p in p_start_pos:
                for v in v_end_pos:
                    if smallestDist > p - v and p - v > -1:
                        smallestDist = p - v
            for v in v_start_pos:
                for p in p_end_pos:
                    if smallestDist > v - p and v - p > -1:
                        smallestDist = v - p
                
            if smallestDist < maxDist:
                print("Full CPE Database Match Found (Distance apart: " + str(smallestDist) + "): " + vendorList[i] + ":" + productList[i])
                
                cveList, cpeList = searchNVD(vendorList[i] + " " + productList[i])
                combinedListofLists.append(cveList)
                combinedListofLists.append(cpeList)
                
            elif smallestDist >= maxDist and smallestDist != 10000000000:
                print("Potential Full CPE Database Match Found (Distance apart: " + str(smallestDist) + "): " + vendorList[i] + ":" + productList[i])
            elif smallestDist == 10000000000:
                pass

    productMatchList = []
    vendorMatchList = []        
    for i in range(0, len(vendorList)):
        if re.search(r"\b" + re.escape(vendorList[i]) + r"\b", inTextString):
            if vendorList[i] not in vendorMatchList:
                vendorMatchList.append(vendorList[i])
                print("Potential CPE Database Vendor Match Found: " + vendorList[i] + "  (" + vendorList[i] + "::" + productList[i] + ")")
                
        if re.search(r"\b" + re.escape(productList[i]) + r"\b", inTextString):
            if productList[i] not in productMatchList:
                productMatchList.append(productList[i])
                print("Potential CPE Database Product Match Found: " + productList[i] + "  (" + vendorList[i] + "::" + productList[i] + ")")
                    
    return combinedListofLists

# Start ##############################################
try:
    inputDictPath = sys.argv[1]
    inputJSON = sys.argv[2]
except:
    print("Missing Argument(s)")
    exit()
    
try:
    outputJSON = sys.argv[3]
except:
    outputJSON = inputJSON

if os.path.isfile(inputDictPath):
    vendorList, productList = makeLists(inputDictPath)
else:
    print("Error: File Does Not Exist")
    exit()

#Load Bundle
json_dict = json.load(open(inputJSON, 'r', errors='replace'))

#Locate Vulnerability Objects UUID from input JSON file
cveDict = {}
for j in json_dict["objects"]:
    if j["type"] == "vulnerability":
        descTemp = j["description"]
        
        combinedListofLists = searchLists(descTemp, vendorList, productList)
        
        try:
            j["external_references"]
        except:
            j["external_references"] = []
        
        try:
            if not {"source_name":"potential_cve","external_id":(",").join(sorted(combinedListofLists[0]))} in j["external_references"]:
                j["external_references"].append({"source_name":"potential_cve","external_id":(",").join(sorted(combinedListofLists[0]))})
        
            if not {"source_name":"potential_cpe","external_id":(",").join(sorted(combinedListofLists[1]))} in j["external_references"]:
                j["external_references"].append({"source_name":"potential_cpe","external_id":(",").join(sorted(combinedListofLists[1]))})
        except:
            #Remove Blank "External Reference" Entry
            if j["external_references"] == []:
                del j["external_references"]
        
#Save bundle to file
outFile = open(outputJSON, 'w')
outString = str(json.dumps(json_dict, sort_keys=True, indent=4))
outFile.write(outString)
outFile.close()
