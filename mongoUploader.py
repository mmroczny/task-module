import requests
import csv
import json
import concurrent.futures
import pymongo

accept = 'application/vnd.allegro.public.v1+json'
k = 'Bearer '
headers = {'accept': accept, 'authorization': k}


supp_IDs = []

def tupleFiller():
    with open('offers_with_supplier_id.csv', 'r') as f:

        suppData = csv.reader(f)
    
        for line in suppData:
            supp_IDs.append((line[0], line[1]))        
call = tupleFiller()



def getMessage():

    messagesURL = f'https://api.allegro.pl/sale/disputes/{}/messages'
    curMessagesURL = baseURL + str(auID)

    messResp = requests.get(curOffURL, headers=headers)
    
    messagesJSON = messResp.json()
    messRespCode = messResp.status_code

    
def recordCreator(suppID, auID):
    
    baseURL = 'https://api.allegro.pl/sale/offers/'
    curOffURL = baseURL + str(auID)

    offer = requests.get(curOffURL, headers=headers).json()
    
    client = pymongo.MongoClient("mongodb://root:example@192.168.1.50")

    allCollec = client.allegro.offers
    
    insertion = [{"supplier_id": suppID, "our_picture": False, "offer": offer}]
    

    initing = allCollec.insert(insertion)


    print(suppID)


with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    for ajdi in supp_IDs:
        future = executor.submit(recordCreator, suppID = ajdi[0], auID = ajdi[1])  
        

