from fastapi import FastAPI

app = FastAPI()

@app.post("/send-brn")
def send_brn_start_conversation():
    # Add logic here
    return