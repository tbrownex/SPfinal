import sys
sys.path.insert(0, '/home/tomb/code/hermes/scripts')

import sqlalchemy
import psycopg2
from sqlalchemy import text

from getOrganization import getOrg

def main():
    connection = getPostgresConnection()
    sql = text("INSERT INTO campaigns_client(client_id, name) VALUES(:client_id, :name);")
    orgs = getOrg(None)
    print('\n\n')
    print('----------------------')
    count = 3
    for org in orgs['organizations']:
        parmDict = {}
        parmDict['client_id'] =org['id'] 
        parmDict['name'] = org['name']
        if parmDict['client_id'] == 374920:
            results = connection.execute(sql, parameters=parmDict)
            print(results)
    connection.commit()
    return



if __name__ == "__main__":
    main()
