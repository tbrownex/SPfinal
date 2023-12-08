import sys
sys.path.insert(0, '/home/tomb/code/hermes/scripts')

import time
from sqlalchemy import text
from copyMaster import copyMaster
from getDBConnection import getPostgresConnection
from getOrganization import getOrg

NUM_COPIES = 2

def getUserInputs():
    input("Enter Organization ID:")
    orgID = 374920
    orgName = getOrg(orgID)
    groupID = input("Enter Campaign Group ID:")
    return orgID, orgName, groupID

def confirmInputs(orgID, orgName, groupID, connection):
    confirm = False
    sql = text("SELECT * FROM campaigns_campaigngroup WHERE id = (:groupID);")
    results = connection.execute(sql, parameters={'groupID': groupID}).fetchone()
    name, groupOrg = results[1], results[2]
    if groupOrg != orgID:
        print("\nThat Campaign Group ID is for organization {}".format(groupOrg))
        print("But you entered {} as the organization ID".format(orgID))
        print("Those two have to match...ending")
    else:
        print("\n{:<20}{:<20}{}".format("Organization", "Campaign Group ID", "Group Name"))
        print("{:<25}{:<15}{}".format(orgName, groupID, name))
        confirm = input("Review and press y or Y to continue")
        if confirm.upper() == 'Y':
            return True

def process(orgID, groupID, connection):
        # Get the master campaigns
        sql = text("SELECT masterid FROM campaigns_masters WHERE campaigngroup = (:groupID);")
        results = connection.execute(sql, parameters={'groupID': groupID})
        sql = text("INSERT INTO campaigns_children(campaigngroup, masterid, childid) VALUES(:groupID, :master, :child);")
        parmDict ={'groupID': groupID}
        for row in results:
            master = row.masterid
            print("Processing master {}".format(master))
            parmDict['master'] = master
            childIDs = copyMaster(orgID, master, NUM_COPIES)
            for id in childIDs:
                parmDict['child'] = id
                results = connection.execute(sql, parameters=parmDict)

def main():
    orgID, orgName, groupID = getUserInputs()
    connection = getPostgresConnection()
    confirmed = confirmInputs(orgID, orgName, groupID, connection)
    if confirmed:
        start_time = time.time()
        process(orgID, groupID, connection)
        # TODO: 'commit' every X inserts
        connection.commit()
        print("\ncomplete after {:,.0f} minutes".format((time.time() -start_time)/60))

if __name__ == "__main__":
    main()
