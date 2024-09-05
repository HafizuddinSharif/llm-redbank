from fastapi import FastAPI
from pydantic import BaseModel
from ctos_extractor import *
from main import *
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
sessionIdBrnDict = {}

brnSessionIdDict = {}

redflagsDict = {}

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

        sessionIdBrnDict.update({currentSessionId:customerData.brn})

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


@app.post("/bubble")
def bubble(query_txt: Query):
    print("calling bubble with: " + query_txt.query + " with session_id: " + query_txt.session_id)

    ## TODO: API for suggested bubble - redflags, 
    ## logic to define redflags
    if findSession(query_txt.session_id):
        print("session exist, check the target bubble")

        if (query_txt.query == 'redflags'):
            #print("find redflags")

            brn = getBrn(query_txt.session_id)
            print("brn from sessionId: ", brn)

            ## call findRedflags
            redflagsResponse = find_redflags(brn, query_txt.session_id)
    else:
        return("Session not FOUND, BRN info does not exist")
    
    return {query_txt.session_id:redflagsResponse}

 
def find_redflags(brn, session_id):
    print("call find_redflags API with brn:" + brn + ", and session_id: " + session_id)

    redflagsResponse = "NOT REDFLAG"
    redflagsDict = {}

    ## status = 1, customer has bankrupcy record
    extracted_bankruptcy_status = extract_bankruptcy_status(brn)
    print("extracted_bankruptcy_status: " + extracted_bankruptcy_status)
    
    ## status = 1, customer's related parties has bankrupcy record
    ## if both == 1 , customer and customer's related parties has bankruptcy record
    extracted_related_bankruptcy_status = extract_related_parties_bankruptcy(brn)
    print("extracted_related_bankruptcy_status: " + extracted_related_bankruptcy_status)

    if int(extracted_bankruptcy_status) == 1 and int(extracted_related_bankruptcy_status) == 1:
        redflagsResponse = "The customer and its related parties have bankruptcy records. Please perform your due diligence and proceed with caution."
        redflagsDict.update({"both_brankrupt":redflagsResponse})
        #return(redflagsResponse)

    if int(extracted_bankruptcy_status) == 1:
        redflagsResponse = "The customer has a bankruptcy record. Please perform your due diligence and proceed with caution."
        redflagsDict.update({"customer_bankrupt":redflagsResponse})
        #return(redflagsResponse)
    
    if int(extracted_related_bankruptcy_status) == 1:
        redflagsResponse = "The customer has related parties with a bankruptcy record. Please perform your due diligence and proceed with caution."
        redflagsDict.update({"customer_related_brankrupt":redflagsResponse})
        #return(redflagsResponse)

    ## redflag if gear ratio > 50
    extracted_latest_gear_ratio = extract_gear_ratio(brn)
    print("extracted_latest_gear_ratio: " + extracted_latest_gear_ratio)
    if float(extracted_latest_gear_ratio) > 50:
        redflagsResponse = "The customer has a very high gearing ratio of <" + extracted_latest_gear_ratio + "/100>. Please look into the customer’s financial reports to perform your due diligence. You can ask me to retrieve any number of financial data available in the CTOS reports."
        redflagsDict.update({"gear_ratio":redflagsResponse})
        #return(redflagsResponse)

    ## redflag if profit margin < 10
    extracted_profit_margin = extract_profit_margin(brn)
    print("extracted_profit_margin: " + extracted_profit_margin)
    if float(extracted_profit_margin) < 10:
        redflagsResponse = "The customer had a very poor profit margin of <" + extracted_profit_margin + ">. Please look into the customer’s financial reports to perform your due diligence. You can ask me to retrieve any number of financial data available in the CTOS reports."
        redflagsDict.update({"profit_margin":redflagsResponse})
        #return(redflagsResponse)

    ## if legalStatus == 1, then extract the name and date
    extracted_legal_status = extract_legal_status(brn)
    print("extracted_legal_status: " + str(extracted_legal_status))

    if not extracted_legal_status == 0:
        redflagsResponse = "The customer has records of legal proceedings. In particular, with regards to <" + extracted_legal_status['name'] +"> on <" + extracted_legal_status['date'] + ">."
        redflagsDict.update({"legal_status":redflagsResponse})
        #return(redflagsResponse)

    ## if extracted_msic_code in the msicHighRiskList then HIGHRISK
    msicHighRiskList = ["94920", "92000", "84220", "73200", "63910", "59120", "59110", "52249", "52241", "47736", "46619", "43124", "30400", "28240", "19201", "19100", "16291", "09900", "09101", "08999", "08996", "08995", "08994", "08993", "08992", "08991", "08918", "08917", "08916", "08915", "08913", "08912", "08911", "08108", "08107", "08104", "08103", "07799", "07797", "07796", "07795", "07794", "07793", "07792", "07791", "07721", "07701", "07605", "06104", "06103", "06101", "05100", "05200", "02203"]

    extracted_msic_code = extract_msic_codes(brn)
    print("extracted_msic_code: " + str(extracted_msic_code))
    if extracted_msic_code in msicHighRiskList:
        redflagsResponse = "The customer operates in a high risk industry code: <" + extracted_msic_code + ">."
        redflagsDict.update({"msic_code":redflagsResponse})
        #return(redflagsResponse)
    
    ## extracted_trex_ref == 0, not highrisk, ==1 is HIGH RISK
    extracted_trex_ref = extract_trex(brn)
    print("extracted_trex_ref: " + str(extracted_trex_ref))
    if extracted_trex_ref == 1:
        redflagsResponse = "The customer has records of negative non-bank monthly payment(s) (such as, but not limited to: rental, telco and utilities bill payments). As such, please perform due diligence."
        redflagsDict.update({"trex_ref":redflagsResponse})
        #return(redflagsResponse)

    ## 450 is days
    extracted_age_of_company = extract_age_of_company(brn)
    print("extracted_age_of_company: " + str(extracted_age_of_company))
    if int(extracted_age_of_company) < 450:
        redflagsResponse = "The customer’s age is too young, at only <" + str(extracted_age_of_company) + "> days old."
        redflagsDict.update({"age_of_company":redflagsResponse})
        #return(redflagsResponse)
    
    return(redflagsDict)


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

def getBrn(sessionId):
    if sessionId in sessionIdBrnDict:
        return(sessionIdBrnDict[sessionId])
    else:
        return(1)

