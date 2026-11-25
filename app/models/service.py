from sqlalchemy import Float, Column, String, Integer
from app.database.database import Base

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    image_path = Column(String, nullable=True)