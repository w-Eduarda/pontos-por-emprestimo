# Arquivo: test_integration_users.py
# Localização Sugerida: backend/tests/

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app # Importa a aplicação FastAPI principal
from core.database import Base, get_db # Importa o Base e a função de dependência
from models.user import User # Importa o modelo de usuário para verificação no DB

# 1. Configuração de um Banco de Dados de Teste em Memória
# Usaremos um arquivo SQLite para persistência temporária
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db" 
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# Cria uma sessão de banco de dados de teste
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

def setup_function():
    """Cria as tabelas antes de cada teste."""
    Base.metadata.create_all(bind=engine)

def teardown_function():
    """Remove as tabelas após cada teste para garantir isolamento."""
    Base.metadata.drop_all(bind=engine)

def test_api_register_user_full_flow():
    """
    Testa a integração completa da rota de registro (Router -> Service -> Repository -> DB).
    """
    # Dados de registro
    user_data = {
        "name": "Alice Teste",
        "email": "alice@teste.com",
        "password": "senhateste"
    }
    
    # 4. Execução da Requisição
    response = client.post(
        "/api/users/register",
        json=user_data
    )
    
    # 5. Asserções
    assert response.status_code == 200
    data = response.json()
    
    # Verifica se os dados retornados estão corretos
    assert data["email"] == user_data["email"]
    assert "id" in data
    assert data["points"] == 50 # Verifica se os pontos iniciais foram atribuídos
    
    # Verifica se o usuário foi realmente criado no banco de dados
    db = TestingSessionLocal()
    created_user = db.query(User).filter(User.email == user_data["email"]).first()
    db.close()
    
    assert created_user is not None
    assert created_user.name == user_data["name"]
    
def test_api_register_user_email_exists_integration():
    """
    Testa a integração quando se tenta registrar um email já existente.
    """
    # Cria o primeiro usuário
    client.post(
        "/api/users/register",
        json={
            "name": "Primeiro",
            "email": "existente@teste.com",
            "password": "senha"
        }
    )
    
    # Dados de registro do segundo usuário (com email duplicado)
    user_data = {
        "name": "Segundo",
        "email": "existente@teste.com", # Email já existente
        "password": "senhateste"
    }
    
    # Execução da Requisição
    response = client.post(
        "/api/users/register",
        json=user_data
    )
    
    # Asserções
    assert response.status_code == 400
    assert "Email já cadastrado." in response.json()["detail"]
