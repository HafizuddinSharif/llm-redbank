# How to setup Backend server

The backend server uses the following stuff:

1. Ollama (to run the model)
2. FastAPI (backend Python framework)

## Step 1: Installing Ollama and the model

1. Install Ollama from https://ollama.com and follow the installation process. It should available in the terminal.
2. Get Gemma2 model and embedding model by running `ollama pull gemma2:2b` and `ollama pull mxbai-embed-large` (**NOTE**: the model has the size of **1.6GB**, make sure you have enough memory)
3. To check if the model is installed correctly, open terminal and run `ollama run gemma2:2b` and you should be able to have a chat with it.

## Step 2: Install the neccessary package for Python project

1. Make sure you have the latest `python` and `pip` installed in your laptop. You can check if it's installed by running `python --version` and `pip --version`
    - you need a minimum python 3.8.1 & pip 24.2 which come together from python 3.8.1 to run this project
    - install unvicorn, `pip install uvicorn`
    - ensure your uvicorn is in your env PATH
    `WARNING: The script uvicorn.exe is installed in 'C:\Users\yapya\AppData\Roaming\Python\Python38\Scripts' which is not on PATH.`
    - pip install xmltodict
    - pip install fastapi
    - pip install langchain
    - pip install pydantic
    - pip install langchain_community
    - pip install bs4
    - pip install langchain_chroma
    - download sqllite for your os type, https://www.sqlite.org/download.html, replace the dll and def file in C:\Program Files\Python38\DLLs
    - pip install langchain_ollama
    - pip install python-multipart
    - pip install unstructured
    - pip install "unstructured[md]"
    - pip install "unstructured[pdf]"
2. In the project directory, run `pip install -r requirements.txt` to install the dependency.
3. Try running the project with this command `uvicorn main:app --reload`.
4. [Conditional] If there is any missing dependency, just run this command `pip install <library_name>`

## Step 3: Test if your backend is running properly

1. You can run a GET request to this url http://localhost:8000/isready to determine if the chatbot is ready.

##
PS D:\CIMB\Hackathon\octoadvisor\llm-redbank> uvicorn main:app --reload
INFO:     Will watch for changes in these directories: ['D:\\CIMB\\Hackathon\\octoadvisor\\llm-redbank']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [13824] using WatchFiles
INFO:     Started server process [11108]
INFO:     Waiting for application startup.
3
INFO:     Application startup complete.
INFO:     127.0.0.1:59516 - "GET /isready HTTP/1.1" 200 OK
##