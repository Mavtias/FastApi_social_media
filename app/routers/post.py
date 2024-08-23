from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db
from typing import  List, Dict, Optional


router = APIRouter(
    prefix = "/posts",
    tags = ['Posts']
)

@router.get("/", response_model = List[schemas.PostOut])
async def get_posts(db: Session = Depends(get_db), 
                    get_current_user: int = Depends(oauth2.get_current_user), 
                    limit: int = 10,
                    skip: int = 0,
                    search: Optional[str] = ""):
    

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    #para obtener solo los posts de un usuario en particular
    #posts = db.query(models.Post).filter(models.Post.user_id == get_current_user.id).all()

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.Post)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(user_id=get_current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model = schemas.PostOut)
async def get_post(id: int, response: Response, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    #post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    #para obtener solo los posts de un usuario en particular, comentar lo siguiente si se quiere un tipo de rrss open for everyone
    # if post.user_id != get_current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
    #                         detail="Not authorized to perform requested action")
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} not found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    
    
    deleted_post_query = db.query(models.Post).filter(models.Post.id == id)

    deleted_post = deleted_post_query.first()
    
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"post with id {id} not found")
    
    if deleted_post.user_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform requested action")

    deleted_post_query.delete(synchronize_session = False)
    
    db.commit()
     
    return Response(status_code = status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model = schemas.Post)
async def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    old_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not old_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} not found")
    
    if old_post.user_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform requested action")
    
    old_post.title = post.title
    old_post.content = post.content
    old_post.published = post.published
    
    db.commit()
    db.refresh(old_post)

    return old_post