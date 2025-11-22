# Documentação do Módulo de Teste de Integração (Pytest/FastAPI)

## Arquivo: `test_api_integration.py`

Este documento descreve o arquivo `test_api_integration.py`, que contém testes de **Integração e Funcionais** para o *backend* da aplicação P2P Livros, construído com **FastAPI**. Os testes utilizam a *framework* **Pytest** e o cliente de teste nativo do FastAPI (`TestClient`) para simular requisições HTTP e verificar o comportamento da API, incluindo a interação com o banco de dados.

### 1. Visão Geral

| Característica | Detalhe |
| :--- | :--- |
| **Tecnologia** | Pytest, FastAPI, SQLAlchemy |
| **Tipo de Teste** | Teste de Integração e Funcional |
| **Funcionalidade Testada** | API *backend* (Usuários, Livros, Empréstimos) |
| **Configuração** | Utiliza um banco de dados SQLite em memória (`sqlite:///./test.db`) para isolamento. |

### 2. Configuração do Ambiente de Teste

O módulo implementa uma configuração robusta para garantir o isolamento e a reprodutibilidade dos testes.

#### 2.1. Banco de Dados de Teste

*   **Engine e Sessão:** Cria uma *engine* SQLAlchemy e uma sessão (`TestingSessionLocal`) para um banco de dados SQLite dedicado ao teste.
*   **Sobrescrita de Dependência:** A função `override_get_db` substitui a dependência `get_db` da aplicação principal, redirecionando todas as operações de banco de dados para o banco de teste.

#### 2.2. Fixtures de Setup/Teardown

O Pytest é configurado com *fixtures* para gerenciar o ciclo de vida do banco de dados de teste.

| Fixture | Escopo | Descrição |
| :--- | :--- | :--- |
| `setup_db` | `module` | **Cria** todas as tabelas no início do módulo de teste e as **remove** (`drop_all`) ao final, garantindo um ambiente limpo entre execuções de módulos. |
| `clean_db` | `function` | **Limpa** os dados (DELETE FROM) das tabelas `users`, `books` e `loans` antes da execução de **cada** teste, garantindo que os testes sejam independentes. |

#### 2.3. Função Auxiliar

A função `register_test_user` simplifica a criação de pré-condições, registrando um usuário e retornando seu **Token JWT** para uso em testes que exigem autenticação.

### 3. Casos de Teste de Integração

O arquivo contém testes que validam o fluxo completo de diferentes funcionalidades da API.

#### 3.1. Testes de Usuários (Autenticação)

| Teste | Cenário | Verificações |
| :--- | :--- | :--- |
| `test_api_login_user_full_flow_success` | Login com credenciais corretas. | *Status Code* 200, presença de `access_token` e `token_type` como `bearer`. |
| `test_api_login_user_full_flow_invalid_password` | Login com senha incorreta. | *Status Code* 401, mensagem de erro "Credenciais inválidas" no detalhe da resposta. |

#### 3.2. Testes de Livros

| Teste | Cenário | Verificações |
| :--- | :--- | :--- |
| `test_api_add_book_auth_required_unauthorized` | Cadastro de livro sem token de autenticação. | *Status Code* 401, mensagem de erro "Não autenticado". |
| `test_api_add_book_auth_required_success` | Cadastro de livro com token válido. | *Status Code* 200, título do livro correto na resposta e `owner_id` preenchido. |

#### 3.3. Testes de Empréstimos (Transacional)

| Teste | Cenário | Verificações |
| :--- | :--- | :--- |
| `test_api_request_loan_full_flow_success` | Solicitação de empréstimo bem-sucedida. | *Status Code* 200, `book_id` correto e *status* do empréstimo como `pending`. |
| `test_api_request_loan_full_flow_insufficient_points` | Solicitação de empréstimo com pontos insuficientes. | *Status Code* 400, mensagem de erro "Pontos insuficientes" no detalhe da resposta. |

### 4. Importância

Estes testes de integração são vitais para garantir que os componentes do *backend* (rotas da API, lógica de negócio e banco de dados) funcionem corretamente em conjunto, especialmente em fluxos transacionais complexos como o de empréstimos, que envolvem múltiplos usuários e a lógica de pontuação.
