# Documentação do Módulo de Teste de Interface (Cypress)

## Arquivo: `test_interface.js`

Este documento detalha o arquivo de teste de ponta a ponta (E2E) `test_interface.js`, escrito em JavaScript utilizando a *framework* **Cypress**. O objetivo principal deste módulo é simular o fluxo de usuário no *frontend* da aplicação P2P Livros, garantindo que as funcionalidades de **login** e **navegação entre abas** estejam operacionais.

### 1. Visão Geral

| Característica | Detalhe |
| :--- | :--- |
| **Tecnologia** | Cypress (JavaScript) |
| **Tipo de Teste** | Teste de Ponta a Ponta (E2E) |
| **Funcionalidade Testada** | Fluxo de Login e Navegação Principal |
| **Pré-requisitos** | Aplicação *frontend* rodando em `http://localhost:3000` e um usuário de teste (`cypress@test.com`) registrado no *backend*. |

### 2. Estrutura do Código

O arquivo é estruturado em um bloco `describe` que agrupa os testes relacionados ao "Fluxo de Login e Navegação".

#### 2.1. Configuração (`before` Hook)

O *hook* `before` é utilizado para configurar o ambiente antes da execução dos testes. Neste caso, ele assume que o usuário de teste (`cypress@test.com` com a senha `cypresspassword`) já está registrado no *backend*.

```javascript
before(() => {
    // ...
    cy.log('Assumindo que o usuário de teste já está registrado no backend.');
});
```

#### 2.2. Caso de Teste: Login e Navegação Bem-Sucedidos

O teste `it('Deve fazer login e navegar corretamente entre as abas')` valida o fluxo principal da aplicação após o login.

| Passo | Ação | Verificação |
| :--- | :--- | :--- |
| **1. Acesso** | `cy.visit('http://localhost:3000')` | Acessa a URL base do *frontend*. |
| **2. Login** | Preenche os campos de e-mail (`#login-email`) e senha (`#login-password`) e clica no botão de *submit*. | A tela de autenticação (`#auth-screen`) deve estar visível antes do login. |
| **3. Tela Principal** | N/A | A tela principal (`#main-screen`) deve estar visível, e o e-mail do usuário (`#user-email`) e a pontuação (`#user-points`) devem ser exibidos. |
| **4. Navegação** | Clica sequencialmente nos botões de navegação (`data-tab="my-books"`, `data-tab="add-book"`, `data-tab="my-loans"`). | A aba correspondente deve se tornar visível (ex: `#my-books`), e a aba anterior deve ser ocultada (`not.be.visible`). |

#### 2.3. Caso de Teste: Login com Credenciais Inválidas

O teste `it('Deve exibir erro ao tentar login com credenciais inválidas')` verifica o tratamento de erro na autenticação.

| Passo | Ação | Verificação |
| :--- | :--- | :--- |
| **1. Acesso** | `cy.visit('http://localhost:3000')` | Acessa a URL base. |
| **2. Login Inválido** | Tenta fazer login com uma senha incorreta (`wrongpassword`). | O *status* de erro deve ser tratado, e um modal de erro (`#modal`) deve aparecer, contendo a mensagem "Credenciais inválidas" (`#modal-message`). |

### 3. Melhores Práticas e Observações

*   **Isolamento de Teste:** O Cypress garante que cada teste seja isolado, mas a pré-condição de registro do usuário é crucial para a estabilidade.
*   **Seletores:** O código utiliza seletores de ID (`#login-email`, `#main-screen`) e atributos (`button[data-tab="my-books"]`), que são considerados boas práticas para testes de interface, pois são menos propensos a quebrar do que seletores baseados em classes CSS.
*   **Simulação de Estado:** A simulação de login e navegação é um teste de fumaça essencial para a saúde da aplicação *frontend*.
