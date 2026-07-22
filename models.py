from datetime import date
from database import Base,engine
from sqlalchemy import Column, Integer, VARCHAR, DATE, TIMESTAMP, func

class UserRegistration(Base):
    __tablename__ = "secure_bank_user_registration"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(VARCHAR(50))
    mobile_number = Column(VARCHAR(10))
    email = Column(VARCHAR(100))
    user_name = Column(VARCHAR(63))
    user_password =Column(VARCHAR(20))
    opening_date = Column(DATE, default=date.today)
    created_at = Column(TIMESTAMP, server_default = func.now())
    
class Transation(Base):
    __tablename__ = 'secure_bank_user_transations'
    
    id = Column(Integer, autoincrement=True, index=True, primary_key=True)
    full_name = Column(VARCHAR(50))
    mobile_number = Column(VARCHAR(10))
    email = Column(VARCHAR(50))
    amount =Column(VARCHAR(10))
    loan_date = Column(DATE, default=date.today)
    created_at = Column(TIMESTAMP, server_default = func.now())
    
    


# for creating the table 
Base.metadata.create_all(bind = engine)