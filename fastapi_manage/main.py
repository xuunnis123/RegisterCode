from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

class Item(BaseModel):
    user: str
    code: Optional[str] = None
    expired: str
    mac_address: str


@app.post("/items/")
async def create_item(item: Item):
    return item

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]