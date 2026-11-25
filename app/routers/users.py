from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.user import UserResponse,UserCreate,UserUpdate
from app.crud.user import get_user,get_users,create_user,update_user,delete_user
from app.models.user import User
from app.core.dependencies import get_admin_user,get_current_user
from typing import Literal


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/{user_id}", response_model=UserResponse)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if (
        current_user.id != user_id
        and current_user.role not in ("admin", "super_admin")
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own account",
        )
    user = get_user(user_id, db)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found!",
        )
    return user

@router.get("/", response_model=list[UserResponse])
def read_users(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    role: Literal["user", "admin", "super_admin"] | None = None,
    search: str | None = Query(default=None, min_length=1, max_length=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user),
):
    return get_users(
        db=db,
        skip=skip,
        limit=limit,
        role=role,
        search=search,
    )

@router.post("/",response_model=UserResponse)
def create_new_user(user:UserCreate,db:Session=Depends(get_db)):
    return create_user(user,db)

@router.patch("/{user_id}",response_model=UserResponse)
def update_exisiting_user(user:UserUpdate,user_id:int,db:Session=Depends(get_db),current_user: User = Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own account"
        )
    updated_user= update_user(user,user_id,db)
    if updated_user is None:
        raise HTTPException(status_code=404,detail="User not found!")
    return updated_user

@router.delete("/{user_id}")
def delete_exisiting_user(user_id:int,db:Session=Depends(get_db),current_user: User = Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own account"
        )
    deleted_user=delete_user(user_id,db)
    if deleted_user is None:
        raise HTTPException(status_code=404,detail="User not found!")
    return {"Message":"User Deleted Successfully!"}

