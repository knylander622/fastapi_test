from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Started via 'uvicorn main:app --reload'
app = FastAPI()

# Data model for an item, defines the shape of data clients send/receive
class Item(BaseModel):
    text: str
    isDone: bool = False

# In-memory storage for items (resets whenever the server restarts)
items = []

# Root endpoint
@app.get("/")
def root():
    return {"Hello" : "World"}

# Create a new item and add it to the in-memory list
@app.post("/items")
def create_item(item: Item):
    items.append(item)
    return items

# Return a list of items, limited to the first `limit` entries (default 10)
@app.get("/items", response_model=list[Item])
def list_items(limit: int = 10):
    return items[0:limit]

# Retrieve a single item by its index in the list
@app.get("/items/{item_id}", response_model=Item)
def get_items(item_id: int) -> Item:
    if(item_id < len(items)):
        return items[item_id]
    else:
        # Index out of range -> item doesn't exist, return 404
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found :(")
    
# Remove all items from the in-memory list
@app.post("/items/clear")
def remove_items():
    items.clear()
    return items