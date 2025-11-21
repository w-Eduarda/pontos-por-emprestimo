from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.user import UserCreate, UserOut, Token, UserLogin
from services.user_service import register, authenticate
from core.security import decode_token
from core.exceptions import unauthorized
from repositories.user_repository import get as get_user_repo

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")

@router.post("/register", response_model=UserOut)
def api_register(payload: UserCreate, db: Session = Depends(get_db)):
    try:
        return register(db, payload)
    except Exception as e:
        raise HTTPException(400, str(e))

@router.post("/login", response_model=Token)
def api_login(form: UserLogin, db: Session = Depends(get_db)):
    out = authenticate(db, form.email, form.password)
    if not out:
        raise HTTPException(401, "Credenciais inválidas.")
    return {"access_token": out["access_token"], "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        data = decode_token(token)
        user = get_user_repo(db, int(data["sub"]))
        if not user:
            unauthorized("Usuário não encontrado.")
        return user
    except:
        unauthorized("Token inválido.")
