# Arquivo: locustfile.py
# Localização Sugerida: Fora da pasta de testes, na raiz do backend, ou em uma pasta dedicada.

from locust import HttpUser, task, between
import random

# Constantes de Usuário para simulação
TEST_USER_EMAIL = "loadtest@p2plivros.com"
TEST_USER_PASSWORD = "loadpassword"

class P2PLivrosUser(HttpUser):
    """
    Classe que define o comportamento de um usuário virtual no sistema P2P Livros.
    """
    # Tempo de espera entre as tarefas (em segundos)
    wait_time = between(1, 2.5) 
    
    # Endereço base da API (deve ser ajustado para o ambiente de teste)
    host = "http://localhost:8000" 
    
    # Variáveis de estado
    token = None
    
    def on_start(self):
        """
        Método executado no início da vida de cada usuário virtual.
        Usado para simular o login e obter o token de autenticação.
        """
        # 1. Tenta registrar o usuário (para garantir que exista)
        self.client.post("/api/users/register", json={
            "name": "Load Test User",
            "email": TEST_USER_EMAIL,
            "password": TEST_USER_PASSWORD
        }, name="/api/users/register (Setup)")
        
        # 2. Realiza o Login
        response = self.client.post("/api/users/login", json={
            "email": TEST_USER_EMAIL,
            "password": TEST_USER_PASSWORD
        }, name="/api/users/login")
        
        if response.status_code == 200:
            self.token = response.json().get("access_token")
            self.client.headers = {"Authorization": f"Bearer {self.token}"}
        else:
            # Se o login falhar, o usuário não fará mais nada
            self.environment.runner.quit() 

    @task(3) # Prioridade 3 (mais frequente)
    def list_books(self):
        """
        Simula a listagem de livros disponíveis (operação de leitura mais comum).
        """
        self.client.get("/api/books/", name="/api/books/ (Listar)")

    @task(1) # Prioridade 1 (menos frequente)
    def add_book(self):
        """
        Simula o cadastro de um novo livro (operação de escrita).
        """
        if self.token:
            book_data = {
                "title": f"Livro de Teste {random.randint(1, 10000)}",
                "author": "Load Test",
                "points": random.randint(5, 20)
            }
            self.client.post("/api/books/", json=book_data, name="/api/books/ (Cadastrar)")

    @task(1) # Prioridade 1 (menos frequente)
    def request_loan(self):
        """
        Simula a solicitação de um empréstimo (operação transacional).
        """
        if self.token:
            # Simulação simplificada: tenta solicitar um livro com ID aleatório
            # Em um teste real, seria necessário listar os IDs disponíveis primeiro.
            random_book_id = random.randint(1, 50) 
            self.client.post("/api/loans/request", json={"book_id": random_book_id}, name="/api/loans/request")

# --- Como Executar o Teste de Carga ---
# 1. Instalar o Locust: pip install locust
# 2. Iniciar o backend: uvicorn main:app --reload --port 8000
# 3. Executar o Locust: locust -f locustfile.py
# 4. Abrir o navegador em http://localhost:8089 e configurar a carga.
