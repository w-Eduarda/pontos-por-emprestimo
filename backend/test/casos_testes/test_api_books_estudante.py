# Arquivo: test_api_books_estudante.py
# Testes de Integração de API para os endpoints de Livros (Books)
# Usei o TestClient do FastAPI para simular requisições HTTP de verdade.

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app 
from core.database import Base, get_db 
from models.user import User 
from models.book import Book 

# --- Configuração do Ambiente de Teste (Padrão para isolamento) ---

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_books_estudante.db" 
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    """Cria e remove as tabelas no início e fim do módulo de teste."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(autouse=True)
def clean_db():
    """Limpa os dados antes de cada teste."""
    db = TestingSessionLocal()
    db.execute("DELETE FROM users")
    db.execute("DELETE FROM books")
    db.commit()
    db.close()

# --- Funções Auxiliares ---

def register_and_login(email, password, name="Test User"):
    """Função auxiliar para registrar e logar um usuário, retornando o token."""
    client.post("/api/users/register", json={"name": name, "email": email, "password": password})
    response = client.post("/api/users/login", json={"email": email, "password": password})
    return response.json()["access_token"]

# --- Testes de API (Livros) ---

def test_api_post_add_book_sucesso():
    """
    Teste POST: Cadastrar um novo livro.
    Verifica se o status é 200 (OK) e se o livro foi criado.
    """
    # 1. Pré-condição: Precisamos de um usuário logado para cadastrar
    token = register_and_login("post_book@test.com", "senha123", "Cadastrador")
    
    book_data = {"title": "POO com Python", "author": "Estudante CC", "points": 10}
    
    # 2. Ação: Enviar a requisição POST
    response = client.post(
        "/api/books/", 
        json=book_data, 
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # 3. Verificação:
    assert response.status_code == 200 # O status HTTP tem que ser 200
    data = response.json()
    assert data["title"] == book_data["title"]
    assert "id" in data # O livro deve ter um ID gerado

def test_api_get_list_books_sucesso():
    """
    Teste GET: Listar todos os livros disponíveis.
    Verifica se o status é 200 (OK) e se a lista não está vazia (se tiver livros).
    """
    # 1. Pré-condição: Precisamos de um livro cadastrado para listar
    token = register_and_login("get_book@test.com", "senha123", "Listador")
    book_data = {"title": "Banco de Dados", "author": "Estudante CC", "points": 5}
    client.post(
        "/api/books/", 
        json=book_data, 
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # 2. Ação: Enviar a requisição GET
    response = client.get("/api/books/")
    
    # 3. Verificação:
    assert response.status_code == 200 # O status HTTP tem que ser 200
    data = response.json()
    assert isinstance(data, list) # A resposta deve ser uma lista
    assert len(data) > 0 # Deve ter pelo menos o livro que cadastramos
    assert data[0]["title"] == book_data["title"]
