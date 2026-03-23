# Copyright 2026, Battelle Energy Alliance, LLC, ALL RIGHTS RESERVED

import sys, os
from urllib import request

try:
    print("Downloading CPE Dictionary XML...")
    response = request.urlretrieve("https://nvd.nist.gov/feeds/xml/cpe/dictionary/official-cpe-dictionary_v2.3.xml.zip","CPEDict.zip")
    print("Unzipping CPE Dictionary ZIP...")
    os.system('unzip -j CPEDict.zip -d . >/dev/null 2>&1')
    os.remove("CPEDict.zip")
except:
    pass

outFile = open("CPE_Dictionary.csv", "w", errors='replace')
tempList = []

print("Processing File...")
inFile = open('official-cpe-dictionary_v2.3.xml', "r", errors='replace')
    
Lines = inFile.readlines()
 
for line in Lines:
    if line.startswith("    <cpe-23:"):
        line = line.split("cpe:2.3")[1].split(":")
        line = line[2] + "::" + line[3]
        if line not in tempList:
            tempList.append(line)
            outFile.write(str(line) + "\n")

os.remove("official-cpe-dictionary_v2.3.xml")

print("Processing Complete.")
