from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import text,func,or_
from models import Transation,UserRegistration
from schemas import userTransation
from database import get_db
from Registration import get_currentuser
from datetime import date

from typing import Any


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
    
@router.get("/get_userTransation")
def getUserTransation(
    page: int = Query(default=1, ge=1, description="Page number"),
    limit: int = Query(default=10, ge=1, le=50, description="Total records per page"),
    search: str | None = Query(default=None, max_length=100, description="Search"),
    db: Session = Depends(get_db),
    current_user: UserRegistration = Depends(get_currentuser)
):

    # 1. Calculate offset
    offset = (page - 1) * limit

    # 2. Clean search
    search = search.strip() if search else None

    # 3. Base query
    query = db.query(Transation)

    # 4. Apply search
    if search:
        search_value = f"%{search}%"

        query = query.filter(
            or_(
                Transation.full_name.ilike(search_value),
                Transation.mobile_number.ilike(search_value),
                Transation.email.ilike(search_value)
            )
        )

    # 5. Total count AFTER search filter
    all_transation_count = query.count()

    # 6. Get paginated transactions
    all_transation = (
        query
        .order_by(Transation.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    # 7. Calculate totals
    Total_amount = db.query(
        func.sum(Transation.amount)
    ).scalar() or 0

    Total_interest_amount = db.query(
        func.sum(Transation.total_amount)
    ).scalar() or 0

    Total_profit = Total_interest_amount - Total_amount

    # 8. Return response
    return {
        "page": page,
        "limit": limit,
        "total_records": all_transation_count,
        "total_pages": (all_transation_count + limit - 1) // limit,
        "Transation_List": all_transation,
        "Total_amount": Total_amount,
        "Total_interest_amount": Total_interest_amount,
        "Total_profit": Total_profit
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
            