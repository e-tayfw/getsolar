from pydantic import BaseModel

class QueryRequest(BaseModel):
    user_id: str
    user_query: str 






