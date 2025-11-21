// Configuração da API
const API_URL = 'https://8000-i06glrurotzdp8ekxx7ds-5f7454b1.manusvm.computer/api'; // URL do backend exposto

// Estado da aplicação
let currentUser = null;
let token = null;

// Elementos do DOM
const authScreen = document.getElementById('auth-screen');
const mainScreen = document.getElementById('main-screen');
const modal = document.getElementById('modal');
const modalMessage = document.getElementById('modal-message');
const modalClose = document.getElementById('modal-close');

// ==================== FUNÇÕES AUXILIARES ====================

function showModal(message) {
    modalMessage.innerHTML = message;
    modal.classList.add('active');
}

function closeModal() {
    modal.classList.remove('active');
}

function switchScreen(screen) {
    authScreen.classList.remove('active');
    mainScreen.classList.remove('active');
    
    if (screen === 'auth') {
        authScreen.classList.add('active');
        document.getElementById('login-form').classList.remove('hidden');
        document.getElementById('register-form').classList.add('hidden');
    } else if (screen === 'main') {
        mainScreen.classList.add('active');
        switchTab('books-available');
    }
}

function switchTab(tabId) {
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    
    document.querySelector(`[data-tab="${tabId}"]`).classList.add('active');
    document.getElementById(tabId).classList.add('active');
    
    if (tabId === 'books-available') {
        loadAvailableBooks();
    } else if (tabId === 'my-books') {
        loadMyBooks();
    } else if (tabId === 'my-loans') {
        loadMyLoans();
    }
}

async function updatePoints() {
    // A API não tem um endpoint /users/me, então vamos simular a atualização
    // Em um projeto real, buscaríamos o usuário atualizado aqui.
    document.getElementById('user-points').textContent = currentUser.points;
}

// Função para tratar respostas da API
async function handleResponse(response) {
    const data = await response.json();
    if (!response.ok) {
        // Tenta extrair a mensagem de erro de diferentes formatos
        let errorMessage = 'Erro desconhecido';
        
        if (typeof data.detail === 'string') {
            errorMessage = data.detail;
        } else if (Array.isArray(data.detail)) {
            // Formatar erros de validação do FastAPI
            errorMessage = data.detail.map(err => `${err.loc.join(' > ')}: ${err.msg}`).join(', ');
        } else if (data.detail && data.detail.msg) {
            errorMessage = data.detail.msg;
        } else {
            errorMessage = JSON.stringify(data);
        }
        
        throw new Error(errorMessage);
    }
    return data;
}

// ==================== AUTENTICAÇÃO ====================

document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    
    try {
        const response = await fetch(`${API_URL}/users/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        
        const data = await handleResponse(response);
        
        token = data.access_token;
        // Decodificar o token para obter o ID do usuário
        const payload = JSON.parse(atob(token.split('.')[1]));
        
        // Simulação de pontos: O backend não retorna pontos no login, então assumimos 100
        // e o ID do usuário é o 'sub' do token.
        currentUser = { id: payload.sub, email: email, points: 100 }; 
        
        document.getElementById('user-email').textContent = currentUser.email;
        updatePoints();
        switchScreen('main');
    } catch (error) {
        console.error('Erro de Login:', error);
        showModal(`Falha no Login: ${error.message}`);
    }
});

document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const name = document.getElementById('register-name').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    
    try {
        const response = await fetch(`${API_URL}/users/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, password })
        });
        
        await handleResponse(response);
        
        showModal('Cadastro realizado com sucesso! Faça login para continuar.');
        document.getElementById('register-form').reset();
        switchScreen('auth');
    } catch (error) {
        console.error('Erro de Cadastro:', error);
        showModal(`Falha no Cadastro: ${error.message}`);
    }
});

document.getElementById('logout-btn').addEventListener('click', () => {
    currentUser = null;
    token = null;
    switchScreen('auth');
});

// ==================== LIVROS ====================

async function loadAvailableBooks() {
    try {
        const response = await fetch(`${API_URL}/books/`);
        const books = await handleResponse(response);
        
        const container = document.getElementById('books-list');
        container.innerHTML = ''; // Limpa o container
        
        if (books.length === 0) {
            container.innerHTML = '<p class="empty-message">Nenhum livro disponível no momento.</p>';
            return;
        }
        
        books.forEach(book => {
            const isOwner = book.owner_id === currentUser.id;
            const isAvailable = book.available;
            
            const card = document.createElement('div');
            card.className = 'book-card';
            card.innerHTML = `
                <h3>${book.title}</h3>
                <p><strong>Autor:</strong> ${book.author}</p>
                ${book.description ? `<p>${book.description}</p>` : ''}
                <p><strong>Proprietário:</strong> ${isOwner ? 'Você' : book.owner_id}</p>
                <div class="book-points">⭐ ${book.points_required} pontos</div>
                <button class="btn-primary" 
                    onclick="requestLoan(${book.id}, ${book.points_required})" 
                    ${isOwner || !isAvailable ? 'disabled' : ''}>
                    ${isOwner ? 'Seu Livro' : (!isAvailable ? 'Emprestado' : 'Pegar Emprestado')}
                </button>
            `;
            container.appendChild(card);
        });
    } catch (error) {
        console.error('Erro ao carregar livros:', error);
        showModal(`Erro ao carregar livros disponíveis: ${error.message}`);
    }
}

