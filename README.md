# 🛍️ Trabalho N2: Teste de Software - Cenário Catálogo & Carrinho

## 🎯 Visão Geral do Projeto

Este projeto implementa as regras de negócio de um sistema de Catálogo e Carrinho, com foco total na aplicação de técnicas de Teste de Software (JUnit 5 / Pytest), conforme requisitos da disciplina.

O objetivo principal foi garantir a qualidade do código utilizando o ciclo TDD, implementando dobras de teste (Mocks e Stubs) para dependências externas e automatizando a verificação com Integração Contínua (CI).

---

## ⚙️ 1. Instruções de Execução

Este projeto utiliza Python e Pytest. Siga os passos abaixo para rodar os testes e gerar o relatório de cobertura.

### 1.1. Configuração do Ambiente

1.  **Clone o Repositório:**
    ```bash
    git clone https://github.com/tatilevandowski/trabalho-N2.git
    cd trabalho-N2
    ```
2.  **Crie e Ative o Ambiente Virtual (Recomendado):**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # No Windows/CMD
    # source venv/bin/activate # No Linux/Git Bash
    ```
3.  **Instale as Dependências:**
    ```bash
    pip install pytest pytest-cov pytest-mock
    ```

### 1.2. Execução dos Testes

Para rodar **todos** os testes:

```bash
pytest