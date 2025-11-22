# Documentação do Módulo de Teste de Carga (Locust)

## Arquivo: `test_load.py`

Este documento descreve o arquivo `test_load.py`, que atua como um *Locustfile* para a realização de **Testes de Carga (Load Testing)** na API *backend* da aplicação P2P Livros. O objetivo é simular o comportamento de múltiplos usuários concorrentes para avaliar a performance, estabilidade e escalabilidade do sistema sob estresse.

### 1. Visão Geral

| Característica | Detalhe |
| :--- | :--- |
| **Tecnologia** | Locust (Python) |
| **Tipo de Teste** | Teste de Carga (Load Testing) |
| **Funcionalidade Testada** | API *backend* (Login, Listagem de Livros, Cadastro de Livros, Solicitação de Empréstimos) |
| **Pré-requisitos** | Servidor *backend* rodando (ex: `http://localhost:8000`), Locust instalado (`pip install locust`). |

### 2. Estrutura da Classe `P2PLivrosUser`

A classe `P2PLivrosUser` herda de `HttpUser` do Locust e define o comportamento do usuário virtual.

#### 2.1. Configurações

*   **`wait_time = between(1, 2.5)`:** Define um tempo de espera aleatório entre 1 e 2.5 segundos entre a execução de cada tarefa, simulando um comportamento humano mais realista.
*   **`host = "http://localhost:8000"`:** O endereço base da API a ser testada.
*   **`TEST_USER_EMAIL` / `TEST_USER_PASSWORD`:** Credenciais fixas para o usuário de teste de carga.

#### 2.2. Inicialização (`on_start`)

O método `on_start` é executado uma única vez por usuário virtual no início. Ele é crucial para estabelecer o estado de autenticação.

1.  **Registro (Setup):** Tenta registrar o usuário de teste (`/api/users/register`) para garantir que ele exista no banco de dados.
2.  **Login:** Realiza o login (`/api/users/login`) para obter o **Token JWT**.
3.  **Autenticação:** Se o login for bem-sucedido, o token é armazenado na variável de estado `self.token` e adicionado ao cabeçalho `Authorization` de todas as requisições subsequentes.

#### 2.3. Tarefas de Carga (`@task`)

As tarefas definem as ações que os usuários virtuais executarão repetidamente. O decorador `@task(peso)` define a frequência relativa de cada tarefa.

| Tarefa | Endpoint | Peso | Descrição |
| :--- | :--- | :--- | :--- |
| `list_books` | `/api/books/` (GET) | 3 | **Leitura Frequente:** Simula a listagem de livros disponíveis. É a tarefa mais comum. |
| `add_book` | `/api/books/` (POST) | 1 | **Escrita:** Simula o cadastro de um novo livro, utilizando dados aleatórios para evitar colisões. Requer autenticação (`self.token`). |
| `request_loan` | `/api/loans/request` (POST) | 1 | **Transacional:** Simula a solicitação de um empréstimo, utilizando um `book_id` aleatório. Requer autenticação. |

### 3. Execução do Teste de Carga

O arquivo inclui instruções claras para a execução do teste:

1.  Instalar o Locust: `pip install locust`
2.  Iniciar o *backend*: `uvicorn main:app --reload --port 8000`
3.  Executar o Locust: `locust -f locustfile.py`
4.  Acessar a interface web para configuração: `http://localhost:8089`
