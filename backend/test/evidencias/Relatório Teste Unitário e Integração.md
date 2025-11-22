# Relatório de Análise de Teste de Software: pontos-por-emprestimo

Este relatório detalha a análise da estratégia de testes para o projeto pontos-por-emprestimo, focando em Testes Unitários e Testes de Integração de Componentes, conforme a estrutura do backend em Python/FastAPI.

---

## 1. Teste de Unitários

O Teste Unitário foca em isolar e verificar a menor unidade de código testável, garantindo que a lógica interna de cada componente funcione corretamente.

### Lista dos Componentes de Cada Sistema

O backend do projeto pontos-por-emprestimo é estruturado em camadas, o que facilita a identificação de componentes para testes unitários:

| Camada | Componente | Descrição |
| :--- | :--- | :--- |
| **Serviços (Lógica de Negócio)** | `user_service.py` | Contém a lógica de negócio para registro e autenticação de usuários. |
| | `book_service.py` | Contém a lógica de negócio para livros (cadastro, listagem). |
| | `loan_service.py` | Contém a lógica de negócio para empréstimos (solicitação, confirmação, devolução). |
| **Repositórios (Acesso a Dados)** | `user_repository.py` | Abstrai o acesso ao banco de dados para a entidade `User`. |
| | `book_repository.py` | Abstrai o acesso ao banco de dados para a entidade `Book`. |
| | `loan_repository.py` | Abstrai o acesso ao banco de dados para a entidade `Loan`. |
| **Core (Funcionalidades Compartilhadas)** | `core/security.py` | Funções de segurança (hash de senha, criação/decodificação de tokens JWT). |

### Lista de Testes Unitários Previstos, mostrando o estado atual

Os testes unitários devem focar em isolar a lógica de negócio de cada componente.

| Componente | Teste Previsto | Estado Atual |
| :--- | :--- | :--- |
| `user_service.py` | `test_register_user_success` | Pendente |
| | `test_register_user_email_exists` | Pendente |
| | `test_authenticate_user_success` | Pendente |
| | `test_authenticate_user_invalid_password` | Pendente |
| `book_service.py` | `test_add_book_success` | Pendente |
| | `test_list_books_available` | Pendente |
| `loan_service.py` | `test_request_loan_success` | Pendente |
| | `test_request_loan_insufficient_points` | Pendente |
| `core/security.py` | `test_hash_and_verify_password` | Pendente |
| | `test_create_and_decode_token` | Pendente |

### Ferramentas Utilizadas

| Ferramenta | Uso |
| :--- | :--- |
| **`pytest`** | Framework de teste principal para Python. |
| **`unittest.mock`** (ou `pytest-mock`) | Para criar *mocks* e *stubs* para isolar dependências. |

### Exemplo de um Teste Unitário que Utilize Mock para Isolar as Dependências

O exemplo abaixo testa a função `register` do `user_service.py`, isolando o acesso ao banco de dados e a função de hash de senha através de *mocks*.

```python
# Arquivo: test_unit_user_service.py (Completo em anexo)

from unittest.mock import MagicMock, patch
from services.user_service import register
from schemas.user import UserCreate

# ... (criação de mock_db e user_payload)

@patch('services.user_service.hash_password')
@patch('services.user_service.user_repository')
def test_register_user_success_with_mock(mock_repo, mock_hash_password):
    """
    Testa o registro de um novo usuário com sucesso, isolando o repositório
    e a função de hash de senha.
    """
    # 1. Configuração do Mock do Repositório: Simula que o email NÃO existe
    mock_repo.get_by_email.return_value = None
    mock_created_user = MagicMock()
    mock_repo.create.return_value = mock_created_user
    
    # 2. Configuração do Mock de Segurança: Simula o hash da senha
    mock_hash_password.return_value = "hashed_password_mock"

    # 3. Execução da Função a ser Testada
    result = register(db=mock_db, payload=user_payload)

    # 4. Asserções (Verificações)
    mock_repo.get_by_email.assert_called_once_with(mock_db, user_payload.email)
    mock_hash_password.assert_called_once_with(user_payload.password)
    mock_repo.create.assert_called_once()
    assert result == mock_created_user
```

---

## 2. Teste de Integração de Componentes

O Teste de Integração de Componentes verifica se diferentes módulos ou serviços interagem corretamente entre si, simulando o fluxo de dados através das camadas do sistema.

### Lista das "Interfaces" entre Componentes

Os testes de integração de componentes focam na comunicação entre as camadas do backend (Roteadores -> Serviços -> Repositórios) e com o banco de dados.

