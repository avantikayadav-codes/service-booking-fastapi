from sqlalchemy.orm import Session
from fastapi import Depends,APIRouter,HTTPException
from app.database.database import get_db
from app.schemas.user import UserLogin,UserResponse
from app.crud.user import user_authentication
from app.core.security import create_access_token
from app.core.dependencies import get_current_user
from fastapi.security import OAuth2PasswordRequestForm



router=APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/login")
def logic(user:UserLogin,db:Session=Depends(get_db)):
    authenticate_user=user_authentication(db,user.password,user.email)
    if authenticate_user is None:
        raise HTTPException(status_code=401,detail="Invalid Email or password!!")
    access_token=create_access_token(
        {
            "sub":str(authenticate_user.id)
        }
    )
    return {
        "access_token":access_token,
        "token_type":"bearer"
    }



@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user=Depends(get_current_user)):
    return current_user



@router.post("/token")
def login_for_swagger(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    authenticated_user = user_authentication(
        db,
        form_data.password,
        form_data.username
    )
    if authenticated_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    access_token = create_access_token(
        {"sub": str(authenticated_user.id)}
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }



