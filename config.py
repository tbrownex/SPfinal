def getHeader():
    return {
        "X-App-Key": "15454bc0-2eb5-0136-4760-067f653fa718",
        "X-User-Key": "1ae9a790-260d-013a-4dd4-06abc14c0bc6",
        "Content-Type": "application/json"
    }

def getBaseURL():
    return "https://app.simpli.fi/api/"

def adPaths():
    return {
        '140199': "/home/tbrownex/data/Subway/images/"
    }

def addressPaths():
    return {
        '140199': "/home/tbrownex/data/Subway/hhAddresses/"
    }

def linkPaths():
    return {
        '140199': "/home/tbrownex/data/Subway/"
    }

def markets():
    return ['chicago', 'denver']
