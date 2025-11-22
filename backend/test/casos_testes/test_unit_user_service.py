# Arquivo: test_unit_user_service.py
# Localização Sugerida: backend/tests/

import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from schemas.user import UserCreate
from services.user_service import register

# Cria um objeto de sessão mock para simular o banco de dados
mock_db = MagicMock(spec=Session)

# Cria um payload de dados de usuário para o teste
user_payload = UserCreate(
    name="Teste Mock",
    email="mock@teste.com",
    password="senhaforte123"
)

@patch('services.user_service.hash_password')
@patch('services.user_service.user_repository')
def test_register_user_success_with_mock(mock_repo, mock_hash_password):
    """
    Testa o registro de um novo usuário com sucesso, isolando o repositório
    e a função de hash de senha.
    """
    # 1. Configuração do Mock do Repositório
    # Simula que o email NÃO existe no banco de dados
    mock_repo.get_by_email.return_value = None
    
    # Simula o retorno da criação do usuário (o objeto User criado)
    mock_created_user = MagicMock()
    mock_repo.create.return_value = mock_created_user
    
    # 2. Configuração do Mock de Segurança
    # Simula o hash da senha
    mock_hash_password.return_value = "hashed_password_mock"

    # 3. Execução da Função a ser Testada
    result = register(db=mock_db, payload=user_payload)

    # 4. Asserções (Verificações)
    
    # Verifica se a função de busca por email foi chamada
    mock_repo.get_by_email.assert_called_once_with(mock_db, user_payload.email)
    
    # Verifica se a função de hash de senha foi chamada com a senha correta
    mock_hash_password.assert_called_once_with(user_payload.password)
    
    # Verifica se a função de criação foi chamada com os dados corretos
    mock_repo.create.assert_called_once()
    
    # Verifica se o resultado é o usuário mockado
    assert result == mock_created_user

@patch('services.user_service.user_repository')
def test_register_user_email_exists_raises_error(mock_repo):
    """
    Testa se a função levanta um erro quando o email já existe.
    """
    # 1. Configuração do Mock do Repositório
    # Simula que o email JÁ existe no banco de dados
    mock_repo.get_by_email.return_value = MagicMock()
    
    # 2. Execução e Asserção de Exceção
    with pytest.raises(ValueError) as excinfo:
        register(db=mock_db, payload=user_payload)
        
    # Verifica se a mensagem de erro está correta
    assert "Email já cadastrado." in str(excinfo.value)
    
    # Verifica se a função de criação NÃO foi chamada
    mock_repo.create.assert_not_called()
