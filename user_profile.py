from fastapi import APIRouter,Depends
from database import get_db
from models import UserRegistration
from schemas import userRegistration
from sqlalchemy.orm import session

router = APIRouter(prefix="/profile",tags=["profile"])

@router.get("/get_profile")
def profile( db:session = Depends(get_db)):
    user_profile = db.query(UserRegistration).all()
    return user_profile

@router.get("/get_profile/{email}")
def getprofile(email:str, db:session= Depends(get_db)):
    user_profile = db.query(UserRegistration).filter(UserRegistration.email == email).first()
    
    return user_profile
