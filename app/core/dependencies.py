from fastapi.security import OAuth2PasswordBearer

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/auth/token")

from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
import jwt
from app.core.config import settings
from app.database.database import get_db
from app.models.user import User



def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    try:
        payload=jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=settings.ALGORITHM
        )
        user_id=payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Token")
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    user=db.query(User).filter(User.id==int(user_id)).first()
    if user is None:
            raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User not found"
    )
    return user




def get_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.role not in ("admin", "super_admin"):
          raise HTTPException( status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required")
    return current_user


def get_super_admin_user(current_user:User=Depends(get_current_user)):
    if current_user.role!="super_admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
            detail="Super Admin access required")
    return current_user