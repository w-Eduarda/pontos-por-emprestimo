// Arquivo: p2p_navigation.cy.js
// Localização Sugerida: frontend/cypress/e2e/

describe('Fluxo de Login e Navegação (Teste de Interface)', () => {
    
    // Usuário de teste (deve ser registrado no backend antes de rodar o teste)
    const user = { email: 'cypress@test.com', password: 'cypresspassword' };

    // Hook para garantir que o usuário exista (simulação de pré-condição)
    before(() => {
        // Em um teste real, faríamos uma requisição POST para registrar o usuário
        // diretamente no backend para garantir um estado limpo.
        // Aqui, assumimos que o usuário 'cypress@test.com' já foi criado.
        cy.log('Assumindo que o usuário de teste já está registrado no backend.');
    });

    it('Deve fazer login e navegar corretamente entre as abas', () => {
        // 1. Acessar a página (Assumindo que o frontend está rodando em localhost:3000)
        cy.visit('http://localhost:3000'); 

        // 2. Verificar se a tela de autenticação está ativa
        cy.get('#auth-screen').should('be.visible');

        // 3. Fazer Login
        cy.get('#login-email').type(user.email);
        cy.get('#login-password').type(user.password);
        cy.get('#login-form button[type="submit"]').click();

        // 4. Verificar se a Tela Principal foi carregada
        cy.get('#main-screen').should('be.visible');
        cy.get('#user-email').should('contain', user.email);
        
        // O estudante deve saber que o valor inicial de pontos é 50 (ou 100, dependendo da regra)
        cy.get('#user-points').should('be.visible'); 

        // 5. Testar a navegação para "Meus Livros"
        cy.get('button[data-tab="my-books"]').click();
        cy.get('#my-books').should('be.visible');
        cy.get('#books-available').should('not.be.visible'); // Verifica se a aba anterior foi oculta

        // 6. Testar a navegação para "Cadastrar Livro"
        cy.get('button[data-tab="add-book"]').click();
        cy.get('#add-book').should('be.visible');
        cy.get('#my-books').should('not.be.visible');
        
        // 7. Testar a navegação para "Meus Empréstimos"
        cy.get('button[data-tab="my-loans"]').click();
        cy.get('#my-loans').should('be.visible');
        cy.get('#add-book').should('not.be.visible');
    });
    
    it('Deve exibir erro ao tentar login com credenciais inválidas', () => {
        cy.visit('http://localhost:3000'); 
        
        // Tenta login com senha errada
        cy.get('#login-email').type('cypress@test.com');
        cy.get('#login-password').type('wrongpassword');
        cy.get('#login-form button[type="submit"]').click();
        
        // Verifica se o modal de erro aparece
        cy.get('#modal').should('be.visible');
        cy.get('#modal-message').should('contain', 'Credenciais inválidas');
    });
});
