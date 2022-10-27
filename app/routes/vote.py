from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from typing import List
from app import models
from app.db import get_db
from sqlalchemy.orm import Session
from app.schemas import  Vote
from app.oauth2 import get_current_user



router = APIRouter(prefix="/vote", tags=["Voting"])



@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote:Vote ,db:Session=Depends(get_db), user:int=Depends(get_current_user)):
    print(vote.dict(skip_defaults=True))
    vote_query = db.query(models.Vote).filter(models.Vote.post == vote.post, models.Vote.user == user.id)
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(409, "You Liked this Post before")

        if found_post:= db.query(models.PostModel).filter(models.PostModel.id== vote.post).first():
            new_vote = models.Vote(post=found_post.id, user=user.id)
            db.add(new_vote)
            db.commit()
        else:
            raise HTTPException(404, "Post Not Found!")

        return {"msg": "Successfully"}
    else:
        if not found_vote:
            raise HTTPException(404, "You never liked this post")

        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"msg": "like removed"}

