from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.loan import LoanRequest, LoanOut
from services.loan_service import request_loan, confirm_loan, return_loan, overdue_loans, get_user_loans, return_loan_by_user
from routers.users import get_current_user

router = APIRouter()

@router.post("/request", response_model=LoanOut)
def api_request(payload: LoanRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        return request_loan(db, current_user.id, payload.book_id)
    except Exception as e:
        raise HTTPException(400, str(e))

@router.post("/{loan_id}/confirm", response_model=LoanOut)
def api_confirm(loan_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        return confirm_loan(db, loan_id)
    except Exception as e:
        raise HTTPException(400, str(e))

@router.get("/my_loans", response_model=list[LoanOut])
def api_my_loans(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Retorna todos os empréstimos (ativos e históricos) do usuário logado."""
    try:
        return get_user_loans(db, current_user.id)
    except Exception as e:
        raise HTTPException(400, str(e))

@router.post("/{loan_id}/return", response_model=LoanOut)
def api_return(loan_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Permite que o usuário logado devolva um livro."""
    try:
        return return_loan_by_user(db, loan_id, current_user.id)
    except Exception as e:
        raise HTTPException(400, str(e))

@router.post("/{loan_id}/confirm", response_model=LoanOut)
def api_confirm(loan_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Endpoint para o proprietário confirmar o empréstimo (mantido para compatibilidade)."""
    try:
        return confirm_loan(db, loan_id)
    except Exception as e:
        raise HTTPException(400, str(e))

@router.post("/{loan_id}/return", response_model=LoanOut)
def api_return(loan_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        return return_loan(db, loan_id)
    except Exception as e:
        raise HTTPException(400, str(e))

@router.get("/overdue", response_model=list[LoanOut])
def api_overdue(db: Session = Depends(get_db)):
    return overdue_loans(db)
