# Arquivo: locustfile_books_estudante.py
# Teste de Carga e Estresse focado nos endpoints de Livros (Books)
# Usei Locust para simular muitos usuários acessando a API ao mesmo tempo.

from locust import HttpUser, task, between
import random

# Constantes de Usuário para simulação
TEST_USER_EMAIL = "loadtest_books@p2plivros.com"
TEST_USER_PASSWORD = "loadpassword"

class P2PLivrosBooksUser(HttpUser):
    """
    Classe que define o comportamento de um usuário virtual focado em Livros.
    """
    # O tempo que o usuário "espera" entre uma ação e outra (simula um humano)
    wait_time = between(1, 3) 
    
    # Endereço base da API (onde o backend está rodando)
    host = "http://localhost:8000" 
    
    # Variáveis de estado
    token = None
    
    def on_start(self):
        """
        Função que roda quando o usuário virtual "nasce".
        Aqui a gente registra e loga o usuário para ter o token.
        """
        # 1. Tenta registrar o usuário (para garantir que exista)
        self.client.post("/api/users/register", json={
            "name": "Load Test Books User",
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
            # Se o login falhar, o usuário não faz mais nada
            self.environment.runner.quit() 

    @task(5) # Prioridade 5 (a mais frequente)
    def list_books(self):
        """
        Simula a listagem de livros disponíveis (GET /api/books/).
        Essa é a operação mais comum, então tem prioridade maior.
        """
        self.client.get("/api/books/", name="/api/books/ (GET Listar Livros)")

    @task(1) # Prioridade 1 (menos frequente)
    def add_book(self):
        """
        Simula o cadastro de um novo livro (POST /api/books/).
        Essa operação é mais pesada e menos frequente.
        """
        if self.token:
            book_data = {
                "title": f"Livro de Teste {random.randint(1, 10000)}",
                "author": "Load Test",
                "points": random.randint(5, 20)
            }
            self.client.post("/api/books/", json=book_data, name="/api/books/ (POST Cadastrar Livro)")

# --- Como Executar o Teste de Carga e Estresse ---
# 1. Instalar o Locust: pip install locust
# 2. Iniciar o backend: uvicorn main:app --reload --port 8000
# 3. Executar o Locust: locust -f locustfile_books_estudante.py
# 4. Abrir o navegador em http://localhost:8089 e configurar a carga.
#
# **Diferença entre Carga e Estresse:**
# - **Teste de Carga:** A gente configura um número de usuários (ex: 50) que o sistema DEVE suportar. O objetivo é ver se ele aguenta a carga esperada.
# - **Teste de Estresse:** A gente configura um número de usuários MUITO ALTO (ex: 500 ou 1000) para forçar o sistema até ele quebrar. O objetivo é achar o limite máximo e ver como ele se comporta na falha.
