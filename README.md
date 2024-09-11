# How to setup Backend server

The backend server uses the following stuff:

1. Ollama (to run the model)
2. FastAPI (backend Python framework)

## Step 1: Installing Ollama and the model

1. Install Ollama from https://ollama.com and follow the installation process. It should available in the terminal.
2. Get Gemma2 model and embedding model by running `ollama pull gemma2:2b` and `ollama pull mxbai-embed-large` (**NOTE**: the model has the size of **1.6GB**, make sure you have enough memory)
3. To check if the model is installed correctly, open terminal and run `ollama run gemma2:2b` and you should be able to have a chat with it.

## Step 2: Install the neccessary package for Python project

1. Make sure you have the minimum (you need a minimum python 3.8.1 & pip 24.2 which come together from python 3.8.1 to run this project) `python` and `pip` installed in your laptop. You can check if it's installed by running `python --version` (or `python3 --version`) and `pip --version` (or `pip3 --version`).
2. In the project directory, run `pip install -r requirements.txt` to install the dependency.

- install unvicorn, `pip install uvicorn`
  - ensure your uvicorn is in your env PATH
    `WARNING: The script uvicorn.exe is installed in 'C:\Users\yapya\AppData\Roaming\Python\Python38\Scripts' which is not on PATH`
  - Run this command:
  ```
  pip install uvicorn fastapi langchain langchain_community langchain_chroma langchain_ollama langchain_openai unstructured xmltodict pydantic bs4 python-multipart
  ```
  - Next run this command:
  ```
  pip install "unstructured[all-docs]"
  ```
  - download sqllite for your os type, https://www.sqlite.org/download.html, replace the dll and def file in C:\Program Files\Python38\DLLs

3. Try running the project with this command `uvicorn main:app --reload --port 8000`.
4. And then for the preprocessing server `uvicorn preprocessing:app --reload --port 8181`
5. [Conditional] If there is any missing dependency, just run this command `pip install <library_name>`

## Step 3: Test if your backend is running properly

1. You can run a GET request to this url http://localhost:8000/isready to determine if the chatbot is ready.

```

PS D:\CIMB\Hackathon\octoadvisor\llm-redbank> uvicorn main:app --reload
INFO: Will watch for changes in these directories: ['D:\\CIMB\\Hackathon\\octoadvisor\\llm-redbank']
INFO: Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO: Started reloader process [13824] using WatchFiles
INFO: Started server process [11108]
INFO: Waiting for application startup.
3
INFO: Application startup complete.
INFO: 127.0.0.1:59516 - "GET /isready HTTP/1.1" 200 OK

```

2. Start the preprocessing server at different port - uvicorn preprocessing:app --reload --port 8181

```

PS D:\CIMB\Hackathon\octoadvisor\llm-redbank> uvicorn preprocessing:app --reload --port 8181
INFO: Will watch for changes in these directories: ['D:\\CIMB\\Hackathon\\octoadvisor\\llm-redbank']
INFO: Uvicorn running on http://127.0.0.1:8181 (Press CTRL+C to quit)
INFO: Started reloader process [23056] using WatchFiles
INFO: Started server process [5468]
INFO: Waiting for application startup.
INFO: Application startup complete.
INFO: 127.0.0.1:59516 - "GET /isready HTTP/1.1" 200 OK

```

## To test preprocessing from postman

1. Test if chatbot is ready

```
curl --location 'http://127.0.0.1:8000/isready/sharif' \
--data ''
```

2. Create a session via send-brn

```
curl --location 'http://127.0.0.1:8181/send-brn' \
--header 'Content-Type: application/json' \
--data '{
    "brn":"1408874K"
}'
```

3. Update the bot with the latest training file (you only need to do it once).

You will need to create a form-data in the postman Body.

```
curl --location --request PUT 'http://127.0.0.1:8000/sharif/save' \
--form 'chatbot_title="sharif"' \
--form 'answerMethod="answer normally"' \
--form 'status="active"' \
--form 'files=@"/D:/CIMB/Hackathon/octoadvisor/llm-redbank/data/pdf/CTOS-Training-redflags.pdf"' \
--form 'description="bla bla bla"'
```
http://127.0.0.1:8000/sharif/save

4. copy the session-id from the send-brn response and replace the requests payload in askMe

```
curl --location 'http://127.0.0.1:8181/askMe' \
--header 'Content-Type: application/json' \
--data '{
    "query": "what is the total revenue in 2021, total revenue in 2020 and total revenue in 2022 and the sum of it for this data?",
    "session_id": "afcd3ac1-72ab-4ad6-a13b-a506ab04a636"
}'
```
