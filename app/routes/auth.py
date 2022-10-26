from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas,models,utils,oauth

router = APIRouter(tags = ['Authentication'])

@router.post('/login',response_model=schemas.Token)
def login(data : schemas.UserLogin,db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == data.email).first()
    if not user :
        raise HTTPException(status.HTTP_403_FORBIDDEN,f'Invalid Credentials')
    if not utils.verify(data.password, user.password):
        raise HTTPException(status.HTTP_403_FORBIDDEN,f'Invalid Password or UserName')
    
    access_token = oauth.get_access_token(data = {'user_id':user.id})

    return {'access_token': access_token , 'token_type':'bearer'}