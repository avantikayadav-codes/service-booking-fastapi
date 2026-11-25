
from sqlalchemy.orm import Session
from app.models.user import User


def make_user_admin(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        return None

    if user.role == "super_admin":
        return "already_super_admin"

    if user.role == "admin":
        return "already_admin"

    user.role = "admin"

    db.commit()
    db.refresh(user)

    return user
