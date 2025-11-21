from sqlalchemy.orm import Session
from models.book import Book

def create(db: Session, book: Book):
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

def get(db: Session, book_id: int):
    return db.query(Book).get(book_id)

def search(db: Session, q=None, author=None):
    query = db.query(Book)
    if q:
        query = query.filter(Book.title.ilike(f"%{q}%"))
    if author:
        query = query.filter(Book.author.ilike(f"%{author}%"))
    return query.all()

def update(db: Session, book: Book):
    db.add(book)
    db.commit()
    db.refresh(book)
    return book
