from fastapi import FastAPI, Depends
from pydantic import BaseModel

# consider also https://fastapi.tiangolo.com/tutorial/static-files/

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None
    amazon_prime: bool = True

@app.get("/")
def read_root():
    return {"Hello": "World!"}



# i.e. http://127.0.0.1:8000/items/5?q=somequery
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    """
      Try http://127.0.0.1:8000/items/5?q=somequery

    """
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

def login_data(user: str, api_key: str):
    return { "api_pass": user+"@"+api_key}

# See https://fastapi.tiangolo.com/tutorial/security/http-basic-auth/
@app.put("/login")
def login(login_data: dict = Depends(login_data)):
    login_data["result"]="logged_in"
    return login_data

## Slow down  alert
import logging,time
from starlette.requests import Request

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    if process_time >0.02:
        logging.warn(str(request.url) +" Executed into: "+str(process_time))
    return response