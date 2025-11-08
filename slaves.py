import requests
import time
import json
class Slave:
    def __init__(self,name,token,trade,drop):
        self.Name = name
        self.token = token
        self.userId = self.getUserID()
        self.tradeChannel = trade
        self.dropChannel = drop
    
    def dropKaruta(self):
        url = f"https://discord.com/api/v9/channels/{self.dropChannel}/messages"
        payload = {'content': 'k!drop'}
        header = {'Authorization': self.token}
        r = requests.post(url, data=payload, headers=header)
        data = json.load(r.text) 
        time.sleep(0.25)
        return data["id"] #messageId
        
    def grabCard(self,messageID,emoji):
        url = f"https://discord.com/api/v9/channels/{self.dropChannel}/messages/{messageID}/reactions/{emoji}/@me"
        header = {'Authorization': self.token}
        requests.put(url, headers=header)
        time.sleep(0.25)
        r= requests.get(f"https://discord.com/api/v9/channels/{self.dropChannel}/messages?limit=1")
        data = json.load(r.text)
        return [self.getName(data["0"]["content"]),self] #return [cardName,currentSlave] 
        

    def getID(self,cardName):
        url = f"https://discord.com/api/v9/channels/{self.tradeChannel}/messages"
        payload = {'content': 'k!collection character={cardName}'}
        header = {'Authorization': self.token}
        requests.post(url, data=payload, headers=header)
        time.sleep(0.25)
    
    def InitTrade(self,cardID,userID):
        url = f"https://discord.com/api/v9/channels/{self.tradeChannel}/messages"
        payload = {'content': 'k!trade <@{userID}> {cardID}'}
        header = {'Authorization': self.token}
        requests.post(url, data=payload, headers=header)
        time.sleep(0.25)

    def getUserId(self):
        url = f"https://discord.com/api/v9/users/@me"
        header = {"Authorization":self.token}
        r = requests.get(url,headers=header)
        data = json.load(r.text)
        return data["id"]

    def getName(self,content):
        return "**".split(content)[1]