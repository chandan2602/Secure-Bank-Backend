from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text,func
from models import Transation,UserRegistration
from schemas import userTransation
from database import get_db
from Registration import get_currentuser
from datetime import date


router = APIRouter(prefix="/transation",tags=['Transations'])

@router.post("/add_newTransation")
def newTransation(obj:userTransation, db: Session = Depends(get_db), current_user : UserRegistration = Depends(get_currentuser)):
    
    add_new = Transation(
        full_name = obj.full_name,
        mobile_number = obj.mobile_number,
        email = obj.email,
        amount = obj.amount,
        loan_date = obj.loan_date,
        intrest_rate=obj.intrest_rate
    )
    
    db.add(add_new)
    db.commit()
    db.refresh(add_new)
    
    return add_new
    

@router.get("/get_userTransation" )
def getUserTransation( db:Session = Depends(get_db), current_user : UserRegistration = Depends(get_currentuser)):
    
    all_transation = db.query(Transation).all()
    all_transation_count = db.query(Transation).count()
    Total_amount = db.query(func.sum(Transation.amount)).scalar()
    Total_interest_amount = db.query(func.sum(Transation.total_amount)).scalar()
    Total_profit = (Total_interest_amount - Total_amount)

    return {
        "Transation_List": all_transation,
        "Total_transation_count" : all_transation_count,
        "Total_amount" : Total_amount,
        "Total_interest_amount" : Total_interest_amount,
        "Total_profit" : Total_profit
    }
    

@router.get("/intrest_rate/{id}")
def intrest(id :int, db: Session = Depends(get_db),current_user : UserRegistration = Depends(get_currentuser)):
    
    loan = db.query(Transation).filter(Transation.id == id ).first()
    
    if  not loan :
        raise HTTPException(status_code=404, detail= 'Item not present')
        
    
    today = date.today()
    
    days = (today - loan.loan_date).days
    
    daily_interest = (loan.amount * loan.intrest_rate / 100) /30
    
    Total_intrest = round(daily_interest  * days ,2)
    
    Total_amount = round(loan.amount + Total_intrest, 2)
    
    return {
        "loan_amount": loan.amount,
        "loan_date" : loan.loan_date,
        "interest_rate": loan.intrest_rate ,
        "days": days,
        "daily_interest": daily_interest,
        "total_interest": Total_intrest,
        "total_payable": Total_amount
    }
    
@router.put("/update_intrest")
def update_intrest(
    db: Session = Depends(get_db),
    current_user: UserRegistration = Depends(get_currentuser)
):

    loans = db.query(Transation).all()

    today = date.today()

    for loan in loans:

        days = (today - loan.loan_date).days

        monthly_interest = (loan.amount * loan.intrest_rate) / 100

        daily_interest = monthly_interest / 30

        total_interest = round(daily_interest * days,2)

        total_amount = round(loan.amount + total_interest,2)

        loan.total_days = days
        loan.interest_amount = total_interest
        loan.total_amount = total_amount

    db.commit()

    return {
        "message": "Interest updated successfully"
    }
            