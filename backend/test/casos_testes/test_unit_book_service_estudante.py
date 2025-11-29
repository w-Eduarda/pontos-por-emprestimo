# Arquivo: test_unit_book_service_estudante.py
# Testes Unitários para o Serviço de Livros (book_service.py)
# Usando Pytest e Mocks para simular o banco de dados e isolar a lógica.

import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from schemas.book import BookCreate
from services.book_service import add_book

# 1. Setup: Criei um "banco de dados falso" (mock) e um payload de dados
mock_db = MagicMock(spec=Session)
mock_owner = MagicMock(id=1, points=100) # O usuário que está cadastrando o livro

book_payload = BookCreate(
    title="Livro de Algoritmos",
    author="Estudante CC",
    points=30 # Custa 30 pontos para emprestar
)

@patch('services.book_service.book_repository')
def test_add_book_sucesso(mock_repo):
    """
    Teste 1: Verifica se o livro é cadastrado com sucesso.
    A gente simula que o repositório vai criar o livro de boa.
    """
    # Arrange (Preparação)
    mock_created_book = MagicMock()
    mock_repo.create.return_value = mock_created_book # Dizemos ao mock o que retornar
    
    # Act (Ação)
    result = add_book(db=mock_db, payload=book_payload, owner=mock_owner)

    # Assert (Verificação)
    # O repositório DEVE ser chamado para criar o livro
    mock_repo.create.assert_called_once()
    # O resultado deve ser o livro que o mock "criou"
    assert result == mock_created_book

@patch('services.book_service.book_repository')
def test_add_book_pontos_negativos_erro(mock_repo):
    """
    Teste 2: Verifica se dá erro se tentarmos cadastrar um livro com pontos negativos.
    Isso é uma regra de negócio importante!
    """
    # Arrange (Preparação)
    invalid_payload = BookCreate(
        title="Livro Grátis Demais",
        author="Estudante CC",
        points=-10 # Ponto negativo, não pode!
    )
    
    # Act & Assert (Ação e Verificação)
    # Esperamos que a função levante um erro (ValueError)
    with pytest.raises(ValueError) as excinfo:
        add_book(db=mock_db, payload=invalid_payload, owner=mock_owner)
        
    # Verificamos se a mensagem de erro é a esperada
    assert "Pontos para empréstimo devem ser positivos" in str(excinfo.value)
    
    # O repositório NÃO DEVE ser chamado, pois a validação falhou antes
    mock_repo.create.assert_not_called()
