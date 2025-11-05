# src/tests/test_integracao.py

import pytest
from src.carrinho import Carrinho 
from src.produto import Produto 
from src.estoque import EstoqueRepository
from src.repositorio_fatura import InMemoryFaturaRepository
from src.frete_api import FreteAPI
from src.fatura import Fatura

# Importa o módulo real para o patch do e-mail
import src.servico_email 

# Usando o decorador 'mocker' do pytest-mock
def test_fluxo_compra_completo_integracao(mocker):
    """
    Testa o fluxo completo de compra: Adicionar -> Reservar -> Frete -> Pagar -> Salvar Fatura -> Enviar Email.
    Usa repositório em memória e mocks para todos os serviços externos. (Item 6)
    """
    # --- 1. SETUP DE DEPENDÊNCIAS ---
    
    # Repositório em Memória (Implementação leve)
    repo_fatura = InMemoryFaturaRepository()
    
    # Mocks para serviços externos
    mock_estoque_repo = mocker.Mock(spec=EstoqueRepository)
    mock_frete_api = mocker.Mock(spec=FreteAPI)
    mock_gateway_pagamento = mocker.Mock()
    
    # Stub/Mock de E-mail (Item 5)
    # Substitui a função enviar_confirmacao do módulo servico_email
    mock_servico_email = mocker.patch('src.servico_email.enviar_confirmacao')

    # --- 2. COMPORTAMENTO DOS MOCKS ---
    
    # Stub de Estoque (Item 4)
    mock_estoque_repo.consultar_quantidade.return_value = 10 
    
    # Mock de Frete (Item 4)
    mock_frete_api.calcular_frete.return_value = 50.00 
    
    # Mock de Pagamento (Item 5)
    mock_gateway_pagamento.processar_pagamento.return_value = {"status": "APROVADO", "id_transacao": "TRANS123"} 
    
    # --- 3. CENÁRIO E INJEÇÃO ---
    produto_a = Produto(id=101, nome="Mouse", preco=100.00)
    
    carrinho = Carrinho(estoque_repo=mock_estoque_repo, frete_api=mock_frete_api, 
                        gateway_pagamento=mock_gateway_pagamento)

    carrinho.adicionar_item(produto_a, 2) # 2 unidades * R$100.00 = R$200.00
    
    # --- 4. AÇÃO ---
    fatura = carrinho.finalizar_compra(
        dados_pagamento={"cartao": "visa", "cvv": "123"},
        repo_fatura=repo_fatura,
        servico_email=mock_servico_email # Passando o mock de e-mail como argumento
    )
    
    # --- 5. ASSERTIVAS (Verificação de Estado e Interação) ---
    
    # Assertivas de Estado (Total Final)
    assert fatura is not None
    # 200.00 (produtos) + 50.00 (frete) = 250.00
    assert fatura.total_final == 250.00 
    assert fatura.status == "PAGO"
    
    # Verificação de Interações Críticas
    
    # [Stub] Reserva de Estoque
    mock_estoque_repo.reservar.assert_called_once_with(produto_a.id, 2)
    
    # [Mock] Cálculo de Frete
    mock_frete_api.calcular_frete.assert_called_once()
    
    # [Mock] Pagamento
    mock_gateway_pagamento.processar_pagamento.assert_called_once()
    
    # [Stub] Envio de E-mail (Item 5)
    mock_servico_email.assert_called_once_with(fatura)
    
    # [Repositório em Memória] Salvar Fatura
    assert repo_fatura.buscar_por_id(fatura.id) is not None