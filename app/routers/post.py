from typing import List,Optional
from fastapi import APIRouter,status,HTTPException,Depends
from ..schemas import Postdata_validator,Postdata_response,PostVote
from ..database import db_dependency
from .. import models
from ..OAuth2 import get_current_user
from sqlalchemy import func

router=APIRouter(
    prefix='/posts',
    tags=['posts']
)

@router.get("/",response_model=List[Postdata_response])
async def get_all(db:db_dependency,user=Depends(get_current_user)):
    posts=db.query(models.Post).all()
    return posts

@router.get("/getallvithvote",response_model=List[PostVote])
async def get_post_vote(db:db_dependency):
    posts_with_votes = db.query(
        models.Post,
        func.count(models.Vote.post_id).label("vote")
    ).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
    ).group_by(models.Post.id).all()

    # Transform the query results into a list of dictionaries
    result = [{"post": post, "vote": vote} for post, vote in posts_with_votes]
    return result

@router.get("/getusinguserid",response_model=List[Postdata_response])#response modes does not work for multiple return values so we use list to iterate it
async def root(db:db_dependency,user =Depends(get_current_user),limit:int=10,skip:int=0,search: Optional[str]=""):
    posts=db.query(models.Post).filter(user.id==models.Post.owner_id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() #It will create post class obj
    return posts
    

@router.get("/{id}",response_model=Postdata_response)
async def get_post(id:int,db:db_dependency,user : int =Depends(get_current_user)):
    print(user.email)
    post=db.query(models.Post).filter(id==models.Post.id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Id not found")
    return post


@router.post("/createpost",status_code=status.HTTP_201_CREATED)
async def create_post(new_post:Postdata_validator,db:db_dependency,user  =Depends(get_current_user)):
    post_model=models.Post(owner_id=user.id,**new_post.model_dump())
    db.add(post_model)
    db.commit()
    db.refresh(post_model)
    return {"Created": post_model}

    
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def dele  (id:int,db:db_dependency,user  =Depends(get_current_user)):
    deleted_post_query=db.query(models.Post).filter(id==models.Post.id)
    deleted_post=deleted_post_query.first()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Id not found")
    if user.id != deleted_post.first().owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform this action")
    deleted_post_query.delete(synchronize_session=False)
    db.commit()

@router.put("/{id}",status_code=status.HTTP_200_OK)
async def upd(post:Postdata_validator,id:int,db:db_dependency,user =Depends(get_current_user)):
    updated=db.query(models.Post).filter(id==models.Post.id)
    if updated.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Id not found")
    if user.id != updated.first().owner_id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform this action")
    updated.update(post.model_dump(),synchronize_session=False)
    db.commit()
    return updated.first()