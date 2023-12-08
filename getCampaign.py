import math

from utils import getRequest
from config import getBaseURL

def getCampaign(orgID, campaignID):
    # Get the details for a campaign
    base = getBaseURL()
    url = base+"organizations/"+str(orgID)+"/campaigns/"+str(campaignID)
    resp = singleCampaign(url)
    return resp
    
def singleCampaign(url):
    resp = getRequest(url)
    return resp['campaigns'][0]
