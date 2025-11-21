from sqlalchemy.orm import Session
from models.user import User

def get_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get(db: Session, user_id: int):
    return db.query(User).get(user_id)

def create(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
