import json
import time
from scripts.slaves import Slave
from scripts.middleman import MiddleMan
import os
import threading
from pathlib import Path

class BotManager:
    def __init__(self):
        self.middleMan = None
        self.Slaves = None
        self.IsRunning = False
        self.process = None
        self.thread = None
        root = Path(__file__).resolve().parent.parent
        self.path = root / "userdata"
        self.checkFiles()
        self.setUp()

    def setUp(self):
        with open(self.path / "accounts.json",'r') as f:
            data = json.load(f)
        accounts = data["accounts"]
        with open(self.path / "settings.json",'r') as f:
            data = json.load(f)
        trade=data["tradeChannel"]
        drop=data["dropChannel"]
        owner=data["ownerChannel"]
        
        self.Slaves = [Slave(name=account[0],token=account[1],trade=trade,drop=drop) for account in accounts]
        self.middleMan = MiddleMan(Token=data["token"],Name=data["name"],trade=trade,drop=drop,owner=owner)
    
    def getTime(self):
        return (10/(len(self.Slaves)//3))*60
    
    def checkFiles(self):
        if not os.path.exists(self.path / "accounts.json"):
            with open(self.path / "accounts.json", "w") as f:
                json.dump({"accounts": []}, f)
        if not os.path.exists(self.path / "settings.json"):
            with open(self.path / "settings.json", "w") as f:
                json.dump({"tradeChannel":"","dropChannel":"","ownerChannel":"","token":"","name":""},f)
        if not os.path.exists(self.path / "wishlist.json"):
            with open(self.path / "wishlist.json",'w') as f:
                json.dump({"wishlist":[]},f)
        if not os.path.exists(self.path / "collection.json"):
            with open(self.path / "collection.json",'w') as f:
                json.dump({"collection":[]},f)

    def addSlave(self,name,token):
        if self.isRunning:
            return
        with open(self.path / 'accounts.json','r') as f:
            data = json.load(f)
        data["accounts"].append([name,token])
        with open(self.path / "accounts.json","w") as f:
            json.dump(data,f)
        self.setUp()
    
    def removeSlave(self,token):
        if self.isRunning:
            return
        with open(self.path / "accounts.json","r") as f:
            data = json.load(f)
        for account in data["accounts"]:
            if account[1] == token:
                data["accounts"].pop(data["accounts"].index(account))
                break
        with open(self.path / 'accounts.json','w') as f:
            json.dump(data,f)
        self.setUp()
    
    def editSlave(self,token,newName,newToken):
        if self.IsRunning:
            return
        with open(self.path / 'accounts.json',"r") as f:
            data = json.load(f)
        for account in data["accounts"]:
            if account[1] == token:
                account[0],account[1] = newName, newToken
                break
        with open(self.path / 'accounts.json','w') as f:
            json.dump(data,f)
        self.setUp()

    def editMiddleMan(self,newName,newToken):
        if self.IsRunning:
            return
        with open(self.path / "settings.json","r") as f:
            data = json.load(f)
        data["token"],data["name"] = newToken,newName
        with open(self.path / 'settings.json','w') as f:
            json.dump(data,f)
        self.setUp()

    def start(self):
        if self.process == None:
            self.thread = threading.Thread(target=self.run)
            self.IsRunning = True
            self.thread.start()

    def stop(self):
        if self.thread.is_alive():
            self.thread.join(timeout=1)
        self.IsRunning = False
        self.thread = None

    def run(self):
        
        grabber = [0,1,2]
        cardName = []
        interval = self.getTime()
        
        while self.IsRunning:
            for i in range (len(self.Slaves)):
                messageId = self.Slaves[i].dropKaruta()
                for i in range(3):
                    emoji = self.getEmoji(i+1)
                    cardName.append(self.Slaves[grabber[i]].grabCard(messageID=messageId,emoji=emoji))
                    grabber[i] += 3
                    if grabber[i] > len(self.Slaves):
                        grabber -= len(self.Slaves)
                for card in cardName:
                    if self.middleMan.checkWishList(cardName=card[0]):
                        self.middleMan.stealCardFromSlave(cardName=card[0],slave=card[1])

                time.sleep(interval)

    def getEmoji(number):
        match number:
            case 1:
                return r"1%EF%B8%8F%E2%83%A3"
            case 2:
                return r"2%EF%B8%8F%E2%83%A3"
            case 3:
                return r"3%EF%B8%8F%E2%83%A3"


