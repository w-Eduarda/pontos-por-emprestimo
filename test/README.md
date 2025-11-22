# Testes do Sistema P2P Livros

## Estrutura

A pasta de testes deve seguir a seguinte organização:

```
tests/
├── casos_testes/ → Scripts ou arquivos com casos de teste (Ex: test_unit_user_service.py)
├── evidencias/ → Capturas de tela, logs e relatórios de execução
└── README.md
```

## Como executar os testes

Os testes do backend (FastAPI/Python) devem ser executados utilizando o framework **`pytest`**.

1.  **Instalar dependências de teste:**
    ```bash
    pip install pytest pytest-cov
    ```
2.  **Executar todos os testes:**
    ```bash
    pytest
    ```
3.  **Gerar relatório de cobertura (opcional):**
    ```bash
    pytest --cov=.
    ```

## Status de Testes

Abaixo está o status dos testes **previstos** e **exemplificados** na análise de Teste de Software.

| Tipo de Teste | Componente | Teste Previsto | Estado Atual |
| :--- | :--- | :--- | :--- |
| **Unitário** | `user_service.py` | `test_register_user_success_with_mock` | Implementado (Exemplo) |
| **Unitário** | `user_service.py` | `test_register_user_email_exists_raises_error` | Implementado (Exemplo) |
| **Integração** | Rota `/register` | `test_api_register_user_full_flow` | Implementado (Exemplo) |
| **Integração** | Rota `/register` | `test_api_register_user_email_exists_integration` | Implementado (Exemplo) |
| **Unitário** | Outros Serviços/Repositórios | `test_authenticate_user_success` | Pendente |
| **Integração** | Rota `/login` | `test_api_login_user_full_flow` | Pendente |
| **Integração** | Rota `/books` | `test_api_add_book_auth_required` | Pendente |
| **Integração** | Rota `/loans` | `test_api_request_loan_full_flow` | Pendente |

**Observação:** Os testes marcados como **"Implementado (Exemplo)"** referem-se aos arquivos de exemplo (`test_unit_user_service.py` e `test_integration_users.py`) criados na análise. O restante da suíte de testes está **Pendente** de implementação.
