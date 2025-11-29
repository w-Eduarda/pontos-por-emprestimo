// Arquivo: auth_flow.cy.js
// Testes de Interface para o fluxo de Registro e Login (Cypress)
// O Cypress simula o que o usuário faz no navegador, clicando e digitando.

describe('Fluxo de Autenticação (Registro e Login)', () => {
    
    const new_user = { email: `novo_user_${Cypress._.random(0, 1e6)}@test.com`, password: 'senhaforte' };
    const base_url = 'http://localhost:3000'; // Assumindo que o frontend está aqui

    it('Deve registrar um novo usuário e fazer login em seguida (Fluxo Completo)', () => {
        // 1. Acessar a página inicial
        cy.visit(base_url); 
        cy.get('#auth-screen').should('be.visible');

        // --- 2. Navegar para a tela de Registro (Tela 1) ---
        cy.get('#show-register-form').click();
        cy.get('#register-form').should('be.visible');
        
        // --- 3. Preencher e Submeter o Registro ---
        cy.get('#register-name').type('Novo Aluno CC');
        cy.get('#register-email').type(new_user.email);
        cy.get('#register-password').type(new_user.password);
        cy.get('#register-form button[type="submit"]').click();
        
        // Verificamos se a mensagem de sucesso ou redirecionamento para login aparece
        cy.get('#login-form').should('be.visible');
        cy.contains('Registro realizado com sucesso!').should('be.visible');
        
        // --- 4. Fazer Login (Tela 2) ---
        cy.get('#login-email').type(new_user.email);
        cy.get('#login-password').type(new_user.password);
        cy.get('#login-form button[type="submit"]').click();
        
        // --- 5. Verificação Pós-Login ---
        // O usuário deve ser redirecionado para a tela principal
        cy.get('#main-screen').should('be.visible');
        cy.get('#user-email').should('contain', new_user.email);
        cy.get('#user-points').should('contain', '50'); // Verifica se os pontos iniciais estão lá
    });
    
    it('Deve falhar ao tentar registrar com email já existente', () => {
        // 1. Acessar a página inicial
        cy.visit(base_url); 
        
        // 2. Navegar para a tela de Registro
        cy.get('#show-register-form').click();
        
        // 3. Tentar registrar com um email que já sabemos que existe (o do teste anterior)
        cy.get('#register-name').type('Aluno Duplicado');
        cy.get('#register-email').type(new_user.email);
        cy.get('#register-password').type('outrasenha');
        cy.get('#register-form button[type="submit"]').click();
        
        // 4. Verificação: Deve aparecer uma mensagem de erro
        cy.get('#modal').should('be.visible');
        cy.get('#modal-message').should('contain', 'Email já cadastrado.');
    });
});
