# Arquivo: test_api_integration.py
# Localização Sugerida: backend/tests/

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app # Importa a aplicação FastAPI principal
from core.database import Base, get_db # Importa o Base e a função de dependência
from models.user import User # Importa o modelo de usuário para verificação no DB

# --- Configuração do Ambiente de Teste (Reutilizado da análise anterior) ---

# 1. Configuração de um Banco de Dados de Teste em Memória
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db" 
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2. Sobrescreve a dependência get_db para usar o banco de dados de teste
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# 3. Cria o cliente de teste
client = TestClient(app)

# 4. Funções de Setup/Teardown para isolamento
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
    # Limpa as tabelas (de forma simples para o nível de estudante)
    db.execute("DELETE FROM users")
    db.execute("DELETE FROM books")
    db.execute("DELETE FROM loans")
    db.commit()
    db.close()

# --- Funções Auxiliares ---

def register_test_user(email="test@user.com", password="password", name="Test User"):
    """Função auxiliar para registrar um usuário e retornar o token."""
    client.post("/api/users/register", json={"name": name, "email": email, "password": password})
    
    response = client.post("/api/users/login", json={"email": email, "password": password})
    return response.json()["access_token"]

# --- Testes de API (Usuários) ---

def test_api_login_user_full_flow_success():
    """
    Teste de Integração: Login bem-sucedido.
    Cenário: Usuário registrado faz login com credenciais corretas.
    """
    # Pré-condição: Registro
    register_test_user(email="login@test.com", password="password")
    
    # Execução: Login
    response = client.post("/api/users/login", json={"email": "login@test.com", "password": "password"})
    
    # Asserções
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_api_login_user_full_flow_invalid_password():
    """
    Teste de Integração: Login com senha incorreta.
    Cenário: Usuário registrado tenta login com senha errada.
    """
    # Pré-condição: Registro
    register_test_user(email="wrongpass@test.com", password="password")
    
    # Execução: Login com senha errada
    response = client.post("/api/users/login", json={"email": "wrongpass@test.com", "password": "wrongpassword"})
    
    # Asserções
    assert response.status_code == 401
    assert "Credenciais inválidas" in response.json()["detail"]

# --- Testes de API (Livros) ---

def test_api_add_book_auth_required_unauthorized():
    """
    Teste de API: Cadastro de livro sem autenticação.
    Cenário: Tentar cadastrar um livro sem fornecer um token JWT.
    """
    book_data = {"title": "Livro Secreto", "author": "Autor X", "points": 10}
    
    # Execução: Sem token
    response = client.post("/api/books/", json=book_data)
    
    # Asserções
    assert response.status_code == 401
    assert "Não autenticado" in response.json()["detail"]

def test_api_add_book_auth_required_success():
    """
    Teste de API: Cadastro de livro com autenticação.
    Cenário: Usuário autenticado cadastra um livro.
    """
    # Pré-condição: Autenticação
    token = register_test_user(email="bookowner@test.com")
    
    book_data = {"title": "O Teste Funcional", "author": "Manu S.", "points": 10}
    
    # Execução: Com token
    response = client.post(
        "/api/books/", 
        json=book_data, 
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Asserções
    assert response.status_code == 200
    assert response.json()["title"] == book_data["title"]
    assert response.json()["owner_id"] is not None

# --- Testes de API (Empréstimos) ---

def test_api_request_loan_full_flow_success():
    """
    Teste de Integração: Solicitação de empréstimo bem-sucedida.
    Cenário: Usuário com pontos suficientes solicita um livro disponível.
    """
    # Pré-condição 1: Usuário A (dono do livro)
    owner_token = register_test_user(email="owner@test.com", name="Owner")
    
    # Pré-condição 2: Usuário B (solicitante)
    requester_token = register_test_user(email="requester@test.com", name="Requester")
    
    # Pré-condição 3: Cadastro do livro (custa 10 pontos)
    book_data = {"title": "O Livro do Empréstimo", "author": "Autor Z", "points": 10}
    book_response = client.post(
        "/api/books/", 
        json=book_data, 
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    book_id = book_response.json()["id"]
    
    # Execução: Solicitação de empréstimo
    loan_request_data = {"book_id": book_id}
    response = client.post(
        "/api/loans/request", 
        json=loan_request_data, 
        headers={"Authorization": f"Bearer {requester_token}"}
    )
    
    # Asserções
    assert response.status_code == 200
    assert response.json()["book_id"] == book_id
    assert response.json()["status"] == "pending"
    
def test_api_request_loan_full_flow_insufficient_points():
    """
    Teste de Integração: Solicitação de empréstimo com pontos insuficientes.
    Cenário: Usuário com 50 pontos tenta solicitar um livro que custa 100 pontos.
    """
    # Pré-condição 1: Usuário A (dono do livro)
    owner_token = register_test_user(email="richowner@test.com", name="Rich Owner")
    
    # Pré-condição 2: Usuário B (solicitante) - Inicia com 50 pontos
    requester_token = register_test_user(email="poorrequester@test.com", name="Poor Requester")
    
    # Pré-condição 3: Cadastro do livro (custa 100 pontos)
    book_data = {"title": "O Livro Caro", "author": "Autor Y", "points": 100}
    book_response = client.post(
        "/api/books/", 
        json=book_data, 
        headers={"Authorization": f"Bearer {owner_token}"}
    )
    book_id = book_response.json()["id"]
    
    # Execução: Solicitação de empréstimo
    loan_request_data = {"book_id": book_id}
    response = client.post(
        "/api/loans/request", 
        json=loan_request_data, 
        headers={"Authorization": f"Bearer {requester_token}"}
    )
    
    # Asserções
    assert response.status_code == 400
    assert "Pontos insuficientes" in response.json()["detail"]