| Interface | Componentes Envolvidos | Descrição |
| :--- | :--- | :--- |
| **API -> Serviço** | `routers/users.py` -> `services/user_service.py` | Verifica se o roteador (API) está chamando corretamente a função de serviço com os dados de entrada corretos e tratando as exceções. |
| **Serviço -> Repositório** | `services/user_service.py` -> `repositories/user_repository.py` | Verifica se a lógica de negócio está interagindo corretamente com a camada de acesso a dados. |
| **Repositório -> DB** | `repositories/*.py` -> `core/database.py` | Verifica se as operações de CRUD (Create, Read, Update, Delete) estão sendo executadas corretamente no banco de dados. |

### Ferramentas Utilizadas

| Ferramenta | Uso |
| :--- | :--- |
| **`pytest`** | Framework de teste principal. |
| **`TestClient` (FastAPI)** | Cliente HTTP síncrono para testar as rotas da API sem a necessidade de rodar o servidor. |
| **`SQLAlchemy`** | Utilizado para configurar um banco de dados temporário em memória (SQLite) para garantir que os testes sejam isolados e rápidos. |

### Lista dos Testes de Integração Previstos

| Teste Previsto | Componentes Envolvidos | Estado Atual |
| :--- | :--- | :--- |
| `test_api_register_user_full_flow` | Rota `/register` -> Serviço -> Repositório -> DB | Pendente |
| `test_api_login_user_full_flow` | Rota `/login` -> Serviço -> Repositório -> DB | Pendente |
| `test_api_add_book_auth_required` | Rota `POST /books/` (com e sem token) | Pendente |
| `test_api_request_loan_full_flow` | Rota `/loans/request` -> Serviço -> Repositório -> DB | Pendente |

### Exemplo de um Teste de Integração

O exemplo a seguir testa o fluxo completo de registro de usuário, desde a chamada da API até a persistência no banco de dados, usando o `TestClient` do FastAPI e um banco de dados em memória.

```python
# Arquivo: test_integration_users.py (Completo em anexo)

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from core.database import Base, get_db
from main import app

# ... (Configuração do banco de dados de teste e sobrescrita da dependência get_db)

client = TestClient(app)

def test_api_register_user_full_flow():
    """
    Testa a integração completa da rota de registro.
    """
    # Limpa e recria o banco de dados para isolamento
    # ...
    
    user_data = {
        "name": "Alice Teste",
        "email": "alice@teste.com",
        "password": "senhateste"
    }
    
    # Execução da Requisição (Integração Rota -> Serviço -> Repositório -> DB)
    response = client.post(
        "/api/users/register",
        json=user_data
    )
    
    # Asserções
    assert response.status_code == 200
    data = response.json()
    
    # Verifica se os dados retornados estão corretos
    assert data["email"] == user_data["email"]
    
    # Verifica se o usuário foi realmente criado no banco de dados
    # ... (consulta ao banco de dados de teste)
    
    assert created_user is not None
```

---

## 3. Estrutura de Arquivos e Conteúdo para Slides

### Estrutura de Pastas Sugerida

Os arquivos de teste devem ser organizados na pasta `backend/tests/` para manter a separação clara entre código de produção e código de teste.

```
p2p-livros-integrado-v2/
├── backend/
│   ├── ... (código de produção)
│   ├── tests/  <-- NOVA PASTA PARA TESTES
│   │   ├── test_unit_user_service.py  <-- Exemplo de Teste Unitário
│   │   ├── test_integration_users.py  <-- Exemplo de Teste de Integração
│   ├── ...
```

### Conteúdo para Slides

O arquivo `slides_content.md` (anexo) contém o conteúdo estruturado para 6 slides, seguindo a progressão lógica da disciplina.

| Slide | Título | Imagem Sugerida |
| :--- | :--- | :--- |
| **2** | Testes Unitários Garantem a Integridade da Lógica de Negócio | `unit_test_concept.png` (Lupa sobre código) |
| **3** | Isolando Dependências com Mock para Testes Puros | *Nenhuma imagem conceitual, focar no código de exemplo* |
| **4** | Testes de Integração Validam a Comunicação entre Camadas | `integration_test_concept.png` (Peças de quebra-cabeça) |
| **5** | Testando o Fluxo Completo de Registro via API | *Nenhuma imagem conceitual, focar no código de exemplo* |
| **6** | A Estratégia de Testes como Base para a Evolução do Sistema | `testing_overview_concept.png` (Escudo de QA) |
