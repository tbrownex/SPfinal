from utils import getRequest
from config import getBaseURL

def getOrg(orgID=None, prt=None):
    base = getBaseURL()
    if orgID:
        # This will get the name of an organization
        url = base + "organizations/"+str(orgID)
        return singleOrg(url, prt)
    else:
        # This will get all organizations
        url = base + "organizations"
        return allOrg(url)

def singleOrg(url, prt):
    resp = getRequest(url)
    if prt: print(resp['name'])
    return resp['name']

def allOrg(url):
    resp = getRequest(url)
    for org in resp['organizations']:
        print(org['id'], org['name'])
    return resp