async function loadMyBooks() {
    try {
        const response = await fetch(`${API_URL}/books/`);
        const books = await handleResponse(response);
        const myBooks = books.filter(book => book.owner_id === currentUser.id);
        
        const container = document.getElementById('my-books-list');
        container.innerHTML = ''; // Limpa o container
        
        if (myBooks.length === 0) {
            container.innerHTML = '<p class="empty-message">Você ainda não cadastrou nenhum livro.</p>';
            return;
        }
        
        myBooks.forEach(book => {
            const card = document.createElement('div');
            card.className = 'book-card';
            card.innerHTML = `
                <h3>${book.title}</h3>
                <p><strong>Autor:</strong> ${book.author}</p>
                ${book.description ? `<p>${book.description}</p>` : ''}
                <div class="book-points">⭐ ${book.points_required} pontos</div>
                <p><strong>Status:</strong> ${book.available ? '✅ Disponível' : '🔒 Emprestado'}</p>
            `;
            container.appendChild(card);
        });
    } catch (error) {
        console.error('Erro ao carregar meus livros:', error);
        showModal(`Erro ao carregar seus livros: ${error.message}`);
    }
}

document.getElementById('form-add-book').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const title = document.getElementById('book-title').value;
    const author = document.getElementById('book-author').value;
    const description = document.getElementById('book-description').value;
    const points_required = parseInt(document.getElementById('book-points').value);
    
    try {
        const response = await fetch(`${API_URL}/books/`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                title,
                author,
                description,
                points_required
            })
        });
        
        await handleResponse(response);
        
        showModal('Livro cadastrado com sucesso!');
        document.getElementById('form-add-book').reset();
        switchTab('my-books');
    } catch (error) {
        console.error('Erro ao cadastrar livro:', error);
        showModal(`Falha ao cadastrar livro: ${error.message}`);
    }
});

// ==================== EMPRÉSTIMOS ====================

async function requestLoan(bookId, pointsRequired) {
    if (currentUser.points < pointsRequired) {
        showModal(`Você não tem pontos suficientes. Necessário: ${pointsRequired} pontos.`);
        return;
    }
    
    if (!confirm(`Deseja pegar este livro emprestado por ${pointsRequired} pontos?`)) {
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/loans/request`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ book_id: bookId })
        });
        
        await handleResponse(response);
        
        showModal('Empréstimo solicitado com sucesso! Seu saldo será atualizado após a confirmação.');
        // Simular dedução de pontos (o backend deve fazer isso, mas simulamos para feedback imediato)
        currentUser.points -= pointsRequired;
        updatePoints();
        loadAvailableBooks();
    } catch (error) {
        console.error('Erro ao solicitar empréstimo:', error);
        showModal(`Falha ao solicitar empréstimo: ${error.message}`);
    }
}

async function returnLoan(loanId) {
    if (!confirm('Tem certeza que deseja devolver este livro?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/loans/${loanId}/return`, {
            method: 'POST',
            headers: { 
                'Authorization': `Bearer ${token}`
            }
        });
        
        await handleResponse(response);
        
        showModal('Livro devolvido com sucesso! Seu saldo de pontos será reajustado.');
        loadMyLoans();
        loadAvailableBooks();
    } catch (error) {
        console.error('Erro ao devolver livro:', error);
        showModal(`Falha ao devolver livro: ${error.message}`);
    }
}

async function loadMyLoans() {
    try {
        const response = await fetch(`${API_URL}/loans/my_loans`, {
            headers: { 
                'Authorization': `Bearer ${token}`
            }
        });
        
        const loans = await handleResponse(response);
        
        const container = document.getElementById('loans-list');
        container.innerHTML = ''; // Limpa o container
        
        if (loans.length === 0) {
            container.innerHTML = '<p class="empty-message">Você não possui empréstimos ativos ou no histórico.</p>';
            return;
        }
        
        loans.forEach(loan => {
            const card = document.createElement('div');
            card.className = 'book-card';
            
            // Simulação de status
            let statusText = '';
            let button = '';
            
            if (loan.status === 'active') {
                statusText = 'Empréstimo Ativo';
                button = `<button class="btn-secondary" onclick="returnLoan(${loan.id})">Devolver Livro</button>`;
            } else if (loan.status === 'returned') {
                statusText = 'Devolvido';
            } else if (loan.status === 'requested') {
                statusText = 'Pendente de Confirmação';
            }

            card.innerHTML = `
                <h3>Livro ID: ${loan.book_id}</h3>
                <p><strong>Status:</strong> ${statusText}</p>
                <p><strong>Data de Início:</strong> ${loan.start_date || 'N/A'}</p>
                <p><strong>Data de Devolução:</strong> ${loan.due_date || 'N/A'}</p>
                ${button}
            `;
            container.appendChild(card);
        });
    } catch (error) {
        console.error('Erro ao carregar empréstimos:', error);
        showModal(`Falha ao carregar empréstimos: ${error.message}`);
    }
}

// ==================== EVENT LISTENERS ====================

document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const tabId = btn.getAttribute('data-tab');
        switchTab(tabId);
    });
});

modalClose.addEventListener('click', closeModal);

modal.addEventListener('click', (e) => {
    if (e.target === modal) {
        closeModal();
    }
});

// ==================== INICIALIZAÇÃO ====================

switchScreen('auth');
