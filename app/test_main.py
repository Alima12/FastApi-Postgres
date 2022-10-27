from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from .config import settings
from . import main, schemas, models
import random as rn
from app.db import get_db
import pytest



SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}_test'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Testingsession = sessionmaker(autocommit=False, autoflush=False, bind=engine)




@pytest.fixture(scope="session")
def session():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db =  Testingsession()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    main.app.dependency_overrides[get_db] = override_get_db
    yield TestClient(main.app)






def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "hello world!"}



def test_create_user(client):
    data = {
        "email": f"ali@yahoo.com",
        "username": "alim",
        "password": "123456"
    }
    res = client.post("/users/", json=data)
    user = schemas.ReadUser(**res.json())

    assert user.email == data["email"]
    assert user.username == data["username"]
    assert res.status_code == 201
    


def test_login_user(client):
    data = {
        "username": "alim",
        "password": "123456"
    }
    response = client.post("/login", data=data)
    assert response.status_code == 200

    response = response.json()
    assert response["access_token"]
    assert response["token_type"] == "Bearer"

