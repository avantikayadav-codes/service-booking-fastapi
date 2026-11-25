from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.user import User
from app.schemas.user import UserCreate,UserUpdate
from app.core.security import password_hash,password_verify


def create_user(user:UserCreate,db:Session):
    hashed_password=password_hash(user.password)
    new_user=User(
        name=user.name,
        email=user.email,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user(user_id:int,db:Session):
    return db.query(User).filter(User.id==user_id).first()


def get_users(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    role: str | None = None,
    search: str | None = None,
):
    query = db.query(User)

    if role is not None:
        query = query.filter(User.role == role)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                User.name.ilike(search_term),
                User.email.ilike(search_term),
            )
        )

    return (
        query.order_by(User.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_user(user:UserUpdate,user_id:int,db:Session):
    existing_user= db.query(User).filter(User.id==user_id).first()
    if existing_user is None:
        return None
    if user.name is not None:
        existing_user.name=user.name
    if user.email is not None:
        existing_user.email = user.email
    if user.password is not None:
        existing_user.password = password_hash(user.password)
    db.commit()
    db.refresh(existing_user)
    return existing_user

def delete_user(user_id:int,db:Session):
    exisiting_user=db.query(User).filter(user_id==User.id).first()
    if exisiting_user is None:
        return None
    db.delete(exisiting_user)
    db.commit()
    return exisiting_user

def get_user_by_email(user_email:str,db:Session):
    return db.query(User).filter(user_email==User.email).first()

def user_authentication(db:Session,password:str,email:str):
    user=get_user_by_email(email,db)
    if user is None:
        return None
    if not password_verify(password,user.password):
        return None
    return user