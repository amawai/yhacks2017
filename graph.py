import json
import xml.etree.ElementTree
import csv
from pprint import pprint
import pymongo
from pymongo import MongoClient
import pandas as pd
import os, json

client = MongoClient('localhost', 27017)
db = client.YHack
collection = db.ActualCorporations
bannedBrokers = db.BannedBrokers
courtCases = db.CourtCases
investors = db.Investors

# Uploads data to database assuming the right files are in the right place
# uncomment to upload investors to database
"""
tree = xml.etree.ElementTree.parse('IAPD/IA_INDVL_Feed_10_11_2017.xml/IA_Indvl_Feeds20.xml')
e = tree.getroot()
investorList = []
for ind in e.iter("Indvl"):
    investor = {}
    pasts = []
    for empHss in ind.iter('EmpHss'):
        for empHs in empHss:
            past = {}
            past['orgNm'] = empHs.attrib['orgNm']
            past['fromDt'] = empHs.attrib['orgNm']
            pasts.append(past)
    currents = []     
    for crntEmps in ind.iter('CrntEmps'):
        for crntEmp in crntEmps:
            current = {}
            current['orgNm'] = crntEmp.attrib['orgNm']
            currents.append(current)
    for info in ind.iter('Info'):
        investor["indvlPK"] = info.attrib['indvlPK']
        investor["firstNm"] = info.attrib['firstNm']
        investor["lastNm"] = info.attrib['lastNm']
    investor["currentEmployment"] = currents 
    investor["employmentHistory"] = pasts       
    investorList.append(investor)
result = investors.insert_many(investorList)
"""

# uncomment to upload court cases to database
"""
path_to_folders = 'CourtListner/clusters-all'
dirlist = [ item for item in os.listdir(path_to_folders) if os.path.isdir(os.path.join(path_to_folders, item)) ]
for court in dirlist:
    path_to_json = os.path.join(path_to_folders, court)
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    jsons_data = pd.DataFrame(columns=['date_filed', 'slug', 'nature_of_suit', 'date_blocked'])
    for index, js in enumerate(json_files):
        with open(os.path.join(path_to_json, js)) as json_file:
            json_text = json.load(json_file)
            result = courtCases.insert_one(json_text)

"""

# uncomment to upload active corps to database
"""
csv_file = 'NY Firms/Active_Corporations.csv'
with open(csv_file, 'r') as csvfile:
    spamreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    result = collection.insert_many(spamreader)

"""

# uncomment to upload banned brokers to database
"""
csv_file = 'BannedBrokers/barred_individuals_20170930.csv'
with open(csv_file, 'r') as csvfile:
    spamreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    result = bannedBrokers.insert_many(spamreader)

"""






