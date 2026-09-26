documents = [

    """
TABLE: public.secure_bank_user_registration

DESCRIPTION:
This table stores basic customer information for customers who have taken a loan.

COLUMNS:

full_name:
Full name of the customer.

mobile_number:
Registered mobile number of the customer. Can be used to identify the customer.

email:
Registered email address of the customer.

user_name:
Username associated with the customer's account.

user_password:
Sensitive authentication credential. This column must NEVER be retrieved, exposed,
or returned by the chatbot.

opening_date:
Date on which the customer's loan account was opened.

CUSTOMER IDENTIFICATION:
Customers can be identified using full_name, mobile_number, email, or user_name.
For customer-specific queries, mobile_number is preferred when available.

BUSINESS PURPOSE:
This table is used to retrieve basic customer/account information.

EXAMPLES OF QUESTIONS:
- Who is the customer with mobile number 9876543210?
- When was Rahul Kumar's account opened?
- How many customers opened accounts in August 2026?

SECURITY:
Never expose user_password.
Do not include actual passwords in the RAG context or LLM prompt.
""",

    """
TABLE: public.secure_bank_user_transations

DESCRIPTION:
This table stores loan and financial details for customers who have taken a loan.
Each record represents a loan transaction/account.

COLUMNS:

id:
Unique identifier for the loan record.

full_name:
Full name of the customer associated with the loan.

mobile_number:
Registered mobile number of the customer. Can be used to identify the customer.

email:
Registered email address of the customer.

amount:
Principal loan amount given to the customer before interest.

loan_date:
Date on which the loan was issued or taken by the customer.

created_at:
Date and time when the loan record was created in the database.

intrest_rate:
Interest rate applicable to the loan.
IMPORTANT: The actual database column name is "intrest_rate".
Use "intrest_rate" when generating SQL.

total_days:
Total duration of the loan in days.

interest_amount:
Total interest amount calculated for the loan.

total_amount:
Total amount payable by the customer, including principal amount and interest.

FINANCIAL RELATIONSHIP:

amount:
Principal loan amount.

intrest_rate:
Applicable interest rate.

total_days:
Loan duration.

interest_amount:
Calculated interest amount.

total_amount:
Principal amount plus interest amount.

BUSINESS PURPOSE:
This table is used to retrieve customer loan and financial information.

CUSTOMER IDENTIFICATION:
Customers can be identified using id, full_name, mobile_number, or email.
For customer-specific queries, mobile_number or id should preferably be used because names
may not be unique.

EXAMPLES OF QUESTIONS:
- How much loan did Rahul Kumar take?
- What is the loan amount for mobile number 9876543210?
- What is the interest rate?
- How many days is the loan?
- How much interest does the customer have to pay?
- What is the total amount payable?
- When was the loan taken?
- What is the total loan amount?

SECURITY:
mobile_number and email are personal information.
The chatbot should only return this information to authorized users.

IMPORTANT:
Do not assume relationships between tables unless a valid database relationship exists.
Prefer customer_id/user_id if such a column exists.
"""
]