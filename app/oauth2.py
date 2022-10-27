from jose import JWSError, jwt
from datetime import datetime, timedelta
from fastapi import status, Depends, HTTPException
from app.schemas import TokenData, ReadUser
from fastapi.security import OAuth2PasswordBearer
from app.db import get_db
from sqlalchemy.orm import Session
from app import models
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#Secret Key
SECREK_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_HOURS = 24
REFRESH_TOKEN_EXPIRE_DAYS = 30


def make_session(data: dict, db:Session):
    user_id = data.get("user_id")
    session_id = data.get("session_id")
    # if token := db.query(models.Tokens).filter(models.Tokens.user == user_id).first():
    #     token.is_expired = True
    # else:
    token = models.Tokens(token=session_id, user=user_id)
    db.add(token)
    db.commit()
    db.refresh(token)


def create_access_token(data: dict):
    to_encode = data.copy()
    session_id = to_encode.get("session_id")
    expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({
        "expire_time": expire.timestamp(),
        "_id": session_id
    })
    encoded_jwt = jwt.encode(to_encode, SECREK_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, db: Session):
    to_encode = data.copy()
    session_id = to_encode.get("session_id")
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({
        "expire_time": expire.timestamp(),
        "_id": session_id
    })
    encoded_jwt = jwt.encode(to_encode, SECREK_KEY, algorithm=ALGORITHM)
    make_session(to_encode, db)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception, db:Session):
    try:

        payload = jwt.decode(token, SECREK_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        session: str = payload.get("_id")
        if id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        session_id = db.query(models.Tokens).filter(models.Tokens.user == id).first()
        if not session_id or session_id.is_expired:
            raise HTTPException(401, "Your Token Expired")

        token_data = TokenData(id=id)

        return token_data

    except JWSError as e:
        raise credentials_exception


def verify_refresh_token(token: str, credentials_exception, db:Session):
    try:

        payload = jwt.decode(token, SECREK_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        session: str = payload.get("_id")
        if id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        session_id = db.query(models.Tokens).filter(models.Tokens.user == id).first()
        if not session_id or session_id.is_expired:
            raise HTTPException(401, "Your Token Expired")

        token_data = TokenData(id=id)

        return token_data

    except JWSError as e:
        raise credentials_exception


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could Not Authorize",
        headers={"WWW-Authenticate": "Bearer"}
    )
    token = verify_refresh_token(token, credentials_exception, db=db)
    user = db.query(models.UserModel).filter(models.UserModel.id == token.id).first()
    return user

