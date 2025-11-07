import json
import time
from slaves import Slave
from middleman import MiddleMan
import os

isRunning = False
Slaves = []
middleMan = None
def getTime():
    with open("accounts.json",'r') as f:
        data = json.load(f)
    accounts = len(data["accounts"])
    return 10/(accounts//3)


def setUp():
    with open("accounts.json",'r') as f:
        data = json.load(f)
    accounts = data["accounts"]
    with open("settings.json",'r') as f:
        data = json.load(f)
    
    trade=data["tradeChannel"]
    drop=data["dropChannel"]
    owner=data["ownerChannel"]
    # setting up the slaves
    Slaves = [Slave(name=account[0],token=account[1],trade=trade,drop=drop) for account in accounts]
    middleMan = MiddleMan(Token=data["token"],Name=data["name"],trade=trade,drop=drop,owner=owner)



def checkFiles():
    if not os.path.exists("accounts.json"):
        with open("accounts.json", "w") as f:
            json.dump({"accounts": []}, f)
    if not os.path.exist("settings.json"):
        with open("settings.json", "w") as f:
            json.dump({"tradeChannel":"","dropChannel":"","ownerChannel":""},f)
    if not os.path.exists("wishlist.json"):
        with open("wishlist.json",'w') as f:
            json.dump({"wishlist":[]},f)
    if not os.path.exists("collection.json"):
        with open("collection.json",'w') as f:
            json.dump({"collection":[]},f)

def addSlave(name,token):
    if isRunning:
        return
    with open('accounts.json','r') as f:
        data = json.load(f)
    data["accounts"].append([name,token])
    with open("accounts.json","w") as f:
        json.dump(data,f)

def removeSlave(token):
    if isRunning:
        return
    with open("accounts.json","r") as f:
        data = json.load(f)
    for account in data["accounts"]:
        if account[1] == token:
            data["accounts"].pop(data["accounts"]index(account))

def run():
    isRunning = True
    interval = getTime()
    grabber = [0,1,2]
    cardName = []
    while True:
        for i in range (len(Slaves)):
            messageId = Slaves[i].dropKaruta()
            
            for i in range(3):
                cardName.append(Slaves[grabber[i]].grabCard(messageID=messageID,emoji=emoji))# maybe change messageID to last message like before
                grabber[i] += 3

                if grabber[i] > len(Slaves):
                    grabber -= len(Slaves)
            for card in cardName:
                if middleMan.checkWishList(card[0]):
                    middleMan.stealCardFromSlave(cardName=card[0],slave=card[1])
                