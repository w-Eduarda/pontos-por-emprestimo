from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.settings import settings
from core.database import Base, engine
from routers import users as users_router, books as books_router, loans as loans_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="P2P Livros — Backend Modular", version="1.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router.router, prefix="/api/users", tags=["users"])
app.include_router(books_router.router, prefix="/api/books", tags=["books"])
app.include_router(loans_router.router, prefix="/api/loans", tags=["loans"])

@app.get("/")
def root():
    return {"message": "P2P Livros API — modular backend. Acesse /docs para explorar."}
