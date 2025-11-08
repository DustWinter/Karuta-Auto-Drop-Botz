import requests
import time
import json

class MiddleMan:
    def __init__(self, Token, Name,trade,drop,owner):
        self.token = Token
        self.name = Name
        self.wishList = []
        self.collection = self.getCollection()
        self.tradeChannel = trade
        self.dropChannel = drop
        self.ownerChannel = owner
        self.isMessaging = False
        self.userID = self.getUserId()
        self.getWishList()
    
    def getWishList(self):
        with open("wishlist.json",'r') as wishListFile:
            wishListData = json.load(wishListFile)
        self.wishList = wishListData["wishList"]
    
    def checkWishList(self, cardName):
        if cardName in self.wishList:
            return True
        return False
    def getUserId(self):
        url = f"https://discord.com/api/v9/users/@me"
        header = {"Authorization":self.token}
        r = requests.get(url,headers=header)
        data = json.load(r.text)
        return data["id"]
    
    def stealCardFromSlave(self, cardName, slave):
        cardID = slave.GetID(cardName)
        slave.InitTrade(cardID,self.userID)
        # AcceptTrade
        edition = self.getEdition(cardID)
        self.collection.append([cardName,cardID,edition])
        
        with open("collection.json","w") as f:
            json.dump({"collection":self.collection},f)
    
    def giveCardToEmployer(self,cardID):
        pass
    
    def getCollection(self):
        with open("collection.json",'r') as f:
            data = json.load(f)
        return data["collection"]