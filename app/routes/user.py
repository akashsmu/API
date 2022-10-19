from .. import models , schemas , utils
from fastapi import status,APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(prefix='/user',tags = ["Users"])

@router.post('/', status_code= status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def create_user(data: schemas.UserCreate  , db: Session = Depends(get_db)):
    #hash the password
    data.password = utils.hash(data.password)
    new_user = models.User(**data.dict())
    validate_user = db.query(models.User).filter(models.User.email == new_user.email).first()
    if validate_user != None:
        raise HTTPException(status.HTTP_412_PRECONDITION_FAILED,f"Enter a unique Email address")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}',response_model = schemas.UserResponse)
def get_user(id :int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND,f"user with id :{id} does not exist")
    return user