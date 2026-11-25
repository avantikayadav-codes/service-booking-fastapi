from sqlalchemy import Column,String,Integer,DateTime,ForeignKey
from app.database.database import Base

class Booking(Base):
    __tablename__="bookings"

    id=Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    service_id=Column(Integer,ForeignKey("services.id"),nullable=False)
    booking_date=Column(DateTime,nullable=False)
    status=Column(String,nullable=False,default="Pending")
