from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.book import BookCreate, BookOut
from services.book_service import add_book, list_books
from routers.users import get_current_user

router = APIRouter()

@router.post("/", response_model=BookOut)
def api_add_book(payload: BookCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    try:
        return add_book(db, current_user.id, payload)
    except Exception as e:
        raise HTTPException(400, str(e))

@router.get("/", response_model=list[BookOut])
def api_list(q: str | None = Query(None), author: str | None = Query(None), db: Session = Depends(get_db)):
    return list_books(db, q, author)
