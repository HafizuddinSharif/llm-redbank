from fastapi import FastAPI
from pydantic import BaseModel
from ctos_extractor import *
from main import *
import uuid
import requests
import json

class Query(BaseModel):
    query: str
    session_id: str

class CustomerData(BaseModel):
    brn: str

class SessionId(BaseModel):
    session_id: str

# to store key value brn:ctosData
brnDict = {}

# store sessionId into list
sessionIdList = []

app = FastAPI()

@app.post("/testData")
def testData(sessionId: SessionId):
    getBrnData(sessionId.session_id)
    #getBrnData("1408888")
    printAllSession()

    return{"testData completed"}

@app.post("/send-brn")
def send_brn_start_conversation(customerData: CustomerData):
    print("send-brn with brn: " + customerData.brn)

    ## call main API /start-session/{chatbot_name} to get sessionId
    url = 'http://127.0.0.1:8000/start-session/sharif'
    response = requests.get(url)
    currentSessionId = response.text.replace('"', '')
    print("Your sessionId: " + currentSessionId)

    # check if sessionId exist, else update sessionIdList
    if currentSessionId in sessionIdList:
        print("session EXIST.")
    else:
        sessionIdList.append(currentSessionId)
        print("add sessionId: " + currentSessionId + " into list")

    print(sessionIdList)

    # create brnDict to store brn data
    processing_ctos_data(customerData.brn, currentSessionId)

    return {"session created with session_id: " + currentSessionId}


@app.post("/askMe")
def askMe(query_txt: Query):
    # Add logic here
    print("calling askMe with: " + query_txt.query + " with session_id: " + query_txt.session_id)

    # send question to mainBot

    ## TODO: given sessionId

    ## TODO
    # check if session id exist, if exist, call /chat, if not exist call /sharif
    if findSession(query_txt.session_id):
        # call /chat/{chatbot_name}
        print("session exist, call chat")

        currentBrnData = getBrnData(query_txt.session_id)
        #print(currentBrnData)

        formulated_query = query_txt.query + " " + currentBrnData

        url = 'http://127.0.0.1:8000/chat/sharif'
        data = {"query": formulated_query, "session_id": query_txt.session_id}
        response = requests.post(url, json=data)
        print(response.text)
    else:
        # call start-session, call /chat/{chatbot_name}
        print("session does not exist, start-session followed up by chat")

        ## call main API /start-session/{chatbot_name} to get sessionId
        url = 'http://127.0.0.1:8000/start-session/sharif'
        response = requests.get(url)
        currentSessionId = response.text.replace('"', '')
        print("Your sessionId: " + currentSessionId)

        # check if sessionId exist, else update sessionIdList
        if currentSessionId in sessionIdList:
            print("session EXIST.")
        else:
            sessionIdList.append(currentSessionId)
            print("add sessionId: " + currentSessionId + " into list")

        currentBrnData = getBrnData(currentSessionId)
        #print(currentBrnData)

        formulated_query = query_txt.query + " " + currentBrnData

        url = 'http://127.0.0.1:8000/chat/sharif'
        data = {"query": formulated_query, "session_id": query_txt.session_id}
        response = requests.post(url, json=data)
        print(response.text)

    return {"askMe successful"}

def processing_ctos_data(brn, session_id):
    print("call processing_ctos_data API with brn:" + brn + ", and session_id: " + session_id)

    extracted_xml = extract_xml(brn)
    if extracted_xml is None:
        return {"response": "BRN number does not have the CTOS data"}

    ctos_data = json.dumps(extracted_xml)

    if session_id in brnDict:
        print("brn data exists, do nothing")
    else:
        print("brn data NOT exists, update dict")
        brnDict.update({session_id:ctos_data})

    #for x, y in brnDict.items():
    #    print(x, y)

    return{"createSession OK"}

## a method to return data from the dictionary
def getBrnData(session_id):
    print("call getBrnData API with session_id:" + session_id)

    brnData = brnDict.get(session_id)

    print("=======================")
    print(brnData)

    return brnData

# to find sessionId supplied against the current sessionIdList
def findSession(sessionId):
    if sessionId in sessionIdList:
        print("found sessionId: " + sessionId)
        return True
    else:
        print("NOT found sessionId: " + sessionId)
        return False
    
def printAllSession():
    print(sessionIdList)

## TODO: API for suggested bubble - redflags, 
