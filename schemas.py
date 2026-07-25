from pydantic import BaseModel,EmailStr
from datetime import datetime, date

class userRegistration(BaseModel):
    full_name : str
    mobile_number :str
    email : EmailStr                # it will take only email
    user_name : str
    user_password : str
    
class userLogin(BaseModel):
    email:EmailStr
    password : str
    
class userTransation(BaseModel):
    full_name : str
    mobile_number : str
    email : EmailStr
    amount : float
    loan_date : date
    
class userSupport(BaseModel):
    full_name : str
    mobile_number : str
    email : EmailStr
    Description : str