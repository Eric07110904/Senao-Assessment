from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from src.user.schemas import UserBase, UserCreate, ResponseBase 
from src.utils import valid_pwd, valid_useranme, verify
from src.database import get_db
from src.user import service as user_service 
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import redis 

app = FastAPI()
redis_client = redis.StrictRedis(host='redis', port=6379)
'''
Redis storage 
{
    ip_failed_times: 0, # failed verified times
    ip_block_time:, # block time 
}
'''
@app.middleware("http")
async def limit_middleware(request, call_next): 
    if request.url.path == '/verify':
        client_ip = request.client.host
        failed_times = redis_client.get("%s_failed_times"%(client_ip))
        block_time = redis_client.get("%s_block_time"%(client_ip))
        block_time = None if block_time == None else block_time.decode('utf-8')
        failed_times = 0 if failed_times == None else int(failed_times)
        if block_time!=None:
            if datetime.now().isoformat() <= block_time:
                print("blocking")
                return JSONResponse(status_code=429, content={"success":False, "reason":"Too many failed request, try again later!"})
            else: 
                redis_client.delete("%s_block_time"%(client_ip))
                failed_times = 0
                redis_client.set("%s_failed_times"%(client_ip), failed_times)

        response = await call_next(request)
        if response.status_code != 200: 
            failed_times+=1 
            if failed_times >= 5:
                t = datetime.now() + timedelta(minutes=1)
                redis_client.set("%s_block_time"%(client_ip), t.isoformat())
            else: 
                redis_client.set("%s_failed_times"%(client_ip), failed_times)
    else:
        response = await call_next(request)
    return response 

@app.post("/users", response_model=ResponseBase)
async def create_account(info: UserCreate, db: Session = Depends(get_db)):
    # input validation 
    check_username = valid_useranme(info.username)
    check_pwd = valid_pwd(info.password)
    if check_username["success"] == False:
        return JSONResponse(status_code=422, content=check_username)
    if check_pwd["success"] == False:
        return JSONResponse(status_code=422, content=check_pwd)
    
    # user already exist?
    db_user = await user_service.get_user_by_username(db, info.username)
    if db_user: 
        return JSONResponse(status_code=400, content={"success":False, "reason":"User already exists!"})
    user = await user_service.create_account(db, info)
    return JSONResponse(status_code=200, content={"success":True})

@app.post("/verify", response_model=ResponseBase)
async def verify_account(info: UserCreate, db: Session = Depends(get_db)):
    db_user = await user_service.get_user_by_username(db, info.username)
    if not db_user or not verify(info.password, db_user.hashed_password):
        return JSONResponse(status_code=400, content={"success":False, "reason":"Invalid username or password!"})
    return JSONResponse(status_code=200, content={"success":True})