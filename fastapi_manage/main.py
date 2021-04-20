# app.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Text
from datetime import datetime
from rsa_company_gen import encode_rsa
app = FastAPI()

codedb = []

# post model
class Code(BaseModel):
    id: int
    user: str
    code: Optional[str]=False
    expired: str
    mac_address:str

@app.get("/")
def read_root():
  return {"home": "Home page"}

@app.get("/code")
def get_posts():
    return codedb

@app.post("/code")
def add_post(code: Code):
    codedb.append(code.dict())
    return codedb[-1]

@app.get("/code/{code_id}")
def get_post(code_id: int):
    code = code_id - 1
    return codedb[code]

# Update
@app.post("/code/{code_id}")
def update_post(code_id: int, code: Code):
    
    code.user=codedb[code_id]['user']
    date= codedb[code_id]['expired']
    machine_code= codedb[code_id]['mac_address']

    code_arg = date
    code_arg+= machine_code

    code.expired=codedb[code_id]['expired']
    code.code=encode_rsa(code_arg,machine_code)

    code.mac_address=codedb[code_id]['mac_address']
    codedb[code_id] = code
    
    return {"message": "Code has been updated succesfully"}


# Delete
@app.delete("/code/{code_id}")
def delete_post(code_id: int):
    codedb.pop(code_id-1)
    return {"message": "Post has been deleted succesfully"}