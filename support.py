from fastapi import APIRouter, Depends
from database import get_db
from sqlalchemy.orm import Session
from models import Support
from schemas import userSupport

router = APIRouter();

@router.post("/add_support",tags =["support"])
def support(sp:userSupport, db: Session = Depends(get_db)):
    new_support = Support(
        full_name = sp.full_name,
        mobile_number = sp.mobile_number,
        email = sp.email,
        Description = sp.Description   
    )
    
    db.add(new_support)
    db.commit()
    db.refresh(new_support)
    
    return {
        "full_name" : sp.full_name,
        "mobile_number" : sp.mobile_number,
        "email" : sp.email,
        "description": sp.Description,
        "message" : "We will get back to you soon"
        
    }

@router.get("/get_support", tags = ['support'])
def getSupport(db:Session= Depends(get_db)):
    return db.query(Support).all()