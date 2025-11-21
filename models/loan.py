from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class Loan(Base):
    __tablename__ = "loans"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    lender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    borrower_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    requested_at = Column(DateTime, default=datetime.utcnow)
    start_date = Column(Date)
    due_date = Column(Date)
    returned_date = Column(Date)
    status = Column(String, default="requested")

    book = relationship("Book")
    lender = relationship("User", foreign_keys=[lender_id], back_populates="loans_lent")
    borrower = relationship("User", foreign_keys=[borrower_id], back_populates="loans_borrowed")
