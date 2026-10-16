from fastapi import FastAPI
from .database import engine
from . import models
from .routes import post, user, auth, votes
from .config import settings

print(settings.database_username)

models.Base.metadata.create_all(bind = engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get("/")
async def root():
    return{"message" : "Hello World"}