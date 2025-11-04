# Plano de Teste

## 1. Introdução
Definir estratégia, escopo, tipos de testes e responsabilidades para validação do sistema.

## 2. Itens a serem testados
- Cadastro de usuário
- Sistema de pontuação
- Empréstimo e devolução de recursos

## 3. Tipos de Testes
| Tipo | Aplicação |
|------|-----------|
| Teste Funcional | Regras de negócio do empréstimo |
| Teste de Usabilidade | Interface de usuário |
| Teste de Performance | Escalabilidade no uso |

## 4. Critérios de Aceitação
- O usuário deve conseguir emprestar um item com sucesso
- O sistema deve atualizar a pontuação corretamente

## 5. Riscos
| ID | Risco | Mitigação |
|----|-------|-----------|
| R01 | Falha na lógica de pontuação | Testes unitários obrigatórios |
