from fastapi import FastAPI
import uvicorn
from . import models
from .db import engine
from .routes import users, posts, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)
app.include_router(vote.router)

origins = [
    "http://localhost",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["home"])
async def home():
    return {
        "message": "hello world!"
    }


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
