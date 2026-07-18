from schemas import userRegistration, userLogin 
from models import UserRegistration
from database import get_db
from fastapi import Depends,APIRouter, HTTPException, status
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from jose import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
TOKEN_EXPAIRY_TIME = int(os.getenv("TOKEN_EXPAIRY_TIME",30))

def create_jwt_token(data:dict):
    token_data = data.copy()
    token_time = datetime.now(timezone.utc) + timedelta(minutes = TOKEN_EXPAIRY_TIME)
    token_data.update({"exp": token_time})
    generate_jwt_token = jwt.encode(token_data,SECRET_KEY, algorithm =  ALGORITHM)
    return generate_jwt_token


password_context = CryptContext(schemes=["argon2"],deprecated = "auto")

# hash password
def hash_password(password:str)-> str :
    return password_context.hash(password)
    
# varify passowrd
def verify_passowrd(normal_password : str, hashed_passowrd : str) -> bool:
    return password_context.verify(normal_password,hashed_passowrd)
        

@router.post("/user_registration")
def user_registration(obj : userRegistration, db:Session = Depends(get_db)):
    
    # check the user exits or not in our db
    existing_user = db.query(UserRegistration).filter(UserRegistration.email ==  obj.email).first()
    
    if existing_user:
        raise HTTPException(status_code= 400 , detail= "email already exist")
    
    hash_pass = hash_password(obj.user_password)
    
    new_user = UserRegistration(
        full_name = obj.full_name,
        mobile_number = obj.mobile_number,
        email = obj.email,
        user_name = obj.user_name,
        user_password = hash_pass
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return "user created successfully"


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    # user exist or not
    user = db.query(UserRegistration).filter(UserRegistration.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Invalid User")
    
    if not verify_passowrd(form_data.password , user.user_password):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Invalid Password")
    
    token_data = {'sub' : user.email }
    token = create_jwt_token(token_data)
    return {"access_token" : token, "token_type" : "bearer"}
    

@router.get("/get_users")
def get_users(db:Session = Depends(get_db) ):
    get_user = db.query(UserRegistration).all()
    return get_user
