import json

from utils import postRequest
from config import getBaseURL

import requests

def postAd(orgID, campaignID, adDetails):
    '''
    Associates HTML to a campaign
    "adDetails" is a dictionary for naming the Ad and the location of the image
    '''
    base = getBaseURL()
    url = base+"organizations/"+str(orgID)+"/campaigns/"+str(campaignID)+'/ads'
    
    ad = {}
    ad['ad'] = adDetails
    payload = ad
    payloadString = json.dumps(payload)
    resp = postRequest(url, payloadString)
    return resp