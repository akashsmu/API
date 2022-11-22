from .. import models , schemas ,oauth
from fastapi import Response,status,APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional



router = APIRouter(prefix = '/posts', tags = ['Posts'])




@router.get('/',response_model = List[schemas.PostResponse])
def get_posts(db : Session = Depends(get_db),user
 :int = Depends(oauth.get_current_user),limit :int = 10,skip:int = 0, search : Optional[str] = ''):
    # cursor.execute('Select * from posts')
    # posts = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.post('/',status_code= status.HTTP_201_CREATED,response_model = schemas.PostResponse)
def create_post(data: schemas.PostCreate, db: Session = Depends(get_db), user :int = Depends(oauth.get_current_user)):
    # To convert the model to Dictionary : data.dict()
    #post_dict = data.dict()
    #post_dict['id'] = randrange(0,1000000)
    #raw.routerend(post_dict)
    # cursor.execute("""insert into posts(title , content, published) 
    # values (%s,%s,%s) returning * """,(data.title,data.content,data.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    
    new_post = models.Post(**data.dict(),user_id = user.id)
    db.add(new_post)
    db.commit()
    # return the newly added post and store it in new_post
    db.refresh(new_post)
    return new_post

@router.get('/{id}',response_model = schemas.PostResponse)
def get_post(id : int ,db:Session = Depends(get_db),user:int = Depends(oauth.get_current_user)):

    #post = find_post(id)
    # cursor.execute("select * from posts where id = %s",(str(id)))
    # post = cursor.fetchall()
    post = db.query(models.Post).filter(models.Post.id == id).first()

    # To retrieve posts of only a logged in user
    # post =db.query(models.Post).filter(models.Post.user_id == user.id).all()

    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,f"post with id:{id} was not found")
    return post


@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:Session = Depends(get_db),user
 :int = Depends(oauth.get_current_user)):
    #data = find_post(id,index= True)
    #raw.pop(data[0])
    # cursor.execute("delete from posts where id = %s returning *",(str(id),))
    # post = cursor.fetchall()
    #conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,f"post with id:{id} was not found")
    if post.first().user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail =f'Not authorized to perform requested action')
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model = schemas.PostResponse)
def update_post(id:int, data:schemas.PostCreate, db:Session = Depends(get_db),user
 :int = Depends(oauth.get_current_user)):
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
    if old_post.first().user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail =f'Not authorized to perform requested action')
    
    old_post.update(data.dict(), synchronize_session= False)
    db.commit()
    return old_post.first()