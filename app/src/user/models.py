from sqlalchemy import Column, String 
from src.database import Base 

class User(Base):
    __tablename__ = "user_record"
    username = Column(String(255), primary_key=True)
    hashed_password = Column(String(255), nullable=False)