# Arquivo: test_unit_notifications_estudante.py
# Testes Unitários para o Módulo de Notificações (utils/notifications.py)
# Simula o envio de e-mail para garantir que a função de notificação chame o que precisa.

import pytest
from unittest.mock import MagicMock, patch
from utils.notifications import send_loan_request_notification

# Mockamos a função de envio de e-mail real para não enviar e-mails de verdade durante o teste
@patch('utils.notifications.send_email') 
def test_send_loan_request_notification_sucesso(mock_send_email):
    """
    Teste 1: Verifica se a notificação de solicitação de empréstimo é enviada corretamente.
    """
    # Arrange (Preparação)
    # Criamos objetos mock para simular o livro, o dono e o solicitante
    mock_book = MagicMock(title="Estruturas de Dados")
    mock_owner = MagicMock(email="dono@teste.com", name="Dono")
    mock_requester = MagicMock(name="Solicitante")
    
    # Act (Ação)
    send_loan_request_notification(
        book=mock_book,
        owner=mock_owner,
        requester=mock_requester
    )

    # Assert (Verificação)
    # A função de envio de e-mail DEVE ser chamada exatamente uma vez
    mock_send_email.assert_called_once()
    
    # Verificamos se a função foi chamada com os argumentos corretos
    args, kwargs = mock_send_email.call_args
    
    # O primeiro argumento (args[0]) deve ser o e-mail do dono
    assert args[0] == "dono@teste.com"
    
    # O assunto do e-mail deve conter o nome do livro
    assert "Nova Solicitação de Empréstimo" in args[1]
    
    # O corpo do e-mail deve conter o nome do solicitante e o título do livro
    assert "Solicitante" in args[2]
    assert "Estruturas de Dados" in args[2]

@patch('utils.notifications.send_email') 
def test_send_loan_request_notification_dados_incompletos(mock_send_email):
    """
    Teste 2: Verifica se a função lida bem com dados incompletos (ex: nome do solicitante faltando).
    """
    # Arrange (Preparação)
    mock_book = MagicMock(title="Redes de Computadores")
    mock_owner = MagicMock(email="dono2@teste.com", name="Dono 2")
    mock_requester = MagicMock(name=None) # Nome do solicitante é None
    
    # Act (Ação)
    send_loan_request_notification(
        book=mock_book,
        owner=mock_owner,
        requester=mock_requester
    )

    # Assert (Verificação)
    # A função de envio de e-mail DEVE ser chamada, mesmo com o nome faltando (o e-mail é o mais importante)
    mock_send_email.assert_called_once()
    
    # Verificamos se o corpo do e-mail não quebra e ainda menciona o livro
    args, kwargs = mock_send_email.call_args
    assert "Redes de Computadores" in args[2]
