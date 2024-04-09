from src.user.schemas import UserBase, UserCreate
from src.user import models 
from sqlalchemy.orm import Session 
from src.utils import hash_password

async def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

async def create_account(db: Session, info: UserCreate):
    hashed_password = hash_password(info.password)
    db_user = models.User(username=info.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user 
