
from distutils.log import error
from pydoc import ModuleScanner
from random import randrange
from typing import Optional
from fastapi import FastAPI, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models 
from .database import engine, get_db
from .routes import post,user
from sqlalchemy.orm import Session



models.Base.metadata.create_all(bind=engine)

app= FastAPI()




while(True):
    try:
        conn = psycopg2.connect(host='localhost',database='FastApi',user='postgres',password ='akash', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection was successfull')
        break
    except Exception as error:
        print('Connecting to database failed', error)
        time.sleep(2)

raw =[{'id': 1,'title': "demo Title1","content":"Demo Content 1","published": False},{'id': 2,'title': "demo Title 2","content":"Demo Content 2","rating": 4}]

def find_post(id,index= False):
    for i,p in enumerate(raw):
        if p['id'] == id:
            if index == True:
                return (i,p)
            else: 
                return p

app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def root():
    default_str = "hello world"
    return default_str

@app.get('/ad')
def test(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {'data':posts}