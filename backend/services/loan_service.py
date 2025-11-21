from sqlalchemy.orm import Session
from datetime import date, timedelta
from repositories import loan_repository, user_repository, book_repository
from models.loan import Loan
from config.constants import (
    CREDIT_PER_LEND, DEBIT_PER_BORROW, MIN_POINTS_TO_BORROW,
    MAX_ACTIVE_LOANS, LATE_FINE_PER_DAY, DEFAULT_LOAN_DAYS
)
from utils.notifications import send_notification_stub

def count_active_loans(db: Session, user_id: int):
    return len(loan_repository.get_active_by_borrower(db, user_id))

def get_user_loans(db: Session, user_id: int):
    """Retorna todos os empréstimos (ativos e históricos) de um usuário."""
    return loan_repository.get_by_borrower_id(db, user_id)

def return_loan_by_user(db: Session, loan_id: int, user_id: int):
    """Permite que o usuário devolva um livro, verificando se ele é o tomador."""
    loan = loan_repository.get(db, loan_id)
    if not loan:
        raise ValueError("Empréstimo não encontrado.")
    if loan.borrower_id != user_id:
        raise PermissionError("Você não tem permissão para devolver este livro.")
    
    # Reutiliza a lógica de return_loan
    return return_loan(db, loan_id)

def request_loan(db: Session, borrower_id: int, book_id: int):
    book = book_repository.get(db, book_id)
    if not book or not book.available:
        raise ValueError("Livro indisponível.")
    borrower = user_repository.get(db, borrower_id)
    if not borrower:
        raise ValueError("Usuário não encontrado.")
    if borrower.points < MIN_POINTS_TO_BORROW:
        raise ValueError("Pontos insuficientes.")
    if count_active_loans(db, borrower_id) >= MAX_ACTIVE_LOANS:
        raise ValueError("Limite de empréstimos ativos atingido.")

    loan = Loan(book_id=book.id, borrower_id=borrower_id, lender_id=book.owner_id)
    loan = loan_repository.create(db, loan)

    send_notification_stub(book.owner.email, "Pedido de empréstimo", f"{borrower.name} solicitou '{book.title}'.")

    return loan

def confirm_loan(db: Session, loan_id: int):
    loan = loan_repository.get(db, loan_id)
    if not loan:
        raise ValueError("Pedido não encontrado.")
    if loan.status != "requested":
        raise ValueError("Este empréstimo não está pendente.")

    borrower = user_repository.get(db, loan.borrower_id)
    lender = user_repository.get(db, loan.lender_id)
    book = book_repository.get(db, loan.book_id)

    loan.start_date = date.today()
    loan.due_date = loan.start_date + timedelta(days=DEFAULT_LOAN_DAYS)
    loan.status = "active"
    book.available = False

    lender.points += CREDIT_PER_LEND
    borrower.points -= DEBIT_PER_BORROW

    loan_repository.update(db, loan)
    book_repository.update(db, book)
    user_repository.update(db, lender)
    user_repository.update(db, borrower)

    return loan

def return_loan(db: Session, loan_id: int):
    loan = loan_repository.get(db, loan_id)
    if not loan or loan.status != "active":
        raise ValueError("Empréstimo inválido.")

    today = date.today()
    loan.returned_date = today
    loan.status = "returned"

    book = book_repository.get(db, loan.book_id)
    book.available = True

    if loan.due_date and today > loan.due_date:
        days_late = (today - loan.due_date).days
        borrower = user_repository.get(db, loan.borrower_id)
        borrower.points -= days_late * LATE_FINE_PER_DAY
        user_repository.update(db, borrower)

    loan_repository.update(db, loan)
    book_repository.update(db, book)

    return loan

def overdue_loans(db: Session):
    return loan_repository.get_overdue(db)
