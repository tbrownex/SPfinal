import pandas as pd
import json

from utils import putRequest
from config import getBaseURL
from getAddresses import getAddresses

def delAddress(campaignID):
    '''
    Get the addressable target for a campaign and delete it, This assumes 1 Target per campaign
    '''
    resp = getID(campaignID)
    # response will be None if no current target
    if resp:
        delID = resp[0]['id']
        resp = delete(campaignID, delID)
        return resp
    else:
        return

def getID(x):
    resp = getAddresses(x)
    print(resp)
    return resp['campaign_addresses']

def delete(campaignID, delID):
    base = getBaseURL()
    url = base + "campaigns/"+str(campaignID)+'/campaign_addresses/change'
    d = {}
    d["delete"] = [delID]
    d['segment_type_id']= 1
    d["segment_match_type"] = "any"
    payload = {}
    payload["campaign_first_party_segments"] = d
    payloadString = json.dumps(payload)
    print(payloadString)
    return putRequest(url, payloadString)
