from fastapi import FastAPI,Response,status,HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel

from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas, utils
from sqlalchemy.orm import Session
from .database import engine, get_db
from .routes import post, user, auth
models.Base.metadata.create_all(bind = engine)

app = FastAPI()


try:
    conn = psycopg2.connect(host = 'localhost', database = 'fastapi',user = 'postgres', password = 'keerti@1009', cursor_factory= RealDictCursor)
    cursor = conn.cursor()
    print("Database:", conn.info.dbname)
    print("Host:", conn.info.host)
    print("Port:", conn.info.port)
    print("User:", conn.info.user)
    print("Database connection was succesfull")

except Exception as error:
    print("Connecting to database failed")
    print("Error :", error)
    time.sleep(2)

my_posts = [{"title" : "title of posts 1", "content" : "content of post 1", "id" : 1}, {"title": "favourite foods", "content": "I like pizza", "id": 2}]


def find_posts(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id: int):
    for i, p in enumerate(my_posts) :
        if p['id'] == id :
            return i


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return{"message" : "Hello World"}