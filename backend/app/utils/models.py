from pydantic import BaseModel

class QueryRequest(BaseModel):
    user_id: str
    user_query: str 

class QueryForm(BaseModel):
    user_id: str
    name: str
    email: str
    phone: str = None 
    address: str 
    company: str = None
    referral_source: str
    budget: int 
    timeline_months: int
    interest_level: str
    requested_capacity: str
    enquiry: str







