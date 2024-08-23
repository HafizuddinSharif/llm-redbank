from typing import List
from fastapi import FastAPI, Form, File, UploadFile
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from contextlib import asynccontextmanager
from chatbot import store_knowledge, get_rag_chain, get_llm_model, upload_documents, load_retriever
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_chroma import Chroma
from pydantic import BaseModel
from ctos_extractor import extract_xml
import json
import shutil
from pathlib import Path
import sys

from fastapi.middleware.cors import CORSMiddleware

from model import CustomerData, QueryObject

store = {}
retriever = {
    "sme_products": None,
    "ace_portal": None
}
rag_chain = {
    "sme_products": None,
    "ace_portal": None
}
chatbot = {
    "sme_products": None,
    "ace_portal": None
}
list_of_chatbot_name = ["sharif"]
chatbots = [
    {
        "id": 1,
        "name": "ace_portal",
        "title": "ACE portal",
        "status": "inactive",
        "instruction": "You will be answering question related to loan products. If the user ask for your name, say 'I like mermaids'. Don't say 'I like mermaids' if the use didnt ask for your name"
    },
    {
        "id": 2,
        "name": "sme_products",
        "title": "SME Loan Products Chatbot",
        "status": "inactive"
    },
    {
        "id": 3,
        "name": "sharif",
        "title": "Sharif Chatbot",
        "status": "active"
    },
]
session_counter = 1

@asynccontextmanager
async def lifespan(app: FastAPI):
    global retriever, chatbot
    # Get LLM model
    print(f"Fetching model...")
    llm = get_llm_model()

    for chatbot_name in list_of_chatbot_name:
        retriever[chatbot_name] = load_retriever(chatbot_name)
        rag_chain[chatbot_name] = get_rag_chain(llm, retriever[chatbot_name], chatbots[0]["instruction"])
        chatbot[chatbot_name] = get_conversational_rag_chain(rag_chain=rag_chain[chatbot_name])

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

# ========================================================================
# GET request to check if chatbot is ready
# ========================================================================

@app.get("/isready/{chatbot_name}")
def is_ready(chatbot_name: str):
    if (chatbot[chatbot_name] is not None):
        return {"message": "Chatbot is ready :)"}
     
    return {"message": "Chatbot is not ready :("}

# ========================================================================
# POST request for first query and it will return generated session id
# ========================================================================

@app.post("/start-chat/{chatbot_name}")
async def start_chat(chatbot_name: str, query: QueryObject):
    global session_counter
    if (chatbot[chatbot_name] is None):
        return {"message": "Chatbot is not ready :("}

    generated_session_id = "session_" + str(session_counter)
    session_counter += 1
    
    query = chatbot[chatbot_name].invoke(
        {"input": query.query},
        config={
            "configurable": {"session_id": generated_session_id}
        },  # constructs a key "abc123" in `store`.
    )

    query["session_id"] = generated_session_id

    return query

# ========================================================================
# POST request for continuing conversation. Should supply session id
# ========================================================================
@app.post("/chat/{chatbot_name}")
async def on_chat(chatbot_name: str, query_obj: QueryObject):
    print(f"STORE: {store}")
    if not bool(store):
        return {"message": "No chat session started yet :("}
     
    query = chatbot[chatbot_name].invoke(
        {"input": query_obj.query},
        config={
            "configurable": {"session_id": query_obj.session_id}
        },  # constructs a key "abc123" in `store`.
    )

    return query

UPLOAD_DIRECTORY = "knowledge_base_dir"

# ========================================================================
# POST request for saving/creating chatbots in the back office
# ========================================================================
@app.post("/{chatbot_name}/save")
async def save_chatbot_settings(chatbot_name: str, chatbot_title: str = Form(...), answerMethod: str = Form(...), files: List[UploadFile] = File(...)):
    # uploading documents
    file_locations = upload_documents(chatbot_name=chatbot_name, answerMethod=answerMethod, files=files)
    store_knowledge(chatbot_name=chatbot_name)

    chatbots.append({
        "id": len(chatbots) + 1,
        "name": chatbot_name,
        "title": chatbot_title,
        "status": "active",
        "instruction": answerMethod

    })

    return {"info": f"{len(files)} files successfully uploaded!", "files": file_locations}

# ========================================================================
# GET request to get list of all chatbots
# ========================================================================
@app.get("/chatbots")
def get_all_chatbots():
    return chatbots

def createSession(brn, session_id):
    print("call createSession API with brn:" + brn + ", and session_id: " + session_id)

    return{"createSession OK"}