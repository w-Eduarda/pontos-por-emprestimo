from sqlalchemy.orm import Session
from repositories import book_repository
from models.book import Book
from schemas.book import BookCreate

def add_book(db: Session, owner_id: int, payload: BookCreate):
    book = Book(
        title=payload.title,
        author=payload.author,
        condition=payload.condition,
        owner_id=owner_id,
        available=True
    )
    return book_repository.create(db, book)

def list_books(db: Session, q: str = None, author: str = None):
    return book_repository.search(db, q=q, author=author)
