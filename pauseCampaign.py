from utils import postRequest
from config import getBaseURL

def pauseCampaign(orgID, campaignID):
    base = getBaseURL()
    url = base+'organizations/'+str(orgID)+'/campaigns/'+str(campaignID)+'/pause'
    resp = postRequest(url, data=None)
    return resp