import os
from typing import List
from fastapi.responses import FileResponse
from langchain_community.document_loaders import DirectoryLoader
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pathlib import Path
from fastapi import File, Form, UploadFile
import shutil

store = {}

import getpass
import os

CHROMA_ROOT_PATH = "chroma_db"
UPLOADED_FILE_PATH = "uploaded_dir"
USE_OPENAI = False

if USE_OPENAI:
    os.environ["OPENAI_API_KEY"] = "hidden"

if False:
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_API_KEY"] = "hidden"

def load_documents(chatbot_name: str):
    loader = DirectoryLoader(f"{UPLOADED_FILE_PATH}/{chatbot_name}", glob="**/*")
    documents = loader.load()
    
    # Assign metadata to each document
    for doc in documents:
        doc.metadata["group"] = chatbot_name

    print(f"Loaded {len(documents)} documents tagged as '{chatbot_name}'...")
    print(f"Documents have been loaded to be stored in the knowledge base...")
    return documents

def upload_documents(chatbot_name: str, answerMethod: str = Form(...), files: List[UploadFile] = File(...)) -> List:
    file_locations = []

    if files is None:
        return file_locations

    # Create the upload directory if it doesn't exist
    Path(f"{UPLOADED_FILE_PATH}").mkdir(exist_ok=True)
    Path(f"{UPLOADED_FILE_PATH}/{chatbot_name}").mkdir(exist_ok=True)
    
    for file in files:
        file_location = f"{UPLOADED_FILE_PATH}/{chatbot_name}/{file.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_locations.append(file_location)

    return file_locations

def store_knowledge(chatbot_name):
    # Initialize the vector store, loading from the persisted directory if it exists
    persist_directory = f"{CHROMA_ROOT_PATH}/{chatbot_name}"

    # Create the store db if it doesn't exist
    Path(f"{CHROMA_ROOT_PATH}").mkdir(exist_ok=True)
    Path(f"{CHROMA_ROOT_PATH}/{chatbot_name}").mkdir(exist_ok=True)

    # Load documents and tag them with the group
    docs = load_documents(chatbot_name=chatbot_name)

    # Split the documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=400)
    splits = text_splitter.split_documents(docs)

    # Refresh the knowledge base with existing and newly uploaded files
    delete_old_knowledge_base_in_chroma(persist_directory)

    vectorstore = Chroma(persist_directory=persist_directory, embedding_function= OpenAIEmbeddings() if USE_OPENAI else OllamaEmbeddings(model="mxbai-embed-large"))
    vectorstore.reset_collection()
    vectorstore.add_documents(splits)
    print("Finish storing knowledge...")

def delete_old_knowledge_base_in_chroma(directory):
    # This is the only file that should not be deleted
    exception_file = 'chroma.sqlite3'
    # Iterate through all files in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        # If it's a directory, remove it and its contents
        if os.path.isdir(file_path):
            shutil.rmtree(file_path)
            print(f"Deleted directory: {file_path}")
        
        # Check if it's a file (not a directory) and not the exception file
        if os.path.isfile(file_path) and filename != exception_file:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
    
def load_retriever(chatbot_name):
    persist_directory = f"{CHROMA_ROOT_PATH}/{chatbot_name}"
    if os.path.exists(persist_directory):
        vectorstore = Chroma(persist_directory=persist_directory, embedding_function=OpenAIEmbeddings() if USE_OPENAI else OllamaEmbeddings(model="mxbai-embed-large"))
        print(f"Document loaded for '{chatbot_name}':")
        # To check what is the loaded knowledge base files for a chatbot
        print_knowledge_base_files(vectorstore=vectorstore)
        return vectorstore.as_retriever(search_type="similarity_score_threshold", search_kwargs={"filter": {"group": chatbot_name}, "score_threshold": 0.7})
    
def is_document_stored(vectorstore, key):
    result = vectorstore.similarity_search(key, k=1)
    return len(result) > 0

def get_list_documents(chatbot_name) -> list:
    directory = f"{UPLOADED_FILE_PATH}/{chatbot_name}"
    documents = os.listdir(directory)
    return documents

def print_knowledge_base_files(vectorstore):
    # Convert list of dictionaries to a set of tuples (to make them hashable)
    unique_data_set = {tuple(sorted(item.items())) for item in vectorstore.get()["metadatas"]}
    # Convert back to list of dictionaries
    unique_data = [dict(item) for item in unique_data_set]
    for yeet in unique_data:
        print(yeet)

def get_rag_chain(llm, retriever, instructions):
    ### Contextualize question ###
    # contextualize_q_system_prompt = """Given a chat history and the latest user question \
    # which might reference context in the chat history, formulate a standalone question \
    # which can be understood without the chat history. Do NOT answer the question, \
    # just reformulate it if needed and otherwise return it as is."""
    contextualize_q_system_prompt = """Formulate a standalone question based on the latest user input. \
    Do NOT answer the question, just reformulate it if needed and otherwise return it as is."""
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            # MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    ### Answer question ###
    qa_system_prompt = """You are an assistant for question-answering tasks. \
    Use the following pieces of retrieved context to answer the question. \
    Focus on answering the question and DO NOT give suggestion unless asked. \
    If you don't know the answer, just say that you don't know. \
    """ + instructions + """
    {context}
    """
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            # MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    return rag_chain

def delete_file(chatbot_name: str, filename: str):
    return_message = ""
    try:
        # Construct the full file path
        file_path = os.path.join(f"{UPLOADED_FILE_PATH}/{chatbot_name}", filename)
        
        # Check if the file exists
        if os.path.isfile(file_path):
            os.remove(file_path)
            return_message = f"Deleted file: {file_path}"
        else:
            return_message = f"The file '{filename}' does not exist in the directory '{chatbot_name}'."
        
    except Exception as e:
        return_message = f"An error occurred: {e}"
    
    print(return_message)
    return return_message

def get_file(chatbot_name: str, filename: str):
    file_path = os.path.join(f"{UPLOADED_FILE_PATH}/{chatbot_name}", filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return f"File '{file_path}' cannot be found. It's either the file does not exist or the chatbot name does not exist."

def get_llm_model():
    return ChatOpenAI(model="gpt-4o-mini") if USE_OPENAI else ChatOllama(
        # model="cimbllm1:latest",
        model="gemma2:2b",
        temperature=0
        # other params...
    )
