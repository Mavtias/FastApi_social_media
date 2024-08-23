from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix = "/vote",
    tags = ['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def vote(vote: schemas.Vote, 
               db: Session = Depends(database.get_db), 
               get_current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Vote).filter(models.Post.id == vote.post_id). first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Post with {id} not found")
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == get_current_user.id)
    found_vote = vote_query.first()
    
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {get_current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id = get_current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully removed vote"}

"""

para ver los upvotes y downvotes de un post en particular


@router.post("/", status_code=status.HTTP_201_CREATED)
async def vote(
    vote: schemas.Vote, 
    db: Session = Depends(database.get_db), 
    get_current_user: int = Depends(oauth2.get_current_user)
):
    # Verifica si ya existe un voto para el usuario y el post
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, 
        models.Vote.user_id == get_current_user.id
    )
    found_vote = vote_query.first()

    # Accede al post para actualizar los conteos
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    if vote.vote_value == 1:
        if found_vote:
            if found_vote.vote_value == 1:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User has already upvoted this post")
            elif found_vote.vote_value == -1:
                post.downvotes -= 1
                post.upvotes += 1
                found_vote.vote_value = 1
        else:
            new_vote = models.Vote(post_id=vote.post_id, user_id=get_current_user.id, vote_value=1)
            db.add(new_vote)
            post.upvotes += 1

    elif vote.vote_value == -1:
        if found_vote:
            if found_vote.vote_value == -1:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User has already downvoted this post")
            elif found_vote.vote_value == 1:
                post.upvotes -= 1
                post.downvotes += 1
                found_vote.vote_value = -1
        else:
            new_vote = models.Vote(post_id=vote.post_id, user_id=get_current_user.id, vote_value=-1)
            db.add(new_vote)
            post.downvotes += 1

    elif vote.vote_value == 0:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        if found_vote.vote_value == 1:
            post.upvotes -= 1
        elif found_vote.vote_value == -1:
            post.downvotes -= 1
        vote_query.delete(synchronize_session=False)

    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid vote value")

    db.commit()
    return {"message": "Vote processed successfully"}


"""





    
