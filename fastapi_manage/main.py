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
    return templates.TemplateResponse("code_list.html", {"request": request,"all_item":all_item})


@app.post('/register',response_class=HTMLResponse)
async def create(request:Request,user:str=Form(...),expired:str=Form(...),mac_address:str=Form(...)):
    print("creating")
    print("user:",user)
    code_arg = expired
    code_arg+= mac_address
    encode=encode_rsa(code_arg,mac_address)
    #code.code=encode
    query=notes.insert().values(
        user=user,
        expired=expired,
        code=encode,
        mac_address=mac_address
    )
    record_id=await database.execute(query)
    return RedirectResponse(url='/',status_code=status.HTTP_302_FOUND)
    #return templates.TemplateResponse('index.html',{'request': request})



@app.get("/create")
async def create_form(request:Request):
    print("create")
    return templates.TemplateResponse('code_form.html',{"request":request,"notes":all_item})

@app.get("/register/")
async def read_notes(request:Request):
    print("read")
    query = notes.select()
    all_item=await database.fetch_all(query)
    return templates.TemplateResponse('code_list.html',{"request":request,"notes":all_item})


@app.get('/register/{code_id}',response_model=Code)
async def get_one(request:Request,code_id:int):
    query=notes.select().where(notes.c.id==code_id)
    print(query)
    uni_item=await database.fetch_one(query)


    return  templates.TemplateResponse('code_detail.html',{"request":request,"row":uni_item,"user":uni_item['user'],"code":uni_item['code'],"expired":uni_item['expired'],"mac_address":uni_item['mac_address']})

@app.get('/update/{code_id}',response_model=Code)
def jump_to_update(request:Request,code_id:int,row:list):
    print("row=",row)
    return  templates.TemplateResponse('code_update.html',{"request":request,"code_id":code_id,"row":uni_item})

@app.put('/register/{code_id}',response_model=Code,response_model_include={"id", "user","code","expired","mac_address"})
async def update(code_id:int ,r: CodeIn=Depends()):
    code_arg = r.expired
    code_arg+= r.mac_address
    encode=encode_rsa(code_arg,r.mac_address)
    
    query=notes.update().where(notes.c.id==code_id).values(
        user=r.user,
        expired=r.expired,
        code=encode,
        mac_address=r.mac_address
    )
  
    record_id= await database.execute(query)
   
    query=notes.select().where(notes.c.id == record_id)
    user=await database.fetch_one(query)
    return user

@app.get("/delete/{code_id}")
def jump_to_confirm_delete(request:Request,code_id:int):
    print("jump_to_confirm_delete")
    return  templates.TemplateResponse('code_confirm_delete.html',{"request":request,"code_id":code_id})

@app.delete("/register/{code_id}",response_model=Code)
async def delete(code_id:int):
    print("delete")
    query=notes.delete().where(notes.c.id == code_id)
    await database.execute(query)
    return RedirectResponse('/')
######
@app.get("/code")
def get_posts():
    return codedb
# ADD
@app.post("/code")
def add_post(code: Code):
    code_arg = code.expired
    code_arg+= code.mac_address
    encode=encode_rsa(code_arg,code.mac_address)
    code.code=encode
    #generate_licensefile(encode)
    codedb.append(code.dict())
    return codedb[-1]

@app.get("/code/{code_id}")
def get_post(code_id: int):
    code = code_id - 1
    return codedb[code]

@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})

# Update
@app.post("/code/{code_id}")
def update_post(code_id: int, code: Code):
    
    code.user=codedb[code_id]['user']
    date= code.expired
    machine_code= code.mac_address

    code_arg = date
    code_arg+= machine_code
    encode=encode_rsa(code_arg,code.mac_address)
    code.code=encode
    #generate_licensefile(encode)
    code.mac_address=codedb[code_id]['mac_address']
    codedb[code_id] = code
    
    return {"message": "Code has been updated succesfully"}


# Delete
@app.delete("/code/{code_id}")
def delete_post(code_id: int):
    codedb.pop(code_id-1)
    return {"message": "Post has been deleted succesfully"}



@app.get("/items/")
async def read_items():
    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/legacy/")
def get_legacy_data():
    data = """<?xml version="1.0"?>
    <shampoo>
    <Header>
        Apply shampoo here.
    </Header>
    <Body>
        You'll have to use soap here.
    </Body>
    </shampoo>
    """
    return Response(content=data, media_type="application/xml")




@app.get('/download')
def form_post(request: Request):
    result = 'Type a number'
    
    return templates.TemplateResponse('/item.html', context={'request': request, 'result': result})

@app.get('/test', response_class=HTMLResponse)
def form_post(request: Request):
    result = 'Type a number'
    
    return templates.TemplateResponse('/item.html', context={'request': request, 'result': result})