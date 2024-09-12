from typing import List
import uuid
from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import FileResponse
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from contextlib import asynccontextmanager
from chatbot import get_file, store_knowledge, get_rag_chain, get_llm_model, upload_documents, load_retriever, get_list_documents, delete_file
from langchain_core.runnables.history import RunnableWithMessageHistory
from fastapi.middleware.cors import CORSMiddleware
from model import Filename, QueryObject

# ========================================================================
# Server state store here
# ========================================================================
store = {}
session_list = []
retriever = {}
rag_chain = {}
chatbot = {}
session_counter = 1
list_of_chatbot_name = ["sharif", "ace_portal"]
chatbots = {
    "sharif": {
        "id": 1,
        "name": "sharif",
        "title": "Sharif Chatbot",
        "description": "To talk about Sharif in general",
        "status": "active",
        "instruction": "You are Hafizuddin Sharif Bin Umar Sharif. You are going to answer the the user question like you are him."
    },
    "ace_portal": {
        "id": 2,
        "name": "ace_portal",
        "title": "ACE portal",
        "description": "To talk about SME loan products",
        "status": "inactive",
        "instruction": "You will be answering question related to loan products. If the user ask for your name, say 'I like mermaids'. Don't say 'I like mermaids' if the use didnt ask for your name"
    }
}

# ========================================================================
# Server configuration(s)
# ========================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Get LLM model
    print(f"Fetching model...")
    llm = get_llm_model()
    for chatbot_name in list_of_chatbot_name:
        setup_chatbot(chatbot_name=chatbot_name, llm=llm)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Angular default URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========================================================================
# Helper functions
# ========================================================================
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

def setup_chatbot(chatbot_name, llm):
    global retriever, chatbot
    retriever[chatbot_name] = load_retriever(chatbot_name)
    rag_chain[chatbot_name] = get_rag_chain(llm, retriever[chatbot_name], chatbots[chatbot_name]["instruction"])
    chatbot[chatbot_name] = get_conversational_rag_chain(rag_chain=rag_chain[chatbot_name])

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
    if query_obj.session_id not in session_list:
        return {"message": "No chat session started yet :("}
     
    query = chatbot[chatbot_name].invoke(
        {"input": query_obj.query},
        config={
            "configurable": {"session_id": query_obj.session_id}
        },  # constructs a key "abc123" in `store`.
    )

    return query

# ========================================================================
# POST request for creating chatbots in the back office
# ========================================================================
@app.post("/create-chatbot")
async def save_chatbot_settings(chatbot_title: str = Form(...), description: str = Form(...), answerMethod: str = Form(...), status: str = Form(...), files: List[UploadFile] = File(...)):
    # Set the name of the chatbot from the chatbot_title input
    chatbot_name = chatbot_title.replace(' ', '_').lower()

    # uploading documents
    file_locations = upload_documents(chatbot_name=chatbot_name, answerMethod=answerMethod, files=files)
    store_knowledge(chatbot_name=chatbot_name)

    # Saved/updated chatbot details
    chatbots[chatbot_name] = {
        "id": chatbots[chatbot_name]["id"] if chatbots.get(chatbot_name) != None else len(chatbots) + 1,
        "name": chatbot_name,
        "title": chatbot_title,
        "status": status,
        "description": description,
        "instruction": answerMethod
    }
    # Setup the saved/updated chatbot
    setup_chatbot(chatbot_name=chatbot_name, llm=get_llm_model())

    return {"info": f"{len(files)} files successfully uploaded!", "files": file_locations}

# ========================================================================
# GET request to get list of all chatbots
# ========================================================================
@app.get("/chatbots")
def get_all_chatbots():
    chatbots_list = list(chatbots.values())

    # To transform chatbots dict to list
    for bot in chatbots_list:
        print(bot.get("name"))
        bot["files"] = get_list_documents(bot.get("name"))

    return chatbots_list

# ========================================================================
# GET request to get a specific chatbot details
# ========================================================================
@app.get("/chatbots/{chatbot_name}")
def get_one_chatbot(chatbot_name: str):
    bot = chatbots.get(chatbot_name)
    bot["files"] = get_list_documents(bot.get("name"))
    return bot

# ========================================================================
# GET request to get session ID with a specific chatbot
# ========================================================================
@app.get("/start-session/{chatbot_name}")
def create_session(chatbot_name: str):
    # generate uuid
    session_id = str(uuid.uuid4())
    session_list.append(session_id)
    print("call create_session API with session_id: " + session_id)

    return(session_id)

@app.get("/download-pdf")
def download_pdf():
    file_path = "./uploaded_dir/sharif/dummyFile.txt"  # Replace with the actual path to the text file
    return FileResponse(file_path, media_type='text/plain', filename="downloaded_file.txt")

# ========================================================================
# PUT request for updating chatbots in the back office
# ========================================================================
@app.put("/{chatbot_name}/save")
async def save_chatbot_settings(chatbot_name: str, chatbot_title: str = Form(...), description: str = Form(...), answerMethod: str = Form(...), status: str = Form(...), files: List[UploadFile] = File(...)):
    # uploading documents
    file_locations = upload_documents(chatbot_name=chatbot_name, answerMethod=answerMethod, files=files)
    store_knowledge(chatbot_name=chatbot_name)

    # Saved/updated chatbot details
    chatbots[chatbot_name] = {
        "id": chatbots[chatbot_name]["id"] if chatbots.get(chatbot_name) != None else len(chatbots) + 1,
        "name": chatbot_name,
        "title": chatbot_title,
        "description": description,
        "status": status,
        "instruction": answerMethod
    }
    # Setup the saved/updated chatbot
    setup_chatbot(chatbot_name=chatbot_name, llm=get_llm_model())

    return {"info": f"{len(files)} files successfully uploaded!", "files": file_locations}


# ========================================================================
# DELETE request to delete a file based on given filename
# ========================================================================
@app.delete("/{chatbot_name}/delete-file")
async def delete_file_given_filename(chatbot_name: str, filename: Filename):
    response = delete_file(chatbot_name=chatbot_name, filename=filename.filename)
    return {"success": True, "message": response}

# ========================================================================
# GET request to view/download a file
# ========================================================================
@app.get("/{chatbot_name}/file/{filename}")
async def get_filen_given_filename(chatbot_name: str, filename: str):
    response = get_file(chatbot_name=chatbot_name, filename=filename)
    return response
