from schemas import userRegistration, userLogin 
from models import UserRegistration
from database import get_db
from fastapi import Depends,APIRouter, HTTPException, status
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from jose import jwt,JWTError
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer


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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
def get_currentuser(
    token :str =  Depends(oauth2_scheme),
    db: Session = Depends(get_db)):
    
    credential_exception  = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail = "user not found", 
        headers= {"www-Authenticate" : "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        email:str = payload.get("sub")
        
        if email is None:
            raise credential_exception
    except JWTError :
        raise credential_exception
        
    user = db.query(UserRegistration).filter(UserRegistration.email == email).first()
    
    if user is None:
        raise credential_exception
    
    return user
        

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
def get_users(
    current_user: UserRegistration = Depends(get_currentuser)):
    
    # get_user = db.query(UserRegistration).all()
    return {
        "message" : f"Welcome {current_user.full_name}"
    }
