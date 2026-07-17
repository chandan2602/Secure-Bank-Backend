from datetime import date
from database import Base,engine
from sqlalchemy import func

from sqlalchemy import Column, Integer, VARCHAR, DATE, TIMESTAMP

class user_registration(Base):
    __tablename__ = "secure_bank_user_registration"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(VARCHAR(50))
    mobile_number = Column(VARCHAR(10))
    email = Column(VARCHAR(100))
    user_name = Column(VARCHAR(63))
    user_password =Column(VARCHAR(20))
    opening_date = Column(DATE, default=date.today)
    created_at = Column(TIMESTAMP, server_default = func.now())


# for creating the table 
Base.metadata.create_all(bind = engine)