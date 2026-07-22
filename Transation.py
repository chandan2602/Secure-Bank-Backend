from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import Transation
from schemas import userTransation
from database import get_db

router = APIRouter()

@router.post("/get_userTransation", tags=['Transations'])
def getUserTransation(transationobj : userTransation, db:Session = Depends(get_db)):
    
    new_transation = Transation(   
        full_name  = transationobj.full_name,
        mobile_number  =  transationobj.mobile_number,
        email = transationobj.email,
        amount = transationobj.amount,
        loan_date  = transationobj.loan_date
    )
    
    db.add(new_transation)
    db.commit()
    db.refresh(new_transation)
    
    return {
        "Name " : f"{transationobj.full_name}"
        "amount" f"{transationobj.amount}"
    }
    
    

@router.get("/get_userTransation" , tags=['Transations'])
def getUserTransation( db:Session = Depends(get_db)):
    
    all_transation = db.query(Transation).all()
    
    return all_transation