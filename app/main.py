
from distutils.log import error
from pydoc import ModuleScanner
from random import randrange
from typing import Optional
from fastapi import FastAPI, Response,status, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app= FastAPI()


class Post (BaseModel):
    title : str 
    content : str
    published : bool = True

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



@app.get("/")
def root():
    return {'message': 'Hello World to API'}  

@app.get('/ad')
def test(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {'data':posts}


@app.get('/posts')
def get_posts(db : Session = Depends(get_db)):
    # cursor.execute('Select * from posts')
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {'data': posts}

@app.post('/posts',status_code= status.HTTP_201_CREATED)
def create_post(data: Post, db: Session = Depends(get_db)):
    # To convert the model to Dictionary : data.dict()
    #post_dict = data.dict()
    #post_dict['id'] = randrange(0,1000000)
    #raw.append(post_dict)
    # cursor.execute("""insert into posts(title , content, published) 
    # values (%s,%s,%s) returning * """,(data.title,data.content,data.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(**data.dict())
    db.add(new_post)
    db.commit()
    # return the newly added post and store it in new_post
    db.refresh(new_post)
    return {'message': new_post}

@app.get('/posts/{id}')
def get_post(id : int ,db:Session = Depends(get_db)):

    #post = find_post(id)
    # cursor.execute("select * from posts where id = %s",(str(id)))
    # post = cursor.fetchall()
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,f"post with id:{id} was not found")
    return {'Post': post}

@app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:Session = Depends(get_db)):
    #data = find_post(id,index= True)
    #raw.pop(data[0])
    # cursor.execute("delete from posts where id = %s returning *",(str(id),))
    # post = cursor.fetchall()
    #conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,f"post with id:{id} was not found")
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int, data:Post, db:Session = Depends(get_db)):
    # new_data=data.dict()
    # old_data = find_post(id,index=True)
    #new_data['id'] = id
    #raw[old_data[0]]= new_data

    # cursor.execute('update posts set title = %s , content = %s, published = %s where id = %s returning *',
    # (data.title,data.content,data.published,str(id)))
    # updated_post = cursor.fetchone()
    #conn.commit()
    old_post = db.query(models.Post).filter(models.Post.id == id)
    if old_post .first()== None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,f"post with id:{id} was not found")
    
    old_post.update(data.dict(), synchronize_session= False)
    db.commit()
    return {'Updated_Data': old_post.first()}

