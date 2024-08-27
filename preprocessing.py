from fastapi import FastAPI
from pydantic import BaseModel
from main import *
import uuid
import requests

class Query(BaseModel):
    query: str
    session_id: str

class CustomerData(BaseModel):
    brn: str

brnDict = {}

app = FastAPI()

@app.post("/testData")
def testData():
    getBrnData("1408874")
    getBrnData("1408888")

    return{"testData completed"}

@app.post("/send-brn")
def send_brn_start_conversation(customerData: CustomerData):
    # Add logic here
    print("send-brn with brn: " + customerData.brn)

    # generate uuid
    currentUUID = str(uuid.uuid4())

    ## TODO: call main API /start-session/{chatbot_name} to get sessionId

    #print("Your sessionId: " + currentUUID)

    # create user session at mainBot
    processing_ctos_data(customerData.brn, currentUUID)

    return {"session created with session_id: " + currentUUID}


@app.post("/askMe")
def askMe(query_txt: Query):
    # Add logic here
    print("calling askMe with: " + query_txt.query + " with session_id: " + query_txt.session_id)

    # send question to mainBot

    ################################
    # check if session id exist, if exist, call /chat, if not exist call /sharif

    ## TODO: call /chat/{chatbot_name}
    '''
    {
        "query": formulate_query,
        "session_id": session_id
    }

    response
    {
        "message": "New session for the BRN XXXXXX have been created",
        "session_id": "XXXXXX-XXXXXX-XXXXXX"
    }
    '''

    # check also if bot is ready before calling url below
    url = 'http://127.0.0.1:8000/start-chat/sharif'
    data = {"brn": "1408874K"}
    response = requests.post(url, json=data)
    print(response.text)
    #start_chat("sharif", CustomerData)

    return {"askMe successful"}

def processing_ctos_data(brn, session_id):
    print("call processing_ctos_data API with brn:" + brn + ", and session_id: " + session_id)

    extracted_xml = extract_xml(brn)
    if extracted_xml is None:
        return {"response": "BRN number does not have the CTOS data"}

    ctos_data = json.dumps(extracted_xml)

    if brn in brnDict:
        print("brn data exists, do nothing")
    else:
        print("brn data NOT exists, update dict")
        brnDict.update({brn:ctos_data})

    #for x, y in brnDict.items():
    #    print(x, y)

    return{"createSession OK"}

## a method to return data from the dictionary
def getBrnData(brn):
    print("call getBrnData API with brn:" + brn)

    currentBrnData = brnDict.get("1408874K")

    print("=======================")
    print(currentBrnData)

