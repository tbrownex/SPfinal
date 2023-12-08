import sys
sys.path.insert(0, '/home/tomb/code/hermes/scripts')

import pandas as pd
import sqlalchemy
import psycopg2
from sqlalchemy import text

from getCampaign import getCampaign
from getDeviceTypes import getDeviceTypes
from getDomains import getDomains
from getGeoFences import getGeoFences
from getOrganization import getOrg
#Max Bid
#(Trigger) Geofence Changes
#(Conversion Fences) Geo-Conversions

SIMPLIFI_MASTERS = [3582129]
SIMPLIFI_ORGID = 374920 
CAMPAIGNGROUP_ID = 8

def main():
    orgName = getOrg(SIMPLIFI_ORGID)
    print("\n{:<20}{:<18}{}".format(orgName, "Campaign ID", "Name"))
    for master in SIMPLIFI_MASTERS:
        tmp = getCampaign(SIMPLIFI_ORGID, master)
        print("{:<21}{:<17}{}".format(" ", master, tmp['name']))
    connection = getPostgresConnection()
    groupName = getCampaignGroup(connection)
    print("\nCampaign Group: {}".format(groupName))
    confirm = input("\nContinue? Press Ctrl-C to stop or <enter> to continue")
    if confirm.upper() == 'Y':
        sql = text("INSERT INTO campaigns_masters(name, campaigngroup, masterid, start_date, end_date) VALUES(:name, :groupID, :master, :startDt, :endDt);")
        for master in SIMPLIFI_MASTERS:
            tmp = getCampaign(SIMPLIFI_ORGID, master)
            parmDict = {}
            parmDict['name'] = 'test' 
            parmDict['groupID'] = CAMPAIGNGROUP_ID 
            parmDict['master'] = master 
            parmDict['startDt'] = tmp['start_date'] 
            parmDict['endDt'] = tmp['end_date'] 
            results = connection.execute(sql, parameters=parmDict)
            connection.commit()

def getCampaignGroup(connection):
    sql = text("SELECT * FROM campaigns_campaigngroup WHERE id = (:groupID);")
    parmDict = {}
    parmDict['groupID'] = CAMPAIGNGROUP_ID 
    results = connection.execute(sql, parameters={'groupID': CAMPAIGNGROUP_ID}).fetchone()
    return results[1]

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

    # PostGres
def getPostgresConnection():
    LOCAL_PG_USER  = "tom"
    LOCAL_PG_HOST  = "localhost"
    LOCAL_DB_NAME  = "simplify"
    PASSWORD = 'bronco'
    engine = sqlalchemy.create_engine('postgresql://{username}:{pwd}@{host}/{db}'.format(
          username=LOCAL_PG_USER,
          host=LOCAL_PG_HOST,
          db=LOCAL_DB_NAME,
          pwd=PASSWORD))
    return engine.connect()

if __name__ == "__main__":
    main()
