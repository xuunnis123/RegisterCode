# app.py
from fastapi import FastAPI,Response,Request,Form,Depends,BackgroundTasks
from fastapi.responses import HTMLResponse,RedirectResponse
from pydantic import BaseModel,Field
from typing import Optional, Text,List
from datetime import datetime
from rsa_company_gen import encode_rsa,generate_licensefile
from fastapi.templating import Jinja2Templates
import sqlalchemy
import databases
import starlette.status as status
DATABASE_URL = "sqlite:///./test.db"

metadata = sqlalchemy.MetaData()

database=databases.Database(DATABASE_URL)
notes=sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id",sqlalchemy.Integer,primary_key=True),
    sqlalchemy.Column("user",sqlalchemy.String(500)),
    sqlalchemy.Column("code",sqlalchemy.String(500)),
    sqlalchemy.Column("expired",sqlalchemy.String(500)),
    sqlalchemy.Column("mac_address",sqlalchemy.String(500)),

)
engine=sqlalchemy.create_engine(
    DATABASE_URL,connect_args={"check_same_thread":False}
)
metadata.create_all(engine)

app = FastAPI()


templates = Jinja2Templates(directory="templates")
codedb = []
all_item=[]
uni_item=[]
class CodeIn(BaseModel):
    user: str
    code: Optional[str]=False
    expired: str
    mac_address:str
# post model
class Code(BaseModel):
    id: int
    user: str
    code: Optional[str]=False
    expired: str
    mac_address:str

@app.on_event("startup")
async def connect():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
async def main(request: Request):
    print("main")
    query = notes.select()
    all_item=await database.fetch_all(query)
    return templates.TemplateResponse("main.html", {"request": request,"all_item":all_item})


@app.post('/register')
async def create(code:CodeIn):

    code_arg = code.expired
    code_arg+= code.mac_address
    encode=encode_rsa(code_arg,code.mac_address)
    #code.code=encode
    query=notes.insert().values(
        user=code.user,
        expired=code.expired,
        code=encode,
        mac_address=code.mac_address
    )
    record_id=await database.execute(query)
    return {
        "code":"ok",
        "message":"success"
    }
    #return templates.TemplateResponse('index.html',{'request': request})



@app.get('/register/{code_id}')
async def get_one(request:Request,code_id:int):
    query=notes.select().where(notes.c.id==code_id)
    print(query)
    uni_item=await database.fetch_one(query)

    print(uni_item)
    if uni_item is None:
        return{
            "code":"ok",
            "message":"no notes found"
        }
    return {
        "code":"ok",
        "message":"success",
        "user":uni_item['user'],
        "expired":uni_item['expired'],
        "mac_address":uni_item['mac_address']
    }


@app.put('/register/{code_id}')
async def update(code:CodeIn,code_id=int):
    code_arg = code.expired
    code_arg+= code.mac_address
    encode=encode_rsa(code_arg,code.mac_address)
    query=notes.update().where(notes.c.id==code_id).values(
        user=code.user,
        expired=code.expired,
        code=encode,
        mac_address=code.mac_address
    )
  
    record_id= await database.execute(query)
   
    query=notes.select().where(notes.c.id == record_id)
    user=await database.fetch_one(query)
    return {
        "code":"ok",
        "message":"success",
        "expired":code.expired,
        "mac_address":code.mac_address
    }


@app.delete("/register/{code_id}")
async def delete(code_id:int):
    print("delete")
    query=notes.delete().where(notes.c.id == code_id)
    await database.execute(query)
    return {
        "code":"ok",
        "Message":"Deleted Code "+ str(code_id)
    }

@app.get("/download/{code_id}")
async def download(code_id:int):
    query=notes.select().where(notes.c.id==code_id)
    print(query)
    uni_item=await database.fetch_one(query)
    generate_licensefile(uni_item.code)
    return {
        "code":"ok",
        "Message":"Downloaded"
    }
