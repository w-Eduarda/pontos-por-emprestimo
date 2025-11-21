from sqlalchemy.orm import Session
from models.loan import Loan
from datetime import date

def create(db: Session, loan: Loan):
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan

def get(db: Session, loan_id: int):
    return db.query(Loan).get(loan_id)

def get_active_by_borrower(db: Session, borrower_id: int):
    return db.query(Loan).filter(Loan.borrower_id == borrower_id, Loan.status == "active").all()

def get_by_borrower_id(db: Session, borrower_id: int):
    return db.query(Loan).filter(Loan.borrower_id == borrower_id).all()

def get_overdue(db: Session):
    today = date.today()
    return db.query(Loan).filter(Loan.status == "active", Loan.due_date < today).all()

def update(db: Session, loan: Loan):
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan
