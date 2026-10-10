from fastapi import FastAPI,Response,status,HTTPException, Depends
from fastapi.params import Body
from typing import Optional, List
from .database import engine
from .routes import post, user, auth
models.Base.metadata.create_all(bind = engine)

app = FastAPI()

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