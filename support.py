from fastapi import APIRouter, Depends,Query
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text,func,or_
from models import Support
from schemas import userSupport
from email_service import send_email
from Registration import get_currentuser

router = APIRouter(prefix="/support", tags = ['support'], dependencies= [Depends(get_currentuser)]);

@router.post("/add_support")
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
    
    print("Calling send_email()...")
    send_email(
        sp.email,
         "We've Received Your Support Request - Secure Bank",
    f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, Helvetica, sans-serif;
                background-color: #f5f5f5;
                margin: 0;
                padding: 20px;
            }}

            .container {{
                max-width: 600px;
                margin: auto;
                background: #ffffff;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}

            .header {{
                background-color: #003366;
                color: white;
                text-align: center;
                padding: 20px;
                font-size: 24px;
                font-weight: bold;
            }}

            .content {{
                padding: 30px;
                color: #333333;
                line-height: 1.7;
            }}

            .details {{
                background: #f8f9fa;
                border-left: 4px solid #003366;
                padding: 15px;
                margin: 20px 0;
            }}

            .footer {{
                background: #eeeeee;
                text-align: center;
                padding: 15px;
                color: #666666;
                font-size: 13px;
            }}

            .button {{
                display: inline-block;
                padding: 12px 25px;
                background: #003366;
                color: white;
                text-decoration: none;
                border-radius: 4px;
                margin-top: 20px;
            }}
        </style>
    </head>

    <body>

        <div class="container">

            <div class="header">
                Secure Bank
            </div>

            <div class="content">

                <h2>Hello {sp.full_name},</h2>

                <p>
                    Thank you for contacting <strong>Secure Bank</strong>.
                </p>

                <p>
                    We have successfully received your support request.
                    Our support team will review your issue and get back to you
                    as soon as possible.
                </p>

                <div class="details">

                    <strong>Your Submitted Details</strong>

                    <br><br>

                    <strong>Name:</strong> {sp.full_name}<br>

                    <strong>Email:</strong> {sp.email}<br>

                    <strong>Mobile:</strong> {sp.mobile_number}<br>

                    <strong>Issue:</strong><br>

                    {sp.Description}

                </div>

                <p>
                    If additional information is required, one of our support
                    representatives will contact you.
                </p>

                <p>
                    We appreciate your patience and thank you for choosing
                    Secure Bank.
                </p>

                <p>
                    Best Regards,<br>
                    <strong>Secure Bank Support Team</strong>
                </p>

            </div>

            <div class="footer">
                © 2026 Secure Bank. All Rights Reserved.
            </div>

        </div>

    </body>

    </html>
    """
    )
    
    return {
        "full_name" : sp.full_name,
        "mobile_number" : sp.mobile_number,
        "email" : sp.email,
        "description": sp.Description,
        "message" : "We will get back to you soon"
        
    }

@router.get("/get_support")
def getSupport(
    page : int = Query(default=1, ge=1, description= "Page Number"),
    limit : int = Query(default=10, ge=1, le=100, description="Page limit"),
    search : str | None = Query(default=None,max_length=50, description= "search"),
    db:Session= Depends(get_db)):
    
    # 1. Calculate offset
    offset = (page - 1) * limit
    
    # 2. clean seach
    clean_search = search.strip() if search else None
    
    # 3. Base query( for getting all the data from the db)
    Base_query = db.query(Support)
    
    # 4. Apply search
    if clean_search:
        search_value = f"%{clean_search}%"
        
        Base_query = Base_query.filter(
            or_(
                Support.full_name.ilike(search_value),
                Support.mobile_number.ilike(search_value),
                Support.email.ilike(search_value)
            )
        )
    
    # 5. Total count after filter
    total_count = Base_query.count()
    
    # 6. get paginated result
    all_support = (Base_query.order_by(Support.id.desc())
                   .offset(offset)
                   .limit(limit).all())
     
    
    return {
        "page" : page,
        "limit" : limit,
        "Total_pages" : (total_count + limit - 1) // limit,
        "total_record" : total_count,
        "all_support" :all_support,
            }