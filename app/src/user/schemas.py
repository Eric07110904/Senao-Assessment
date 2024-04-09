from pydantic import BaseModel, Field
from typing import Optional

class ResponseBase(BaseModel):
    success: bool 
    reason: Optional[str] = None 
    
class UserBase(BaseModel):
    username: str = Field(..., alias="username", min_length=3, max_length=32)
    class Config:
        orm_mode = True 

class UserCreate(UserBase):
    password: str = Field(..., alias="password")
    # @field_validator("password")
    # @classmethod
    # def check_pwd(cls, v: str) -> str: 
    #     str_size = len(v)
    #     if str_size < 8:
    #         raise HTTPException(status_code=422, detail={"success":False, "reason":"Password is too short!"})
    #     elif str_size > 32:
    #         raise ValueError("password is too long!")