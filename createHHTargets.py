import json
import os
import pandas as pd

from utils import postRequest, putRequest
from config import adPaths, addressPaths, linkPaths
from getOrganization import getOrg
from validateConfig import validate

def main(orgID):
    '''
    For each CSV in "path", create an Addressable Target at the Org level
    Each Addressable Target has a unique ID which needs to be saved and returned
    '''
    validConfig = validate(orgID)
    if validConfig:
        pass
    else:
        print("\nInvalid config...terminating")
        return
    pathDict = adPaths()
    adPath = pathDict[orgID]
    pathDict = addressPaths()
    addressPath = pathDict[orgID]
    csvMap = getCSVmap(addressPath)
    l = []
    for market in csvMap.keys():
        for file in csvMap[market]:
            #addressID = np.random.randint(1000, 2000)
            addressID = processAddressList(orgID, addressPath, file)
            l.append((orgID, market, file, addressID))
    pathDict = linkPaths()
    loc = pathDict[orgID]
    # TODO keep each link table around so we don't lose data on subsequent runs (over-writing what's there)
    pd.DataFrame(l,
                 columns=['organization', 'market', 'addressFile', 'addressID'])\
                 .to_csv(loc+'linkTable.csv', index=False)

def processAddressList(orgID, path, csv):
    # For each CSV create a Target (basically a stub) then add the addresses
    # "create" returns a URL that is used to upload the CSV
    resp = createTarget(orgID, csv)
    addressID = resp['addresses'][0]['id']
    url = resp['upload_url']
    uploadCSV(url, path, csv)
    return addressID
    
def createTarget(orgID, csv):
    # segment_score of "2" means "Frequent"
    base = config.getBaseURL()
    url = base + "organizations/"+str(orgID)+"/addresses"
    d = {'name': csv.split('.')[0],
         "first_party_segment_score_filter_attributes": {"segment_score_filter_id": 2}
        }
    payload = {"address": d}
    payload = json.dumps(payload)
    return postRequest(url, data=payload)

def getCSVmap(path):
    # Return a dictionary of market: list of csv files holding HH addresses
    marketList = []
    for _, markets, _ in os.walk(path):
        for market in markets:
            marketList.append(market)
    d={}
    for market in marketList:
        for _,_, files in os.walk(path+market):
            for file in files:
                d[market] = files
    return d

def uploadCSV(url, path, csv):
    fullPath = path+"/"+csv
    with open(fullPath, "rb") as f:
        resp = putRequest(url, f)

def confirmOrg():
    orgID = input("Enter the Organization ID: ")
    orgName = getOrg(orgID)
    print("\n")
    confirm = input("Confirmed? (yes)")
    if confirm == 'yes':
        return orgID
    else:
        return None

if __name__ == "__main__":
    orgID = confirmOrg()
    if orgID:
        main(orgID)