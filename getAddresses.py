from utils import getRequest
from config import getBaseURL

def getAddresses(campaignID, orgID=None):
    # If orgID passed, get the addresses for an Organization otherwise it's addresses for a Campaign
    base = getBaseURL()
    if orgID is not None:
        url = base+"organizations/"+str(orgID)+"/addresses"
        IDs, names = getAll(url)
        return zip(IDs, names)
    else:
        url = base+"campaigns/"+str(campaignID)+'/campaign_addresses'
        resp = getRequest(url)
        #printAddress(resp)
        return resp

def getAll(url):
    # No printing, just get the ID and Name of all Addresses
    IDs = []
    names = []
    resp = getRequest(url)
    numPages = resp['paging']['total']
    for page in range(2, numPages+2):
        for a in resp['addresses']:
            IDs.append(a['id'])
            names.append(a['name'])
        resp = getRequest(url+"?page="+str(page))
    return IDs, names

def printAddress(resp):
    print("{:<15}{:<40}".format("Campaign ID", "Address ID"))
    for address in resp['campaign_addresses']:
        print("{:<15}{}".format(address['campaign_id'], address['id']))