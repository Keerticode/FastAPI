from fastapi import FastAPI, Response, status, HTTPException, Depends
from . import models, schemas, utils
from sqlalchemy.orm import Session
from .database import engine, get_db
from main import app

@app.post("/users", status_code = status.HTTP_201_CREATED, response_model = schemas.UserOut)
async def create_user(user : schemas.UserCreate, db : Session = Depends(get_db)) :

    #hashed password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get("/users/{id}", response_model = schemas.UserOut)
def get_user(id : int, db : Session = Depends(get_db)) :
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user :
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"User with id : {id} does not exist")

    return user