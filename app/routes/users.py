
from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from typing import List
from app import models
from app.db import get_db
from sqlalchemy.orm import Session
from app.schemas import  CreateUser, ReadUser, ReadUserPosts
from app import utils
from app.oauth2 import get_current_user
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ReadUser)
def create_user(user: CreateUser = Body(...), db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    try:
        new_user = models.UserModel(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    except UniqueViolation:
        raise HTTPException(409, "Username or Email already Exists")
    except IntegrityError as e:
        raise HTTPException(409, "\n".join([error for error in e.args]))

    return new_user


@router.get("/{id}", response_model=ReadUserPosts)
def get_user(id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    if not current_user.is_admin and current_user.id != id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "You Don't have Permission")
    
    user = db.query(models.UserModel).filter(models.UserModel.id == id).first()

    if user:
        return user
    
    raise HTTPException(404, "User not found")


@router.get("/", response_model=List[ReadUserPosts])
def get_user(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "You Don't have Permission")
    users = db.query(models.UserModel).all()
    return users
