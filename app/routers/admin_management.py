
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.core.dependencies import get_super_admin_user
from app.crud.admin_management import make_user_admin as promote_user
from app.schemas.user import SuperUserResponse

router = APIRouter(
    prefix="/admin-management",
    tags=["Admin Management"]
)


@router.patch("/users/{user_id}/make-admin",response_model=SuperUserResponse)
def make_user_admin(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_super_admin_user)
    ):
    result = promote_user(user_id, db)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if result == "already_super_admin":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a Super Admin"
        )

    if result == "already_admin":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already an Admin"
        )

    return result