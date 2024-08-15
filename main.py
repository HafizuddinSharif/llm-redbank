from typing import List
from fastapi import FastAPI, Form
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from contextlib import asynccontextmanager
from chatbot import store_knowledge, get_rag_chain, get_llm_model
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_chroma import Chroma
from pydantic import BaseModel
from ctos_extractor import extract_xml
import json
from fastapi import FastAPI, File, UploadFile
import shutil
from pathlib import Path

from fastapi.middleware.cors import CORSMiddleware

store = {}
retriever = None
chatbot = None

class Query(BaseModel):
    query: str

class CustomerData(BaseModel):
    brn: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    global retriever, chatbot
    # Get LLM model
    llm = get_llm_model()
    # load document for LLM knowledge
    retriever = store_knowledge()
    rag_chain = get_rag_chain(llm, retriever)
    chatbot = get_conversational_rag_chain(rag_chain=rag_chain)
    yield
    # Clean up
    # retriever.delete_collection()

def get_session_history(session_id: str) -> BaseChatMessageHistory:
        global store
        if session_id not in store:
            store[session_id] = ChatMessageHistory()
        return store[session_id]

def get_conversational_rag_chain(rag_chain):
    ### Statefully manage chat history ###
    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )

    return conversational_rag_chain

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Angular default URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/isready")
def is_ready():
    if (chatbot is not None):
        return {"message": "Chatbot is ready :)"}
     
    return {"message": "Chatbot is not ready :("}

@app.post("/start-chat")
async def start_chat(customerData: CustomerData):
    if (chatbot is None):
        return {"message": "Chatbot is not ready :("}
    
    extracted_xml = extract_xml(customerData.brn)
    if extracted_xml is None:
        return {"response": "BRN number does not have the CTOS data"}

    ctos_data = json.dumps(extracted_xml)
    
    question = 'Can you suggest up to 3 product(s) with this data: ' + ctos_data
    
    query = chatbot.invoke(
        {"input": question},
        config={
            "configurable": {"session_id": "abc123"}
        },  # constructs a key "abc123" in `store`.
    )

    return query

@app.post("/chat")
async def on_chat(query_txt: Query):
    if (store is None):
        return {"message": "No chat session started yet :("}
     
    query = chatbot.invoke(
        {"input": query_txt.query},
        config={
            "configurable": {"session_id": "abc123"}
        },  # constructs a key "abc123" in `store`.
    )

    return query

UPLOAD_DIRECTORY = "uploaded_files"

# Create the upload directory if it doesn't exist
Path(UPLOAD_DIRECTORY).mkdir(exist_ok=True)

@app.post("/upload-multiple/{chatbot_name}")
async def upload_multiple_files(chatbot_name: str, files: List[UploadFile] = File(...)):
    file_locations = []
    
    for file in files:
        file_location = f"{chatbot_name}/{file.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_locations.append(file_location)

    return {"info": f"{len(files)} files successfully uploaded!", "files": file_locations}

@app.post("/upload")
async def upload_files(
    chatbotName: str = Form(...), answerMethod: str = Form(...), files: List[UploadFile] = File(...)
):
    file_names = [file.filename for file in files]
    return {"chatbotName": chatbotName, "answerMethod": answerMethod, "files": file_names}