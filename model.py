from pydantic import BaseModel

class QueryObject(BaseModel):
    query: str
    session_id: str

class CustomerData(BaseModel):
    brn: str

class Filename(BaseModel):
    filename: str