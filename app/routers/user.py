from fastapi import APIRouter,HTTPException
from starlette import status
from ..schemas import  User_create, User_out
from ..database import db_dependency
from .. import models
from ..utils import hash


router=APIRouter(
    prefix='/users',
    tags=['users']
)



@router.post("/createuser", status_code=status.HTTP_201_CREATED, response_model=User_out)
async def create_user(new_user: User_create, db: db_dependency):
    new_user.password=hash(new_user.password)
    user_model = models.User(**new_user.model_dump())
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return user_model  # Return the user model directly

@router.get("/{id}",status_code=status.HTTP_302_FOUND,response_model=User_out)
async def get_user_by_id(id:int,db:db_dependency):
    new_user=db.query(models.User).filter(id==models.User.id).first()
    if not new_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Id not found")
    return new_user