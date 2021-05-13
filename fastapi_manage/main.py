# app.py
from sqlalchemy.sql.expression import null
from fastapi import FastAPI,Response,Request,Form,Depends,BackgroundTasks
from fastapi.responses import HTMLResponse,RedirectResponse,FileResponse,JSONResponse
from pydantic import BaseModel,Field
from typing import Optional, Text,List
from datetime import date, datetime
from rsa_company_gen import encode_rsa,generate_licensefile
from fastapi.templating import Jinja2Templates
import sqlalchemy
from sqlalchemy import and_
import databases
import starlette.status as status
import json
from datetime import datetime

DATABASE_URL = "sqlite:///./test.db"

metadata = sqlalchemy.MetaData()

database=databases.Database(DATABASE_URL)
notes=sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id",sqlalchemy.Integer,primary_key=True),
    sqlalchemy.Column("client",sqlalchemy.String(500)),
    sqlalchemy.Column("code",sqlalchemy.String(500)),
    sqlalchemy.Column("expired",sqlalchemy.String(500)),
    sqlalchemy.Column("uuid",sqlalchemy.String(500)),
    sqlalchemy.Column("created_time",sqlalchemy.DateTime),
    sqlalchemy.Column("edited_time",sqlalchemy.DateTime),

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
    client: str
    code: Optional[str]=False
    expired: str
    uuid:str
    created_time:Optional[datetime]=False
    edited_time:Optional[datetime]=False
# post model
class Code(BaseModel):
    id: int
    client: str
    code: Optional[str]=False
    expired: str
    uuid:str
    created_time:Optional[datetime]=False
    edited_time:Optional[datetime]=False

@app.on_event("startup")
async def connect():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/page/{now}")
@app.get("/client/{q}/page/{now}")
@app.get("/client/{q}")
@app.get("/")
async def main(request: Request,q:str=None, now:str=None):

    now_page = 1
    select_client=""
    if q is not None:
        client= sqlalchemy.sql.column('client')
        select_client=q
    
        query = notes.select().where(client==q)
    else:
        query = notes.select()
    all_item=await database.fetch_all(query)

    count,page = cut_page(all_item)
    

    pre_page = 0
    next_page = 0
    
    if now is not None:
     
        pre_page,now,next_page,all_item = pagination(now,pre_page,next_page,page,all_item)
    else:
  
        now=1
        pre_page = 1
        next_page = 2
        pre_page,now,next_page,all_item = pagination(now_page,pre_page,next_page,page,all_item)

        
    return templates.TemplateResponse("main.html", {"request": request,"all_item" : all_item, "count" : count, "page" : page ,"now" : now ,"pre_page": pre_page, "next_page": next_page, "select_client": select_client})

@app.get("/uuid/{uuid}/page/{now}")
@app.get("/uuid/{uuid}")
async def main(request: Request,uuid:str=None,now:str=None):


    select_uuid=""
    if uuid is not None:
        uuid= sqlalchemy.sql.column('uuid')
        select_uuid=uuid
       
    
        query = notes.select().where(uuid == uuid)
    else:
        query = notes.select()
    all_item=await database.fetch_all(query)
    count,page = cut_page(all_item)
    

    pre_page = 0
    next_page = 0
    now_page=1
    if now is not None:
       
        pre_page,now,next_page,all_item = pagination(now,pre_page,next_page,page,all_item)
    else:
        
        now=1
        pre_page = 1
        next_page = 2
        pre_page,now,next_page,all_item = pagination(now_page,pre_page,next_page,page,all_item)

    return templates.TemplateResponse("main.html", {"request": request,"all_item":all_item,"select_uuid":select_uuid,"count" : count, "page" : page ,"now" : now ,"pre_page": pre_page, "next_page": next_page})

