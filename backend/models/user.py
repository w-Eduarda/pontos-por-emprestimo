from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.database import Base
from config.constants import INITIAL_POINTS

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    points = Column(Integer, default=INITIAL_POINTS)

    owned_books = relationship("Book", back_populates="owner")
    loans_borrowed = relationship("Loan", back_populates="borrower", foreign_keys="Loan.borrower_id")
    loans_lent = relationship("Loan", back_populates="lender", foreign_keys="Loan.lender_id")
