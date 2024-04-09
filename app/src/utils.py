import re 
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto") 

def hash_password(s: str) -> str:
    return pwd_context.hash(s) 
def verify(s: str, s_hashed: str) -> bool: 
    return pwd_context.verify(s, s_hashed)
def valid_pwd(password: str) -> dict:
    pwd_length = len(password)
    if pwd_length < 8:
        return {"success": False, "reason": "Password is too short!"}
    elif len(password) > 32: 
        return {"success": False, "reason": "Password is too long!"}
    elif not re.match("^(?=.*[A-Z])(?=.*[a-z])(?=.*\\d).*$", password):
        return {"success": False, "reason": "Password should contain at least 1 uppercase letter, 1 lowercase letter and 1 number!"}
    else:
        return {"success": True}

def valid_useranme(username: str) -> dict:
    username_length = len(username)
    if username_length < 3:
        return {"success": False, "reason": "Username is too short!"}
    elif username_length > 32:
        return {"success": False, "reason": "Username is too long!"}
    else:
        return {"success": True}