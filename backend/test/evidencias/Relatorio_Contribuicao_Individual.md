# Relatório de Contribuição - Testes de Software 

A ideia foi garantir que os testes fossem **diferentes** dos que já estavam no repositório, focando em outros módulos e fluxos.

## 1. Testes Unitários (Pytest)

Foquei em isolar a lógica de negócio de dois módulos, usando `Pytest` e `unittest.mock` para simular as dependências (tipo o banco de dados).

| Componente Testado | Arquivo de Teste | O que foi testado? |
| :--- | :--- | :--- |
| **Book Service** (`services/book_service.py`) | `test_unit_book_service_estudante.py` | Testei se o cadastro de livro funciona (o famoso "happy path") e, mais importante, se ele **bloqueia** o cadastro de livros com pontos negativos (regra de negócio!). |
| **Notifications Utility** (`utils/notifications.py`) | `test_unit_notifications_estudante.py` | Testei se a função de notificação **chama** o serviço de e-mail corretamente, garantindo que o dono do livro seja avisado quando alguém solicita um empréstimo. |

## 2. Testes de API (GET e POST)

Usei o `FastAPI TestClient` (que é tipo um Postman dentro do código) para testar os endpoints de Livros (`/api/books`), focando na validação dos status HTTP.

| Requisição Testada | Endpoint | Arquivo de Teste | O que foi testado? |
| :--- | :--- | :--- | :--- |
| **POST** | `/api/books/` | `test_api_books_estudante.py` | Testei o cadastro de um novo livro, verificando se o status de retorno é `200 OK` e se o livro aparece na resposta. |
| **GET** | `/api/books/` | `test_api_books_estudante.py` | Testei a listagem de livros, verificando se o status é `200 OK` e se a lista retornada contém os livros cadastrados. |

## 3. Testes de Carga e Estresse (Locust)

Criei um script `Locust` para simular muitos usuários acessando a API de Livros.

| Tipo de Teste | Arquivo de Teste | Endpoints Focados | Objetivo |
| :--- | :--- | :--- | :--- |
| **Carga e Estresse** | `locustfile_books_estudante.py` | `GET /api/books/` e `POST /api/books/` | **Carga:** Verificar se o sistema aguenta a quantidade de usuários esperada (ex: 50 usuários). **Estresse:** Aumentar a carga (ex: 500 usuários) até o sistema começar a falhar, para descobrir o limite dele. |

**Gráficos das Métricas de Desempenho:**

O `Locust` gera relatórios e gráficos (latência, taxa de falhas, etc.) automaticamente na sua interface web (`http://localhost:8089`) quando o teste é executado.

## 4. Testes de Interface (Cypress)

Usei o `Cypress` (que é bem mais moderno que o Robot Framework) para simular o fluxo do usuário no frontend.

| Tela/Página Testada | Arquivo de Teste | O que foi testado? |
| :--- | :--- | :--- |
| **Registro** (Tela 1) | `test_interface_auth_estudante.js` | Testamos o fluxo completo de **Registro** de um novo usuário, verificando se ele é redirecionado para o login. |
| **Login** (Tela 2) | `test_interface_auth_estudante.js` | Testamos o **Login** com o usuário recém-criado, verificando se ele entra na tela principal e se os pontos iniciais (50) são exibidos. |

Todos os arquivos de teste estão na pasta `backend/test/casos_testes/` e este relatório está em `backend/test/evidencias/`. Espero que ajude! Qualquer dúvida, é só chamar!
