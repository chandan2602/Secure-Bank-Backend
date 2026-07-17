from fastapi import FastAPI, Depends
from database import get_db, engine
import models
from pydantic import BaseModel,EmailStr
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
from jose import jwt
from datetime import datetime,timedelta

load_dotenv()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*'],
)
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
TOKEN_TIMEOUT = os.getenv("TOKEN_TIMEOUT")

# jwt token creation
def create_access_token(data:dict):             # the data need to pass in dictionary format (because in our database we have data like user name , password many thing which need to be pass dictionary wise)
    to_encode = data.copy()              
    # we need to copy the user data so by mistakly we should not delte the user data
    expairy_time = datetime.utcnow() + timedelta(minutes = TOKEN_TIMEOUT)
    to_encode.update({'exp' : expairy_time})
    encode_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm =ALGORITHM )
    print("jwt token : " + encode_jwt)
    return encode_jwt
    

class userRegistration(BaseModel):
    full_name : str
    mobile_number :str
    email : EmailStr                # it will take only email
    user_name : str
    user_password : str
    
class login(BaseModel):
    username: str
    password : str
 
#passowrd hashing    
password_context = CryptContext(schemes=["argon2"],deprecated = "auto")

#for hashing password this function used
def hash_password(password:str)-> str :
    return password_context.hash(password)
    
    
#for varify password
def varify_password(normal_password:str, hashed_password:str) -> bool:
    return password_context.varify(normal_password,hashed_password)

@app.post("/user_registration")
def user_registration(obj : userRegistration, db:Session = Depends(get_db)):
    new_user = models.user_registration(
        full_name = obj.full_name,
        mobile_number = obj.mobile_number,
        email = obj.email,
        user_name = obj.user_name,
        user_password = obj.user_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    
@app.get("/get_users")
def get_users(db:Session = Depends(get_db) ):
    get_user = db.query(models.user_registration).all()
    return get_user

# @app.post("/login")
# def user_login(user:login, db:Session = Depends(get_db)):
    
    