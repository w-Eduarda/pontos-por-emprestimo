from sqlalchemy.orm import Session
from repositories import user_repository
from models.user import User
from core.security import hash_password, verify_password, create_access_token
from schemas.user import UserCreate
from config.constants import ACCESS_TOKEN_EXPIRE

def register(db: Session, payload: UserCreate):
    existing = user_repository.get_by_email(db, payload.email)
    if existing:
        raise ValueError("Email já cadastrado.")
    user = User(name=payload.name, email=payload.email, password=hash_password(payload.password))
    return user_repository.create(db, user)

def authenticate(db: Session, email: str, password: str):
    user = user_repository.get_by_email(db, email)
    if not user or not verify_password(password, user.password):
        return None

    token = create_access_token(str(user.id), expires_delta=ACCESS_TOKEN_EXPIRE)
    return {"access_token": token, "user": user}
