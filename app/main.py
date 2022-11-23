from fastapi import FastAPI, Depends
from . import models 
from .database import engine, get_db
from sqlalchemy.orm import Session
from .config import Settings
from .routes import post,user,auth

models.Base.metadata.create_all(bind=engine)

app= FastAPI()





# raw =[{'id': 1,'title': "demo Title1","content":"Demo Content 1","published": False},{'id': 2,'title': "demo Title 2","content":"Demo Content 2","rating": 4}]

# def find_post(id,index= False):
#     for i,p in enumerate(raw):
#         if p['id'] == id:
#             if index == True:
#                 return (i,p)
#             else: 
#                 return p


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    default_str = "hello world"
    return default_str

@app.get('/ad')
def test(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {'data':posts}