from fastapi import FastAPI
from pydantic import BaseModel
from ctos_extractor import *
from main import *
import requests
import json

from datetime import datetime
from datetime import date
import time

class Query(BaseModel):
    query: str
    session_id: str

class CustomerData(BaseModel):
    brn: str

class SessionId(BaseModel):
    session_id: str

# to store key value brn:ctosData
brnDict = {}

brnSessionIdDict = {}

# store sessionId into list
sessionIdList = []

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Angular default URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/testData")
def testData(sessionId: SessionId):
    getBrnData(sessionId.session_id)
    #getBrnData("1408888")
    printAllSession()

    return{"testData completed"}

def days_between_dates(dt1, dt2):
    date_format = "%Y-%m-%d"
    a = time.mktime(time.strptime(dt1, date_format))
    b = time.mktime(time.strptime(dt2, date_format))
    delta = b - a
    return int(delta / 86400)

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

    return {"session_id":currentSessionId}


@app.post("/askMe")
def askMe(query_txt: Query):
    # Add logic here
    print("calling askMe with: " + query_txt.query + " with session_id: " + query_txt.session_id)

    # send question to mainBot

    post_response_json = "UNKNOWN"

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

        post_response_json = response.json()
        #print("post response json: ")
        print(post_response_json["answer"])

        #print(response.text)
    else:
        ## brn info not available, unable to create Brn Dict
        return("Session not FOUND, BRN info does not exist")
    
    ## TODO: do we want to return entire response obj or only the answer?
    return {query_txt.session_id:post_response_json["answer"]}

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

    if session_id in brnSessionIdDict:
        print("sessionId brn found in brnSessionIdDict, do nothing")
    else:
        print("sessionId brn NOT found in brnSessionIdDict, update dict")
        brnSessionIdDict.update({session_id:brn})

    #for x, y in brnDict.items():
    #    print(x, y)

    return{"processing_ctos_data OK"}

## a method to return data from the dictionary
def getBrnData(session_id):
    print("call getBrnData API with session_id:" + session_id)

    brnData = brnDict.get(session_id)

    #print("=======================")
    #print(brnData)

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
@app.post("/bubble")
def bubble(query_txt: Query):
    print("calling bubble with: " + query_txt.query + " with session_id: " + query_txt.session_id)

    if findSession(query_txt.session_id):
        print("session exist, check the target bubble")

        if (query_txt.query == 'redflags'):
            #print("find redflags")

            brn = getBrn(query_txt.session_id)
            print("brn from sessionId: ", brn)

            ## call findRedflags
            redflagsResponse = extract_redflags(brn)
            print("redflagsresponse: ", redflagsResponse)

            redflags_query = "Please return all the red flags description for this data: " + " " + str(redflagsResponse)

            url = 'http://127.0.0.1:8000/chat/sharif'
            data = {"query": redflags_query, "session_id": query_txt.session_id}
            response = requests.post(url, json=data)

            post_response_json = response.json()
            print("post response json: ")
            #print(post_response_json["answer"])
    else:
        return("Session not FOUND, BRN info does not exist")

    return {query_txt.session_id:post_response_json["answer"]}
    # to debug the entire context return by bot
    #return {query_txt.session_id:post_response_json}
    
def getBrn(sessionId):
    if sessionId in brnSessionIdDict:
        return(brnSessionIdDict[sessionId])
    else:
        return(1)