# Documentação do Módulo de Teste de Estresse (Locust)

## Conceito e Objetivo

O **Teste de Estresse** é uma variação do Teste de Carga que tem como objetivo levar o sistema a condições extremas, muito além do seu volume de tráfego esperado, para determinar o seu **ponto de ruptura**.

O principal objetivo é:
1.  **Identificar a Capacidade Máxima:** Determinar o número máximo de usuários ou transações que o sistema pode suportar antes de falhar.
2.  **Avaliar a Estabilidade:** Verificar como o sistema se comporta sob sobrecarga (ex: se ele falha de forma graciosa ou se trava completamente).
3.  **Medir a Recuperação:** Analisar o tempo e a forma como o sistema se recupera após a remoção da carga excessiva (*resilience*).

## Ferramenta Utilizada

A ferramenta utilizada é o **Locust** (Python), a mesma usada para o Teste de Carga. A diferença entre os dois tipos de teste reside na **configuração da carga** e na **análise dos resultados**.

| Teste | Foco | Configuração da Carga | Métrica Chave |
| :--- | :--- | :--- | :--- |
| **Carga** | Desempenho sob volume normal. | Número de usuários igual ou ligeiramente superior ao esperado. | Tempo de Resposta (P95) |
| **Estresse** | Ponto de Ruptura e Estabilidade. | Aumento gradual e contínuo do número de usuários até a falha. | Taxa de Falha (%) |

## Lista de Testes Previstos

Os testes de estresse são definidos pela estratégia de aumento de carga:

1.  **Aumento Gradual de Carga (*Ramp-up*):** Aumentar o número de usuários virtuais (VUs) e a taxa de eclosão (*hatch rate*) de forma contínua (ex: 50 VUs a cada 5 minutos) até que a taxa de erro atinja um limite pré-definido (ex: 5% ou 10%).
2.  **Teste de Pico:** Aplicar uma carga máxima repentina (ex: 1000 VUs imediatamente) para simular um evento inesperado e verificar a degradação imediata do serviço.

## Exemplo de Resultados (Gráfico)

O resultado mais importante do teste de estresse é o gráfico que relaciona a **Taxa de Falha** ou o **Tempo de Resposta** com o **Número de Usuários Concorrentes**.

*   **Cenário:** Teste de estresse na rota de Login (`/api/users/login`).
*   **Análise:** O gráfico deve mostrar que, à medida que o número de usuários aumenta, o tempo de resposta se mantém estável até um certo ponto (o limite de capacidade). A partir desse ponto, o tempo de resposta aumenta exponencialmente e a taxa de falha (erros 5xx) começa a subir, indicando o **ponto de ruptura**.

| Métrica | Comportamento no Estresse |
| :--- | :--- |
| **Tempo de Resposta** | Aumenta drasticamente após o limite de capacidade. |
| **Taxa de Falha** | Permanece em 0% e sobe abruptamente no ponto de ruptura. |
| **Taxa de Requisições (RPS)** | Atinge um pico e, em seguida, começa a cair, mesmo com o aumento de usuários, pois o sistema está saturado. |

## Código de Exemplo (Locustfile)

O código para o teste de estresse é o mesmo utilizado para o teste de carga (`test_load.py`), pois o Locust permite que a estratégia de estresse (o número de usuários e a taxa de eclosão) seja configurada diretamente na interface web ou via linha de comando, sem alterar o código da classe `HttpUser`.

O arquivo `stress_test_locustfile.py` (anexado) define os comportamentos que serão estressados. A execução do estresse é feita com comandos como:

```bash
# Exemplo de execução para estresse (configurado para 1000 usuários)
locust -f stress_test_locustfile.py --headless -u 1000 -r 100 --run-time 30m
```
