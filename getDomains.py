from utils import getRequest
from config import getBaseURL

def getDomains(orgID, campaignID):
    # The "device_types" request will return all the device type IDs for this campaign
    base = getBaseURL()
    url = base+"organizations/"+str(orgID)+"/campaigns/"+str(campaignID)+"/domains"
    resp = getRequest(url)
    return resp 
