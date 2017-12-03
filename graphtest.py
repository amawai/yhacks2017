import networkx as nx
from pprint import pprint
import string
from math import exp
import numpy as np
import matplotlib.pyplot as plt
G = nx.Graph()

CORP_PENALTY_STEP = 0.1 #Suspicion points
pplDict = {}
corpDict = {}
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
        corpFactor = self.factor + corpDict[self.currentEmp].getFactor()
        return min(1, corpFactor)

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
    bannedPpl = ["BARBARA JEAN ABADI", "JOSEPH ABBONDANTE", "EMMETT MAURICE ABERCROMBIE", "ANDREW MARTIN ABERN"]


    #Adding the banned brokers to our network
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


    iapd = {} #populate with iapd values
    iapdPerson = None

    #Add corporations to the dictionary

    #TEMPS:
    corp1 = {'id': 123, 'name':'Succ it', 'city': 'NEW YORK'}
    corp2 = {'id': 456, 'name':'Eat it', 'city': 'NEW YORK'}
    corps = {} #Populate with corps values
    corps['Succ it'] = corp1
    corps['Eat it'] = corp2
    #END TEMPS

    courtDates = {} #Populate w/ court jsons
    for corp in corps:
        print(corps[corp])
        corpDict[corp] = Corporation(corps[corp]['id'], corps[corp]['name'], corps[corp]['city'], 0)
        for courts in courtDates:
            #Putting the corp name into slug format found in json
            if (courts.slug.split('-v-')[1] == '-'.join(corp.name.split(' ')).lower()):
                #If the corp was a defendent, it sounds... sketch af
                corpDict[corp].addCourtCitation(courts.citation_id)

    #Adding everybody as a node in the network
    for person in iapd:
        iapdPerson = Person(person.indvlPK, person.firstNm, person.lastNm, corps[person.CrntEmp.orgNm], 0)
        for corp in person.empHs:
            iapdPerson.addToEmployeeHistory(corp.orgNm, corp.fromDt)
        name = (person.firstNm + ' ' + person.lastNm).upper()
        pplDict[name] = iapdPerson
        G.add_node(iapdPerson)



    #Currently, we have nodes representing everybody in our network, but no edges/connections
    #We also have a dictionary of corporations with a suspicious factor calculated based on court appearances as a defendant

    # Assume suspicion is initialized somewhere as a dictionary of nodes to float
    suspicion = list(G.nodes())

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

    plt.plot(121)
    print([ppl.getName() for ppl in pplDict.values()])
    print([ppl.getFactor() for ppl in pplDict.values()])
    nx.draw(G, node_color=[ppl.getFactor() for ppl in pplDict.values()], with_labels=True, font_weight='bold')
    #nx.draw_shell(G, with_labels=True, font_weight='bold')
    plt.show()

    badGuys = [ppl.getName() for ppl in pplDict.values() if ppl.getName() not in bannedPpl]
    print(G.number_of_nodes())
    print(G.number_of_edges())
    return badGuys

computeNodes()
