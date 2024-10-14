from fastapi import APIRouter,status,HTTPException,Depends
from .. import schemas,models
from ..database import db_dependency
from ..OAuth2 import get_current_user

router=APIRouter(
    prefix="/votes",tags=['vote']
)

@router.post("/",status_code=status.HTTP_201_CREATED)
async def vote(vote:schemas.Vote,db:db_dependency,current_user =Depends(get_current_user)):
    post=db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {vote.post_id} is not found")
    vote_query=db.query(models.Vote).filter(models.Vote.post_id==vote.post_id,models.Vote.user_id==current_user.id)
    found_vote=vote_query.first()
    if vote.dir==1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"User {current_user.id} has already voted on post {vote.post_id}")
        new_vote=models.Vote(post_id=vote.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"Successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="vote not found")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"Successfully deleted vote"}
        