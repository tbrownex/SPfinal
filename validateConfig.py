import os

from config import adPaths, addressPaths, linkPaths

def validate(orgID):
    '''
    Confirm adPath folder exists
    Confirm linkPath folder exists
    Confirm HH Adresses folder exists and contains only CSV files
    '''
    valid = True
    d = adPaths()
    path = d[orgID]
    if not os.path.isdir(path):
        print("\nInvalid path to Ads")
        valid = False

    d = linkPaths()
    path = d[orgID]
    if not os.path.isdir(path):
        print("\nInvalid path to Link table")
        valid = False

    d = addressPaths()
    path = d[orgID]
    if os.path.isdir(path):
        for _, markets, _ in os.walk(path):
            for market in markets:
                for _,_, files in os.walk(path+market):
                    for file in files:
                        if not file.endswith('.csv'):
                            print("\nNon-CSV file {} in {} market".format(file, market))
                            valid=False
    else:
        print("\nInvalid path to HH Addresses")
        valid = False
    return valid