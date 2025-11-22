# Arquivo: stress_test_locustfile.py
# Este arquivo é o mesmo locustfile usado para o teste de carga,
# mas a estratégia de estresse (número de usuários e taxa de eclosão)
# é definida na interface web do Locust ou via linha de comando.

from locust import HttpUser, task, between
import random

# Constantes de Usuário para simulação
TEST_USER_EMAIL = "stresstest@p2plivros.com"
TEST_USER_PASSWORD = "stresspassword"

class P2PLivrosStressUser(HttpUser):
    """
    Classe que define o comportamento de um usuário virtual para o Teste de Estresse.
    O comportamento é o mesmo do teste de carga, mas será executado sob alta concorrência.
    """
    # Tempo de espera entre as tarefas (em segundos)
    wait_time = between(0.5, 1.5) # Reduzido para simular usuários mais ativos
    
    # Endereço base da API (deve ser ajustado para o ambiente de teste)
    host = "http://localhost:8000" 
    
    # Variáveis de estado
    token = None
    
    def on_start(self):
        """
        Método executado no início da vida de cada usuário virtual.
        Simula o login e obtém o token de autenticação.
        """
        # 1. Tenta registrar o usuário (para garantir que exista)
        self.client.post("/api/users/register", json={
            "name": "Stress Test User",
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

    @task(5) # Prioridade 5 (mais frequente) - Aumentado para estressar mais o sistema
    def list_books(self):
        """
        Simula a listagem de livros disponíveis (operação de leitura mais comum).
        """
        self.client.get("/api/books/", name="/api/books/ (Listar)")

    @task(2) # Prioridade 2 (menos frequente)
    def add_book(self):
        """
        Simula o cadastro de um novo livro (operação de escrita).
        """
        if self.token:
            book_data = {
                "title": f"Livro de Estresse {random.randint(1, 100000)}",
                "author": "Stress Test",
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
            random_book_id = random.randint(1, 50) 
            self.client.post("/api/loans/request", json={"book_id": random_book_id}, name="/api/loans/request")

# --- Como Executar o Teste de Estresse ---
# 1. Instalar o Locust: pip install locust
# 2. Iniciar o backend: uvicorn main:app --reload --port 8000
# 3. Executar o Locust e configurar uma carga alta (ex: 1000 usuários) na interface web
#    ou via linha de comando:
#    locust -f stress_test_locustfile.py
# 4. Abrir o navegador em http://localhost:8089 e configurar a carga para estresse.
#    Exemplo de configuração: Usuários: 1000, Taxa de Eclosão: 100
