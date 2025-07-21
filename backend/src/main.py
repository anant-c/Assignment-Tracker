from fastapi import FastAPI, HTTPException, Depends
from typing import List, Annotated


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