@app.post('/register')
async def create(code:CodeIn):
    
  
    code_arg = code.expired + "_"
    code_arg+= code.uuid
    encode=encode_rsa(code_arg)
    #code.code=encode
    query=notes.insert().values(
        client=code.client,
        expired=code.expired,
        code=encode,
        uuid = code.uuid,
        created_time = datetime.now(),
        edited_time = datetime.now(),
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
    
    uni_item=await database.fetch_one(query)

    if uni_item is None:
        return{
            "code":"ok",
            "message":"no notes found"
        }
    return {
        "code":"ok",
        "message":"success",
        "client":uni_item['client'],
        "expired":uni_item['expired'],
        "uuid":uni_item['uuid']
    }


@app.put('/register/{code_id}')
async def update(code:CodeIn,code_id=int):
   
    code_arg = code.expired + "_"
    code_arg+= code.uuid
    encode=encode_rsa(code_arg)
    query=notes.update().where(notes.c.id==code_id).values(
        client=code.client,
        expired=code.expired,
        code=encode,
        uuid=code.uuid,
        edited_time = datetime.now(),
    )
  
    record_id= await database.execute(query)
    
    query=notes.select().where(notes.c.id == record_id)
    client=await database.fetch_one(query)
    
    return {
        "code":"ok",
        "message":"success",
        "expired":code.expired,
        "uuid":code.uuid
    }


@app.delete("/register/{code_id}")
async def delete(code_id:int):
   
    query=notes.delete().where(notes.c.id == code_id)
    await database.execute(query)
    return {
        "code":"ok",
        "Message":"Deleted Code "+ str(code_id)
    }

@app.get("/download/{code_id}")
async def download(code_id:int):
    query=notes.select().where(notes.c.id==code_id)

    uni_item=await database.fetch_one(query)
    generate_licensefile(uni_item.code)
    return FileResponse("licensefile.skm")

@app.get("/date/{pass_date}/page/{now}")
@app.get("/date/{date_bind}")
async def main(request: Request,date_bind:str=None,now:str=None,pass_date:str=None):

    start_time=""
    end_time=""
    now_page = 1
    if pass_date is not None:
        date_bind = pass_date

    
    if date_bind.find("_") == 0:
        start = None
        end = date_bind[1:]
        end_time = end
    if date_bind.find("_") == 8:
        start = date_bind.split("_")[0]
        start_time=start
        if len(date_bind) > 9:
            end = date_bind.split("_")[1]
            end_time = end
        else :
            end = None

    if start is not None and end is None:
        
        expired= sqlalchemy.sql.column('expired')
     
        query = notes.select().where(expired >= start)
        
    elif start is None and end is not None:
        
        expired= sqlalchemy.sql.column('expired')

        query = notes.select().where(expired <= end)
    elif start is not None and end is not None:
        
        expired= sqlalchemy.sql.column('expired')

        query = notes.select().where(and_(expired >= start , expired <= end))
    else:
        
        query = notes.select()
    all_item = await database.fetch_all(query)

    count,page = cut_page(all_item)
    

    pre_page = 0
    next_page = 0
    
    if now is not None:
  
        pre_page,now,next_page,all_item = pagination(now,pre_page,next_page,page,all_item)
    else:
  
        now = 1
        pre_page = 1
        next_page = 2
        pre_page,now,next_page,all_item = pagination(now_page,pre_page,next_page,page,all_item)
    
    return templates.TemplateResponse("main.html", {"request": request,"all_item":all_item, "count" : count, "page" : page ,"now" : now ,"pre_page": pre_page, "next_page": next_page,"start_time":start_time,"end_time":end_time})

def cut_page(all_item):
    count = len(all_item)

    
    if count%5 == 0:
      page = count//5
    else:
      page = count//5 +1
    return count,page
def pagination(now,pre_page,next_page,page,all_item):
    now_page=int(now)
   
    start_item = (now_page - 1)*5
    end_item = start_item + 5
    all_item = all_item[start_item:end_item]

    if now_page > 1 and now_page < page:
        next_page = now_page + 1
        if now_page-1 >0:
            pre_page = now_page - 1
        else:
            pre_page = 1
        
    elif now_page == 1 and now_page < page:
        next_page = now_page + 1
        pre_page = 1
    elif now_page > 1 and now_page == page:
        next_page = now_page
        if now_page-1 >0:
            pre_page = now_page - 1
        else:
            pre_page = 1
    else:#now_page == 1 and now_page == page
        next_page = 1
        pre_page = 1
    return pre_page,now,next_page,all_item