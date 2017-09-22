
#Alexander Kutner ak3987
#prompts user for directory of files to process into .csv

import os
import json
import csv

directory_in_str=input("Enter directory of raw data files: ")

def isolateJSON(str):
    start = "define("
    end = ");"
    startCut=len(start)
    str=str[0]
    str=str[startCut:]
    str=str.replace(end,"")
    return str


directory = os.fsencode(directory_in_str)
writeTo=open('flpa-irma-data.csv','w')
writer = csv.writer(writeTo, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
for file in os.listdir(directory):
    filename=os.fsdecode(file)
    with open(directory_in_str+"\\"+filename) as data:
        js = data.readlines()
        js=isolateJSON(js)
    parsed_json=json.loads(js)
    counties=parsed_json['counties']
    timestamp=parsed_json['lastupdated']
    for county in counties:
        writer.writerow([counties[county]['name'],timestamp,str(counties[county]['numberofoutages']),str(counties[county]['numberofaccounts'])])


writeTo.close()

print("flpa-irene-data.csv written to current directory")