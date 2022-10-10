
from distutils.log import error
from random import randrange
from typing import Optional
from fastapi import FastAPI, Response,status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

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

@app.get('/posts')
def get_posts():
    cursor.execute('Select * from posts')
    posts = cursor.fetchall()
    return {'data': posts}

@app.post('/posts',status_code= status.HTTP_201_CREATED)
def create_post(data: Post):
    # To convert the model to Dictionary : data.dict()
    #post_dict = data.dict()
    #post_dict['id'] = randrange(0,1000000)
    cursor.execute("""insert into posts(title , content, published) 
    values (%s,%s,%s) returning * """,(data.title,data.content,data.published))
    
    #raw.append(post_dict)
    new_post = cursor.fetchone()
    conn.commit()
    return {'message': new_post}

@app.get('/posts/{id}')
def get_post(id : int):

    #post = find_post(id)
    cursor.execute("select * from posts where id = %s",(str(id)))
    post = cursor.fetchall()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,f"post with id:{id} was not found")
    return {'Post': post}

@app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    #data = find_post(id,index= True)
    cursor.execute("delete from posts where id = %s returning *",(str(id),))
    post = cursor.fetchall()
    if post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,f"post with id:{id} was not found")
    #raw.pop(data[0])
    conn.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int, data:Post):
    # new_data=data.dict()
    # old_data = find_post(id,index=True)
    cursor.execute('update posts set title = %s , content = %s, published = %s where id = %s returning *',
    (data.title,data.content,data.published,str(id)))
    updated_post = cursor.fetchone()
    if updated_post== None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,f"post with id:{id} was not found")
    #new_data['id'] = id
    #raw[old_data[0]]= new_data
    conn.commit()
    return {'Updated_Data': updated_post}

