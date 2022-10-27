from fastapi import APIRouter, Depends, status, HTTPException, Response, Body
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas import ReadUser, UserLogin, Token, RefreshToken
from app.models import UserModel
from sqlalchemy import or_
from app.utils import verify
from app.oauth2 import create_access_token, create_refresh_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from uuid import uuid4



router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == user_credentials.username).first()
    if not user:
        raise HTTPException(403, "Invalid Credentials")

    if verify(user_credentials.password, user.password):
        session_id = str(uuid4())
        #generate Token
        access_token = create_access_token(data={"user_id": user.id, "session_id": session_id})
        refresh_token = create_refresh_token(data={"user_id": user.id, "session_id": session_id}, db=db)

        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "Bearer"}

    raise HTTPException(403, "Username or Password is Wrong!")



# @router.post("/refresh", response_model=Token)
# def refresh(refresh_token:RefreshToken, db: Session = Depends(get_db)):
#
#     session_id = str(uuid4())
#     # generate Token
#     access_token = create_access_token(data={"user_id": user.id, "session_id": session_id})
#     refresh_token = create_refresh_token(data={"user_id": user.id, "session_id": session_id}, db=db)
#
#     return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "Bearer"}
#
#     raise HTTPException(403, "Username or Password is Wrong!")




