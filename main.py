import json
import time
from slaves import Slave
from middleman import MiddleMan
import os

class BotManager:
    def __init__(self):
        self.middleMan = None
        self.Slaves = None
        self.IsRunning = False
        self.checkFiles()
        self.setUp()

    def setUp(self):
        with open("accounts.json",'r') as f:
            data = json.load(f)
        accounts = data["accounts"]
        with open("settings.json",'r') as f:
            data = json.load(f)
        trade=data["tradeChannel"]
        drop=data["dropChannel"]
        owner=data["ownerChannel"]
        
        self.Slaves = [Slave(name=account[0],token=account[1],trade=trade,drop=drop) for account in accounts]
        self.middleMan = MiddleMan(Token=data["token"],Name=data["name"],trade=trade,drop=drop,owner=owner)

    def getTime():
        with open("accounts.json",'r') as f:
            data = json.load(f)
        accounts = len(data["accounts"])
        return 10/(accounts//3)
    def checkFiles():
        if not os.path.exists("accounts.json"):
            with open("accounts.json", "w") as f:
                json.dump({"accounts": []}, f)
        if not os.path.exist("settings.json"):
            with open("settings.json", "w") as f:
                json.dump({"tradeChannel":"","dropChannel":"","ownerChannel":"","token":"","name":""},f)
        if not os.path.exists("wishlist.json"):
            with open("wishlist.json",'w') as f:
                json.dump({"wishlist":[]},f)
        if not os.path.exists("collection.json"):
            with open("collection.json",'w') as f:
                json.dump({"collection":[]},f)

    def addSlave(self,name,token):
        if self.isRunning:
            return
        with open('accounts.json','r') as f:
            data = json.load(f)
        data["accounts"].append([name,token])
        with open("accounts.json","w") as f:
            json.dump(data,f)

    def removeSlave(self,token):
        if self.isRunning:
            return
        with open("accounts.json","r") as f:
            data = json.load(f)
        for account in data["accounts"]:
            if account[1] == token:
                data["accounts"].pop(data["accounts"].index(account))
    def editSlave(self,name):
        pass

    def editMiddleMan():
        pass

def getEmoji(number):
    match number:
        case 1:
            return r"1%EF%B8%8F%E2%83%A3"
        case 2:
            return r"2%EF%B8%8F%E2%83%A3"
        case 3:
            return r"3%EF%B8%8F%E2%83%A3"

def run():
    bot = BotManager()
    grabber = [0,1,2]
    cardName = []
    interval = bot.getTime()
    
    while True:

        for i in range (len(bot.Slaves)):
            messageId = bot.Slaves[i].dropKaruta()

            for i in range(3):
                emoji = getEmoji(i+1)
                cardName.append(bot.Slaves[grabber[i]].grabCard(messageID=messageId,emoji=emoji))# maybe change messageID to last message like before
                grabber[i] += 3

                if grabber[i] > len(bot.Slaves):
                    grabber -= len(bot.Slaves)

            for card in cardName:
                if bot.middleMan.checkWishList(cardName=card[0]):
                    bot.middleMan.stealCardFromSlave(cardName=card[0],slave=card[1])

            time.sleep(interval)
