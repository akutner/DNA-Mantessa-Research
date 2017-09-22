# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 13:07:11 2017

@author: akutn
"""
import csv
import os
import json
from urllib.request import urlopen

#from geopy.geocoders import Nominatim
#geolocator = Nominatim()
import pytz, datetime
"""
def findCounty(longitude, latitude):
    location = geolocator.reverse(longitude+","+latitude)
    print (location.raw)
    return ""
    """
    
def findCounty(lon, lat):

    components=[]
    components = getComponents(lon,lat,0)
    county="Not Found"
    for i in components:
        if str(i).find('administrative_area_level_2')!=-1:
            county = i['long_name']
    print(county)
    return county


def getComponents(lon,lat,numRequests):
    url = "https://maps.googleapis.com/maps/api/geocode/json?"
    url += "latlng=%s,%s&sensor=false&key=AIzaSyC635EKxxw0FcEqNEjTaoD0nvdH3NgMuBo" % (lat, lon)
    #c=httplib.HTTPSConnection(url)
    #c.request("GET","/")
    #v=c.getresponse.read()
    v = urlopen(url).read()
    j = json.loads(v)
    numRequests+=1
    try:
        components = j['results'][0]['address_components']
    except:
        print(j)
        quitAndSave()
        if numRequests>10:
            quitAndSave();
        getComponents(lon,lat,numRequests)

    return components
def quitAndSave():
    with open('ipData.json','w') as outfile:
                json.dump(countiesCustomers,outfile)

def makeStdTime(tm):
    gmt = pytz.timezone('GMT')
    est = pytz.timezone('US/Eastern')
    year = tm[0:4]
    month= tm[4:6]
    day = tm[6:8]
    tym=month+"/"+day+"/"+year+" "+tm[9:17]
    fmt='%m/%d/%Y %H_%M_%S'
    date = datetime.datetime.strptime(tym, fmt)
    date = gmt.localize(date)
    fTime = date.astimezone(est)
    newFmt='%m/%d/%Y %H:%M'
    return fTime.strftime(newFmt)

directory="C:\\Users\\akutn\\Documents\\My Docs\\Academics\\Network Research\\ip-data"

info=[]
filename= "ips-annotated.txt"
with open(directory+"\\"+filename) as data:
    info=data.readlines()
writeTo=open('scan-irma-data.csv','w')
writer = csv.writer(writeTo, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
curLsIP=open('ipData.json','r')
countiesCustomers = json.loads(curLsIP.read())
countiesTot={}#county=> total IP in county
for ip in countiesCustomers:
    county = countiesCustomers[ip]
    if county in countiesTot.keys():
            countiesTot[county]+=1
    else:
        countiesTot[county] = 1

for line in info:
    ln=line.split(",")
    long = ln[1]
    lat = ln[2]
    ip=ln[0]
    if not ip in countiesCustomers.keys():
        county = findCounty(long,lat)
        countiesCustomers[ip]=county
        if county in countiesTot.keys():
            countiesTot[county]+=1
        else:
            countiesTot[county] = 1
    
directory_of_data="C:\\Users\\akutn\\Documents\\My Docs\\Academics\\Network Research\\ip-data\\ips-datetime\\scan-data"
countiesNumUp={}#county=> total county up
for file in os.listdir(directory_of_data):
    filename=os.fsdecode(file)
    with open(directory_of_data+"\\"+filename) as ips:
        lsIP=ips.readlines()
    
    for county in countiesTot.keys():#sets all counties up to 0
        countiesNumUp[county]=0
        print (county)
        
        
    for ip in lsIP:#find's associated ip with county and increments
        ip=ip.replace('\n',"")
        county = countiesCustomers[ip]
        countiesNumUp[county]+=1
    
    
    for county in countiesTot.keys():
        timestamp=makeStdTime(filename)#plus some function?
        writer.writerow([county,timestamp,str(countiesNumUp[county]),str(countiesTot[county])])
        
writeTo.close()
            
    
    
        