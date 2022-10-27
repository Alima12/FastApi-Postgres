from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from typing import List, Optional
from app import models
from app.db import get_db
from sqlalchemy.orm import Session
from app.schemas import CreatePost, PostVote, ReadPost
from app.oauth2 import get_current_user
from sqlalchemy import func


router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/", response_model=ReadPost)
def create_post(payload: CreatePost = Body(...), db: Session = Depends(get_db), user: int = Depends(get_current_user)):
    post = models.PostModel(**payload.dict(), owner=user)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


# @router.get("/", response_model=List[ReadPost])
@router.get("/", response_model=List[PostVote])
def get_posts(
    response: Response,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = ""
):
    # records = db.query(models.PostModel).filter(models.PostModel.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.PostModel, func.count(models.Vote.post).label("likes")).filter(models.PostModel.title.contains(search))\
    .join(models.Vote, models.Vote.post==models.PostModel.id, isouter=True)\
    .group_by(models.PostModel.id).limit(limit).offset(skip).all()
    response.status_code = 200
    return results


@router.get("/{id}/", response_model=PostVote)
def get_post(id:int, response:Response, db:Session=Depends(get_db)):
    record = db.query(models.PostModel).filter(models.PostModel.id==id).first()
    record = db.query(models.PostModel, func.count(models.Vote.post).label("likes")).filter(models.PostModel.id==id)\
    .join(models.Vote, models.Vote.post==models.PostModel.id, isouter=True)\
    .group_by(models.PostModel.id).first()
    if record:
        response.status_code = 200
        # record.likes = db.query(models.Vote).filter(models.Vote.post==id).count()
        return record

    raise HTTPException(404, "Post Not Found!")




@router.put("/{id}/", response_model=ReadPost)
def update_posts(id:int, response:Response, data:CreatePost=Body(...), db:Session=Depends(get_db)):
    post = db.query(models.PostModel).filter(models.PostModel.id==id)
    if post.first():
        post.update(data.dict(),synchronize_session=False)
        db.commit()
        db.refresh(post.first())
        response.status_code = status.HTTP_202_ACCEPTED
        return post.first()

    response.status_code = status.HTTP_404_NOT_FOUND
    return {"msg": "ID not found"}




@router.delete("/{id}/")
def delete_posts(id:int, response:Response, db:Session=Depends(get_db)):
    post = db.query(models.PostModel).filter(models.PostModel.id==id)
    if post.first() != None:
        post.delete(synchronize_session=False)
        db.commit()
        return HTTPException(204)

    response.status_code = status.HTTP_404_NOT_FOUND
    return {"msg": "post Not Found"}

