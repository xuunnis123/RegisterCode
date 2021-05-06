# app.py
from fastapi import FastAPI,Response,Request,Form,Depends,BackgroundTasks
from fastapi.responses import HTMLResponse,RedirectResponse,FileResponse,JSONResponse
from pydantic import BaseModel,Field
from typing import Optional, Text,List
from datetime import datetime
from rsa_company_gen import encode_rsa,generate_licensefile
from fastapi.templating import Jinja2Templates
import sqlalchemy
from sqlalchemy import and_
import databases
import starlette.status as status
import json
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

@app.get("/client/{q}")
@app.get("/")
async def main(request: Request,q:str=None):
    print("main")
    #.where(user==q)
    print("q=",q)

    if q is not None:
        user= sqlalchemy.sql.column('user')
        print(user)
        #query = notes.select(sqlalchemy.text('*')).where(user==q)
        query = notes.select().where(user==q)
    else:
        query = notes.select()
    all_item=await database.fetch_all(query)
    
    return templates.TemplateResponse("main.html", {"request": request,"all_item":all_item})

@app.get("/mac/{mac}")
async def main(request: Request,mac:str=None):
    print("main")
    #.where(user==q)

    print("mac=",mac)
  
    if mac is not None:
        mac_address= sqlalchemy.sql.column('mac_address')
        print(mac_address)
        #query = notes.select(sqlalchemy.text('*')).where(user==q)
        query = notes.select().where(mac_address==mac)
    else:
        query = notes.select()
    all_item=await database.fetch_all(query)
    
    return templates.TemplateResponse("main.html", {"request": request,"all_item":all_item})

@app.post('/register')
async def create(code:CodeIn):
    
  
    code_arg = code.expired + "_"
    code_arg+= code.mac_address
    encode=encode_rsa(code_arg)
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
    code_arg = code.expired + "_"
    code_arg+= code.mac_address
    encode=encode_rsa(code_arg)
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
    return FileResponse("licensefile.skm")


@app.get("/date/{date_bind}")
async def main(request: Request,date_bind:str=None):
    print("main")
    #.where(user==q)

    
    if date_bind.find("_") == 0:
        start = None
        end = date_bind[1:]
    if date_bind.find("_") == 8:
        start = date_bind.split("_")[0]
        if len(date_bind) > 9:
            end = date_bind.split("_")[1]
        else :
            end = None

    if start is not None and end is None:
        
        expired= sqlalchemy.sql.column('expired')
        
        #query = notes.select(sqlalchemy.text('*')).where(user==q)
        query = notes.select().where(expired >= start)
        
    elif start is None and end is not None:
        
        expired= sqlalchemy.sql.column('expired')
        
        #query = notes.select(sqlalchemy.text('*')).where(user==q)
        query = notes.select().where(expired <= end)
    elif start is not None and end is not None:
        
        expired= sqlalchemy.sql.column('expired')
        
        #query = notes.select(sqlalchemy.text('*')).where(user==q)
        query = notes.select().where(and_(expired >= start , expired <= end))
    else:
        
        query = notes.select()
    all_item = await database.fetch_all(query)
    
    return templates.TemplateResponse("main.html", {"request": request,"all_item":all_item})


