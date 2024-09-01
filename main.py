from fastapi import FastAPI

import posts
import models
import database

from typing import List
from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
import models
import schemas
from fastapi import APIRouter
from database import get_db


app = FastAPI()

app.include_router(posts.router)

models.Base.metadata.create_all(bind=database.engine)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get('/db', response_model=List[schemas.CreatePost])
def test_posts(db: Session = Depends(get_db)):
    post = db.query(models.Post).all()

    return post

@app.post('/db', status_code=status.HTTP_201_CREATED, response_model=List[schemas.CreatePost])
def create_posts(post_create: schemas.CreatePost, db: Session = Depends(get_db)):
    new_post = models.Post(**post_create.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return [new_post]