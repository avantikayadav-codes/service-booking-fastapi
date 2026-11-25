from fastapi import FastAPI
from app.routers.users import router as user_router
from app.routers.services import router as service_router
from app.routers.bookings import router as booking_router
from app.routers.auth import router as auth_router
from app.routers.admin_management import router as admin_management_router
import logging
from app.core.middleware import request_logging_middleware
from fastapi.middleware.cors import CORSMiddleware
from app.routers.async_demo import router as async_router




app=FastAPI()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

app.middleware("http")(request_logging_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




app.include_router(auth_router)
app.include_router(user_router)
app.include_router(service_router)
app.include_router(booking_router)
app.include_router(admin_management_router)
app.include_router(async_router)



@app.get("/")
def get_data():
    return {"message":"Project is started! please add /docs for main menu"}










































# from app.database.database import engine, Base
# from app.models.user import User
# from app.models.service import Service
# from app.models.booking import Booking
# Base.metadata.create_all(bind=engine)
# Base.metadata.create_all(bind=engine)
# Base.metadata.create_all(bind=engine)













































# @app.get("/test")
# def test_data(db:Session = Depends(get_db)):
#     return {"message":"Database Session Received"}

# @app.post("/user/test")
# def test_create_user(user:UserCreate, db:Session = Depends(get_db)):
#     return create_user(db,user)

# @app.get("/user/test")
# def test_get_user(user_id:int, db:Session = Depends(get_db)):
#     return get_user(db,user_id)

# @app.patch("/user/test/patch/{user_id}",response_model=UserResponse)
# def test_update_user(
#         user_id:int,
#         user:UserUpdate,
#         db:Session = Depends(get_db)
# ):
#     return update_user(db,user_id,user)

# @app.delete("/user/test/delete/{user_id}",response_model=UserResponse)
# def test_delete_user(
#         user_id:int,
#         db:Session = Depends(get_db)
# ):
#     return delete_user(db,user_id)