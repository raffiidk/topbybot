import requests
import json
import time
from discord_webhook import DiscordWebhook
import discord

# client = discord.Client()

def writeData(data, filename):
    with open(filename,"w") as f:
        # print(data)
        json.dump(data,f,indent=4)
        f.close()

def getlast(): #Get last item in JSON file (get last stock number read)
    with open(jsonFile,"r+") as f:
        jsonObj = json.load(f)
        jsonObj2 = jsonObj["history"]
        last = jsonObj2[-1]
        f.close()
        return last

def writejson(write): #Send data to JSON file - used to update the stock numbers in the list
    with open(jsonFile,"r+") as f:

        jsonObj = json.load(f)
        jsonObj2 = jsonObj["history"]
        jsonObj2.append(write)
    writeData(jsonObj,jsonFile)

def check(last,checkval): #Check for a change in the latest stock reading and the current stock reading
    changeDetected = False
    newMarket = 0
    titles = []
    for j in last:
        ids.append(j['id'])

    if last == checkval:
        return changeDetected, newMarket
    if checkval != last:
        
        for i in checkval:
            if i['id'] not in ids:
                changeDetected = True
                newMarket = i
                return changeDetected, newMarket
    return changeDetected, newMarket
            
    
jsonFile = 'data.json'
wChannel = 812153914325467146

url = "https://gamma-api.polymarket.com/events?limit=20&active=true&archived=false&closed=false&order=startDate&ascending=false&offset=0&exclude_tag_id=100639"
# postReq = requests.GET(url,json=query)
postReq = requests.get(url)
markets = postReq.json()
URL = "https://discord.com/api/webhooks/816987768013717514/mWa8D2QrFVVSawdb90upxM3xD8mwDd-IY4osf9iyAM-GSFC1kysfKTfmQkQF859jgZhC"

reset = 'static.json'

print(len(markets))
writejson(markets)

delay = 15
bozo = DiscordWebhook(url ="https://discord.com/api/webhooks/816987768013717514/mWa8D2QrFVVSawdb90upxM3xD8mwDd-IY4osf9iyAM-GSFC1kysfKTfmQkQF859jgZhC",content = " stuff: {}".format(type(markets)))
xxx = bozo.execute()

while True:
    recent = requests.get(url)
    recentMarkets = recent.json()
    last = getlast()
    try:
        changed, changedMarket = check(last,recentMarkets)
    except TypeError:
        print(check(last,recentMarkets))
        print("errrrrr")

    if changed == True:
        # #GO CRAZY
        returnObj = [changedMarket['title'],changedMarket['creationDate'],changedMarket['image']]
        webhook = DiscordWebhook(url ="https://discord.com/api/webhooks/816987768013717514/mWa8D2QrFVVSawdb90upxM3xD8mwDd-IY4osf9iyAM-GSFC1kysfKTfmQkQF859jgZhC",content = "``` New Market \n Name: {} \n Creation Time: {} ```".format(returnObj[0],returnObj[1]))
        response = webhook.execute()
        print("GO CRAZY")
    
    # returnMessage = [recentMarkets[0]['title'],recentMarkets[0]['startDate'],recentMarkets[0]['icon']]
    # print(returnMessage)
    # webhookTest = DiscordWebhook(url ="https://discord.com/api/webhooks/816987768013717514/mWa8D2QrFVVSawdb90upxM3xD8mwDd-IY4osf9iyAM-GSFC1kysfKTfmQkQF859jgZhC",content = "``` New Market \n Name: {} \n Creation Time: {} ```".format(returnMessage[0],returnMessage[1]))
    # r2 = webhookTest.execute()
    with open(reset,"r+") as f:
        resetData = json.load(f)
        writeData(resetData,jsonFile)
    
    writejson(recentMarkets)
    time.sleep(delay)


