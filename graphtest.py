import networkx as nx
from pprint import pprint
import string
from math import exp
import numpy as np
import pymongo
from pymongo import MongoClient
import csv
G = nx.Graph()

client = MongoClient('localhost', 27017)
db = client.YHack
actualCorporations = db.ActualCorporations
courtCases = db.CourtCases
investors = db.Investors
bannedBrokers = db.BannedBrokers

CORP_PENALTY_STEP = 0.1 #Suspicion points
pplDict = {}
corpDict = {}
bannedPpl = ["BARBARA JEAN ABADI", "JOSEPH ABBONDANTE", "EMMETT MAURICE ABERCROMBIE", "ANDREW MARTIN ABERN"]
class Person:
    def __init__(self, crd, firstName, lastName, currentEmp, factor):
        self.crd = crd
        self.firstName = firstName
        self.lastName = lastName
        self.currentEmp = currentEmp
        self.empHistory = {}
        self.factor = factor
        #self.pplAssociation = []

    def getName(self):
        return self.firstName + " " + self.lastName

    def addToEmployeeHistory(self, corpName, startDate):
        self.empHistory[corpName] = startDate

    def addToFactor(self, suspicion):
        self.factor += suspicion

    def getCurrentEmployment(self):
        return self.currentEmp

    def getEmpHistory(self):
        return self.empHistory

    def getFactor(self):
        if (self.currentEmp in corpDict):
            corpFactor = self.factor + corpDict[self.currentEmp].getFactor()
        else:
            corpFactor = 1
        return max(0., min(1., corpFactor))

class Corporation:
    def __init__(self, corpId, corpName, city, factor):
        self.corpId = corpId
        self.corpName = corpName
        self.city = city
        self.factor = factor
        self.courtAppearances = 0
        self.courtAppearanceId = []

    def addCourtCitation(self, citationId):
        self.courtAppearances += 1
        self.courtAppearanceId.append(citationId)
        self.factor += CORP_PENALTY_STEP

    def getFactor(self):
        return self.factor

def computeNodes():
    temp = bannedBrokers.find({}, {"_id": False}, 0, 100)
    bannedPpl = []
    for bb in temp:
        bannedPpl.append(bb['Individual Name'])
    for person in bannedPpl:
        G.add_node(person)
        #temporary measure:
        if (person == "BARBARA JEAN ABADI"):
            pplDict[person] = Person(12, person.split(' ')[0], ' '.join(person.split(' ')[1:]), 'Succ it', 1)
        elif (person == "JOSEPH ABBONDANTE"):
            pplDict[person] = Person(12, person.split(' ')[0], ' '.join(person.split(' ')[1:]), 'Eat it', 1)
        elif (person == "ANDREW MARTIN ABERN"):
            pplDict[person] = Person(12, person.split(' ')[0], ' '.join(person.split(' ')[1:]), 'Eat it', 1)
        else:
            pplDict[person] = Person(12, person.split(' ')[0], ' '.join(person.split(' ')[1:]), 'Succ it', 1)


    temp4 = investors.find({}, {"_id": False}, 0, 100)
    iapd = []
    for i in temp4:
        iapd.append(i)
    iapdPerson = None

    #Add corporations to the dictionary
    temp2 = actualCorporations.find({})
    corps = []
    for c in temp2:
        corps.append(c)
    temp3 = courtCases.find({}, {"_id": False}, 0, 100)
    courtDates = []
    for cc in temp3:
        courtDates.append(cc)
    for corp in corps:
        corpDict[corp['DOS Process Name']] = Corporation(corp['DOS ID'], corp['DOS Process Name'], corp['DOS Process City'], 0)
        for courts in courtDates:
            #Putting the corp name into slug format found in json
            if (len(courts['slug']) > 1 and courts['slug'].find('-v-') != -1):
                if (courts['slug'].split('-v-')[1] == '-'.join(corp['DOS Process Name'].split(' ')).lower()):
                    #If the corp was a defendent, it sounds... sketch af
                    corpDict[corp['DOS Process Name']].addCourtCitation(courts['citation_id'])

    #Adding everybody as a node in the network
    for person in iapd:
        if (len(person['currentEmployment']) == 0):
            iapdPerson = Person(person['indvlPK'], person['firstNm'], person['lastNm'], "unknown", 0)
        elif (person['currentEmployment'][0]['orgNm'] in corpDict):
            iapdPerson = Person(person['indvlPK'], person['firstNm'], person['lastNm'], corpDict[person['currentEmployment'][0]['orgNm']].__dict__['corpName'], 0)
        else:
            iapdPerson = Person(person['indvlPK'], person['firstNm'], person['lastNm'], "unknown", 0)
        if (len(person['employmentHistory']) != 0):
            for corp in person['employmentHistory']:
                if (corp['orgNm'] in corpDict):
                    iapdPerson.addToEmployeeHistory(corp['orgNm'], corp['fromDt'])
        name = (person['firstNm'] + ' ' + person['lastNm']).upper()
        pplDict[name] = iapdPerson
        G.add_node(iapdPerson)



    #Currently, we have nodes representing everybody in our network, but no edges/connections
    #We also have a dictionary of corporations with a suspicious factor calculated based on court appearances as a defendant

    # Assume suspicion is initialized somewhere as a dictionary of nodes to float
    suspicion = list(G.nodes())
    print("Entering the danger zone")
    for person in pplDict.values():
        for otherPerson in pplDict.values():
            if (otherPerson != person):
                if (person.getCurrentEmployment() == otherPerson.getCurrentEmployment()):
                    G.add_edge(person.getName(), otherPerson.getName())





    print(G.number_of_edges())
    # Grab neighbours of all nodes
    succ = nx.dfs_successors(G)
    pprint(succ)
    # Function for recursively checking nodezplz
    def recur(nodeCurrent, dist):
      # Update shortest distance to current node
      deltaAtNodes[nodeCurrent] = dist
      # Update suspicion at current node
      pplDict[nodeCurrent].addToFactor(exp(-dist))
      if (nodeCurrent in succ.keys()):
          for neighbour in succ[nodeCurrent]:
              # Yeah I'm global bb
            if deltaAtNodes[neighbour] == -1:
                pass # Another bad person was found
            elif deltaAtNodes[neighbour] == 0:
                recur(neighbour, dist+1) # Neighbour not visited
            elif dist+1 < deltaAtNodes[neighbour]:
                # A shorter distance was found; record distance
                deltaAtNodes[nodeCurrent] = dist+1
            # Replace suspicion from longer path with suspicion from shorter path
                pplDict[nodeCurrent].addToFactor((-deltaAtNodes[nodeCurrent]) + exp(-(dist+1)))

    # Starting from each bad persx on, fill in the suspicion of connected people
    for badPerson in bannedPpl:
      # Set deltas to zero for each node
      deltaAtNodes = {k:0 for k in list(G.nodes)}
      # For bad person, set to -1 to prevent re-counting
      deltaAtNodes[badPerson] = -1
      # Run recurring function thing
      recur(badPerson,1)

    #G.add_edge(dude, jj)


    #print(list(G.nodes))
    #print(list(G.edges))
    # Dictionary of visitedness: node as key

    return G
