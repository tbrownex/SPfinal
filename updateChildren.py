import sys
sys.path.insert(0, '/home/tomb/code/hermes/scripts')

import sqlalchemy
import psycopg2
from sqlalchemy import text
import json

from getCampaign import getCampaign
from getDeviceTypes import getDeviceTypes
from getDomains import getDomains
from getGeoFences import getGeoFences
from getOrganization import getOrg
from getDBConnection import getPostgresConnection
from updateCampaign import updateCampaign
#Max Bid
#(Trigger) Geofence Changes
#(Conversion Fences) Geo-Conversions

def main():
    groupID = input("Enter Campaign Group ID:")
    connection = getPostgresConnection()
    campaignGroup = getCampaignGroup(connection, groupID)
    for row in campaignGroup:
        orgID = row[2]
        masters = getMasters(connection, groupID)
        keys = []
        vals = []
        for row in masters:
            masterID, prev_start, prev_end, prev_freq_cap = row[3], row[4], row[5], row[6]
            #children = getChildren(connection, groupID, masterID)
            curr = getCampaign(orgID, masterID)
            curr_start, curr_end = curr['start_date'], curr['end_date']
            curr_freq_cap = curr['frequency_capping']
            if curr_start != prev_start:
                keys.append('start_date')
                vals.append(curr_start)
                #payload = {'campaign': {"start_date": curr_start}}
                #payload=json.dumps(payload)
                #for campaignID in children:
                #    resp = updateCampaign(orgID, campaignID[0], payload)
            if curr_end != prev_end:
                keys.append('end_date')
                vals.append(curr_end)
                #payload = {'campaign': {"end_date": curr_end}}
                #payload=json.dumps(payload)
                #for campaignID in children:
                #    resp = updateCampaign(orgID, campaignID[0], payload)
            if str(curr_freq_cap) != prev_freq_cap:
                keys.append('frequency_capping')
                vals.append(curr_freq_cap)
            if len(keys) > 0:
                d={}
                for idx, key in enumerate(keys):
                    print(key)
                    d[key] = vals[idx]
                payload = {'campaign': d}
                payload=json.dumps(payload)
                children = getChildren(connection, groupID, masterID)
                for campaignID in children:
                    print('child')
                    resp = updateCampaign(orgID, campaignID[0], payload)
                    print(resp)

def getCampaignGroup(connection, groupID):
    sql = text("SELECT * FROM campaigns_campaigngroup WHERE id = (:groupID);")
    results = connection.execute(sql, parameters={'groupID': groupID})
    return results

def getMasters(connection, groupID):
    sql = text("SELECT * FROM campaigns_masters WHERE campaigngroup = (:groupID);")
    results = connection.execute(sql, parameters={'groupID': groupID})
    return results

def getChildren(connection, groupID, masterID):
    sql = text("SELECT childID FROM campaigns_children WHERE campaigngroup = (:groupID) AND masterID = (:masterID);")
    results = connection.execute(sql, parameters={'groupID': groupID, 'masterID': masterID})
    return results

        #sql = text("INSERT INTO campaigns_masters(campaigngroup, start_date, end_date) VALUES(:start_date, :end_date);")
        #freqCap = tmp['frequency_capping']
        #freqCap_times = freqCap['how_many_times']   # Numeric
        #freqCap_hours = freqCap['hours']            # Numeric
        #dailyImpressionCap = tmp['daily_impression_cap'] # Numeric
        #monthlyImpressionCap = tmp['monthly_impression_cap'] # Numeric  
        #dayParting = tmp['week_dayparting']    # List length 7, each element a list
        #deviceTypes = getDeviceTypes(master)       # List of integers
        #domains = getDomains(ORGANIZATION_ID, master)   # Dictionary
        #print(domains['domains'][0].keys())
        #domainName = domains['domains'][0]['name']
        #domainBlockList = domains['domains'][0]['org_blocklist_opt_out'] # Boolean
        #domainType = domains['domains'][0]['type'] # String
        #domainCount = domains['domains'][0]['count'] # Numeric 
        #domainActions = domains['domains'][0]['actions'] # Dictionary; see if we need this one 
        #fences = getGeoFences(ORGANIZATION_ID, master, None, False)
        #print(sorted(tmp.keys()))'''

if __name__ == "__main__":
    main()
