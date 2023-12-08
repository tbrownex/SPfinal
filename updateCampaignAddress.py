import pandas as pd

from getAddresses import getAddresses

def getID(x):
    resp = getAddresses(x)
    return resp['campaign_addresses'][0]['id']

def updateCampaignAddress(campaigns, addresses):
    # This is temporary for a 1-time run
    campaigns.columns=['campaignID', 'id', '_']
    campaigns.set_index('id', inplace=True)
    addresses.set_index('id', inplace=True)
    j = df.join(campaigns, how='inner')
    return j
    # Get the current address assigned to each campaign
    campaigns['delAddr'] = campaigns['campaignID'].apply(lambda x: getID(x))
    # Each row now has: campaign, current address, new address
    # Remove the current and replace with new
    for row in campaigns.iterrows():
        campaignID = row[1]['campaignID']
        delID = int(row[1]['delAddr'])
        url = base + "campaigns/"+str(campaignID)+'/campaign_addresses/change'
        d = {}
        d["delete"] = [delID]
        payload = {}
        payload["campaign_first_party_segments"] = d
        payloadString = json.dumps(payload)
        resp = putRequest(url, payloadString)