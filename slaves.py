import requests
import time

class Slave:
    def __init__(self,name,token,trade,drop):
        self.Name = name
        self.token = token
        self.tradeChannel = trade
        self.dropChannel = drop
    
    def dropKaruta(self):
        url = f"https://discord.com/api/v9/channels/{self.dropChannel}/messages"
        payload = {'content': 'k!drop'}
        header = {'Authorization': self.token}
        requests.post(url, data=payload, headers=header)
        time.sleep(0.25)
        return #messageId
        
    def grabCard(self,messageID,emoji):
        url = f"https://discord.com/api/v9/channels/{self.dropChannel}/messages/{messageID}/reactions/{emoji}/@me"
        header = {'Authorization': self.token}
        requests.put(url, headers=header)
        time.sleep(0.25)
        #return [cardName,self.token] 

    def getID(self,cardName):
        url = f"https://discord.com/api/v9/channels/{self.tradeChannel}/messages"
        payload = {'content': 'k!collection character={cardName}'}
        header = {'Authorization': self.token}
        requests.post(url, data=payload, headers=header)
        time.sleep(0.25)