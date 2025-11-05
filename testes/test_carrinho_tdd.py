# src/tests/test_carrinho_tdd.py

import pytest
from src.carrinho import Carrinho
from src.fatura import Fatura
from src.exceptions import CupomInvalidoError, PagamentoRecusadoError, QuantidadeInvalidaError, EstoqueInsuficienteError
from unittest.mock import MagicMock
from servico_email import enviar_confirmacao # Importando a função real para o patch

# --- TDD: Promocao Progressiva (15% de desconto) ---

# TDD FASE RED (Testar a regra de 15% antes de implementá-la no Carrinho)
def test_calculo_total_com_promocao_progressiva_desconto_15_porcento(produto_padrao, mock_estoque_repo):
    """
    Novo requisito (TDD): Mais de 10 unidades = 15% de desconto.
    Produto: R$100.00
    Quantidade: 10
    Esperado: (10 * 100) * (1 - 0.15) = R$850.00
    """
    carrinho = Carrinho(estoque_repo=mock_estoque_repo)
    carrinho.adicionar_item(produto_padrao, 10) # 10 unidades
    
    total = carrinho.calcular_total()
    
    assert total == 850.00

# --- Parametrizados (Item 4) ---

@pytest.mark.parametrize(
    "quantidade, desconto_esperado",
    [
        (1, 0.0),      # Sem desconto
        (4, 0.0),      # Sem desconto
        (5, 0.10),     # 10% de desconto
        (9, 0.10),     # 10% de desconto
        (10, 0.15),    # 15% de desconto
        (15, 0.15),    # 15% de desconto
    ]
)

def test_promocao_progressiva_parametrizada(produto_padrao, mocker, quantidade, desconto_esperado):
    """
    Testa se a regra de desconto progressiva (0%, 10%, 15%) está correta 
    para diferentes quantidades (Item 4).
    """
    # CRIA UM MOCK LOCAL QUE SEMPRE TERÁ ESTOQUE SUFICIENTE
    local_mock_estoque = mocker.Mock()
    local_mock_estoque.consultar_quantidade.return_value = quantidade + 1 
    local_mock_estoque.reservar.return_value = None
    
    # Usa o mock local no carrinho
    carrinho = Carrinho(estoque_repo=local_mock_estoque) 
    
    preco_unitario = produto_padrao.preco # 2000.00
    
    carrinho.adicionar_item(produto_padrao, quantidade)
    
    total_esperado = (quantidade * preco_unitario) * (1 - desconto_esperado)
    
    assert carrinho.calcular_total() == round(total_esperado, 2)


# --- Testes de Exceção (Item 3) ---

def test_adicionar_item_quantidade_zero_ou_negativa_levanta_excecao(produto_padrao, mock_estoque_repo):
    """
    Testa se o Carrinho levanta QuantidadeInvalidaError para quantidades <= 0 (Item 3).
    """
    carrinho = Carrinho(estoque_repo=mock_estoque_repo)
    
    with pytest.raises(QuantidadeInvalidaError) as excinfo:
        carrinho.adicionar_item(produto_padrao, 0) # Teste com zero
        
    assert "quantidade do produto deve ser positiva" in str(excinfo.value)
    
    with pytest.raises(QuantidadeInvalidaError):
        carrinho.adicionar_item(produto_padrao, -1) # Teste com negativo



# --- Stubs & Mocks (Itens 4, 5) ---

# Teste que verifica a chamada ao Stub de E-mail (Item 5)
def test_finalizar_compra_chama_stub_email_ao_aprovar(produto_padrao, mocker):
    """
    Testa se a função de e-mail é chamada após um pagamento APROVADO.
    (Stub de e-mail)
    """
    # 1. Preparação: Mock para todas as dependências
    mock_estoque_repo = mocker.Mock()
    mock_frete_api = mocker.Mock()
    mock_frete_api.calcular_frete.return_value = 0.0 
    mock_gateway = mocker.Mock()
    mock_gateway.processar_pagamento.return_value = {"status": "APROVADO"}
    repo_fatura_memoria = mocker.Mock()
    
    # 2. Patch do Serviço de E-mail (Substitui a função real por um Mock)
    # A variável 'mock_email_service' AGORA É um Mock
    mock_email_service = mocker.patch('servico_email.enviar_confirmacao') 
    
    # 3. Cenário
    carrinho = Carrinho(estoque_repo=mock_estoque_repo, frete_api=mock_frete_api, 
                        gateway_pagamento=mock_gateway)
    carrinho.adicionar_item(produto_padrao, 1)

    
    # O método finalizar_compra agora exige o servico_email como argumento
    fatura = carrinho.finalizar_compra(dados_pagamento={}, repo_fatura=repo_fatura_memoria, 
                                       servico_email=mock_email_service) 
    
    # Verifica se o Stub de E-mail foi chamado EXATAMENTE UMA VEZ com a Fatura gerada.
    mock_email_service.assert_called_once_with(fatura)

def test_adicionar_item_sem_estoque_levanta_excecao(produto_padrao, mocker):
    """
    Testa se o Carrinho levanta EstoqueInsuficienteError quando o estoque é baixo.
    (Exige a implementação da consulta ao Stub no Carrinho)
    """
    # 1. Setup: Mock para o Estoque Repository (Stub)
    mock_estoque_repo = mocker.Mock()
    # Força o Stub a retornar uma quantidade baixa
    mock_estoque_repo.consultar_quantidade.return_value = 2 # Apenas 2 disponíveis
    
    # Mocks para o Carrinho (para o construtor)
    mock_frete = mocker.Mock()
    mock_gateway = mocker.Mock()
    
    carrinho = Carrinho(estoque_repo=mock_estoque_repo, frete_api=mock_frete, 
                        gateway_pagamento=mock_gateway)

    # 2. Ação e Assertiva: Tenta adicionar 3 itens (que é > 2)
    with pytest.raises(EstoqueInsuficienteError) as excinfo:
        carrinho.adicionar_item(produto_padrao, 3) 
    
    # 3. Verificação: Confirma se a RESERVA NÃO foi chamada
    mock_estoque_repo.reservar.assert_not_called()
    
    assert "Estoque insuficiente" in str(excinfo.value)