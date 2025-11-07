import requests
import time
import json

class MiddleMan:
    def __init__(self, Token, Name,trade,drop,owner):
        self.token = Token
        self.name = Name
        self.wishList = []
        self.collection = []
        self.tradeChannel = trade
        self.dropChannel = drop
        self.ownerChannel = owner
        self.isMessaging = False
        # getWishList(self)
    
    def getWishList(self):
        with open("wishlist.json",'r') as wishListFile:
            wishListData = json.load(wishListFile)
        self.wishList = wishListData["wishList"]
    
    def checkWishList(self): # will be changed to fetch last 3 msgs
        cardName = [] # fetch card Names
        if cardName in self.wishList:
            return True
        return False
    
    def stealCardFromSlave(self, cardName, slave):
        cardID = slave.GetID(cardName)
        slave.InitTrade(cardID)
        # AcceptTrade
        edition = self.getEdition(cardID)
        self.collection.append([cardName,cardID,edition]) # maybe will make it a json file for consistent tracking
    
    def giveCardToEmployer(self,cardID):
        pass
    
    def getCollection(self):
        for card in self.collection:
            url = f"https://discord.com/api/v9/channels/{self.ownerChannel}/messages"
            payload = {'content': f'Card id : {card[1]}\nCard name : {card[0]}\nCard edition : {card[2]}'}
            header = {'Authorization': self.token}
            requests.post(url, data=payload, headers=header)
            time.sleep(0.25)
