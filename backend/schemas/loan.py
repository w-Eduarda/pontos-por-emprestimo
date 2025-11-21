from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class LoanRequest(BaseModel):
    book_id: int

class LoanOut(BaseModel):
    id: int
    book_id: int
    lender_id: int
    borrower_id: int
    requested_at: datetime
    start_date: Optional[date]
    due_date: Optional[date]
    returned_date: Optional[date]
    status: str

    class Config:
        orm_mode = True
