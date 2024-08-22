import os
from typing import List
import bs4
from langchain import hub
from langchain_community.document_loaders import DirectoryLoader, UnstructuredPDFLoader
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from pathlib import Path
from fastapi import File, Form, UploadFile
import shutil

store = {}

CHROMA_ROOT_PATH = "chroma_db"
UPLOADED_FILE_PATH = "uploaded_dir"

def load_documents_pdf():
    loader = DirectoryLoader("data", glob="*.pdf")

def load_documents_1():
    loader = DirectoryLoader("data", glob="**/*")
    documents = loader.load()
    print(len(documents))
    return documents

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

    # Create the upload directory if it doesn't exist
    Path(f"{UPLOADED_FILE_PATH}").mkdir(exist_ok=True)
    Path(f"{UPLOADED_FILE_PATH}/{chatbot_name}").mkdir(exist_ok=True)
    
    for file in files:
        file_location = f"{UPLOADED_FILE_PATH}/{chatbot_name}/{file.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_locations.append(file_location)

    return file_locations

def store_knowledge_2(chatbot_name) -> Chroma:
    docs = load_documents(chatbot_name=chatbot_name)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(documents=splits, embedding=OllamaEmbeddings(model="mxbai-embed-large"))

    # Retrieve and generate using the relevant snippets of the blog.
    retriever = vectorstore.as_retriever(f"group:{chatbot_name}", search_type="mmr")
    return retriever

def store_knowledge(chatbot_name):
    # Initialize the vector store, loading from the persisted directory if it exists
    persist_directory = f"{CHROMA_ROOT_PATH}/{chatbot_name}"
    duplicated = True

    # Load documents and tag them with the group
    docs = load_documents(chatbot_name=chatbot_name)

    # Split the documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # Check if it uploads the same documents
    # if os.path.exists(persist_directory):
    #     print("HERE NOW")
    #     vectorstore = Chroma(persist_directory=persist_directory, embedding_function=OllamaEmbeddings(model="mxbai-embed-large"))
    #     for split in splits:
    #         if not is_document_stored(vectorstore, split):
    #             logging.info(f"Document not found in vector store. Adding it...")
    #             duplicated = False
    #             break
    
    # if not duplicated:
    #     logging.info("Duplicated file uploaded. No new knowledge is being stored...")
    #     return
    vectorstore = Chroma(persist_directory=persist_directory, embedding_function=OllamaEmbeddings(model="mxbai-embed-large"))
    vectorstore.delete_collection()

    # Create and persist the vector store with metadata
    vectorstore = Chroma.from_documents(documents=splits, embedding=OllamaEmbeddings(model="mxbai-embed-large"), persist_directory=persist_directory)
    print("Finish storing knowledge...")

def load_knowledge(chatbot_name) -> Chroma:
    persist_directory = f"{CHROMA_ROOT_PATH}/{chatbot_name}"
    if os.path.exists(persist_directory):
        vectorstore = Chroma(persist_directory=persist_directory, embedding_function=OllamaEmbeddings(model="mxbai-embed-large"))
        return vectorstore.as_retriever()
    
def load_retriever(chatbot_name):
    persist_directory = f"{CHROMA_ROOT_PATH}/{chatbot_name}"
    if os.path.exists(persist_directory):
        vectorstore = Chroma(persist_directory=persist_directory, embedding_function=OllamaEmbeddings(model="mxbai-embed-large"))
        print(f"Found retriever for {chatbot_name}")
        return vectorstore.as_retriever(search_type="mmr", search_kwargs={"filter": {"group": chatbot_name}})
    
def is_document_stored(vectorstore, key):
    result = vectorstore.similarity_search(key, k=1)
    return len(result) > 0


# def get_session_history(session_id: str) -> BaseChatMessageHistory:
#     global store
#     if session_id not in store:
#         store[session_id] = ChatMessageHistory()
#     return store[session_id]

# def get_conversational_rag_chain(rag_chain):
#     ### Statefully manage chat history ###
#     conversational_rag_chain = RunnableWithMessageHistory(
#         rag_chain,
#         get_session_history,
#         input_messages_key="input",
#         history_messages_key="chat_history",
#         output_messages_key="answer",

#     )

#     return conversational_rag_chain

def get_rag_chain(llm, retriever, instructions):
    ### Contextualize question ###
    contextualize_q_system_prompt = """Given a chat history and the latest user question \
    which might reference context in the chat history, formulate a standalone question \
    which can be understood without the chat history. Do NOT answer the question, \
    just reformulate it if needed and otherwise return it as is."""
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    ### Answer question ###
    qa_system_prompt = """You are an assistant for question-answering tasks. \
    Use the following pieces of retrieved context to answer the question. \
    If you don't know the answer, just say that you don't know. \
    Use three sentences maximum and keep the answer concise.\
    """ + instructions + """
    {context}
    """
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    return rag_chain

def get_llm_model():
     return ChatOllama(
        model="gemma2:2b",
        temperature=0,
        # other params...
    )
     
# def main():

#     llm = get_llm_model()

#     retriever = store_knowledge()
#     rag_chain = get_rag_chain(llm=llm, retriever=retriever)
#     conversational_rag_chain = get_conversational_rag_chain(rag_chain=rag_chain)

#     query1 = conversational_rag_chain.invoke(
#         {"input": "What is Task Decomposition?"},
#         config={
#             "configurable": {"session_id": "abc123"}
#         },  # constructs a key "abc123" in `store`.
#     )
#     print(query1.get('answer'))

#     query2 = conversational_rag_chain.invoke(
#         {"input": "What are common ways of doing it?"},
#         config={"configurable": {"session_id": "abc123"}},
#     )
#     print(query2.get('answer'))

# if __name__ == "__main__":
#     main()