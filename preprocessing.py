from fastapi import FastAPI
from pydantic import BaseModel
from main import *
import uuid

class Query(BaseModel):
    query: str
    session_id: str

class CustomerData(BaseModel):
    brn: str

app = FastAPI()

@app.post("/send-brn")
def send_brn_start_conversation(customerData: CustomerData):
    # Add logic here
    print("send-brn with brn: " + customerData.brn)

    # generate uuid
    currentUUID = str(uuid.uuid4())

    print("Your sessionId: " + currentUUID)

    # create user session at mainBot
    createSession(customerData.brn, currentUUID)

    return currentUUID


@app.post("/askMe")
def askMe(query_txt: Query, ):
    # Add logic here
    print("calling askMe with: " + query_txt.query + " with session_id: " + query_txt.session_id)

    # send question to mainBot

    return {"askMe successful"}


