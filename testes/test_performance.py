# src/tests/test_performance.py

import time
import pytest
from src.carrinho import Carrinho
from src.produto import Produto 

@pytest.mark.slow # Marca o teste como lento
def test_performance_calculo_em_massa(produto_padrao, mocker):
    """Mede o tempo de execução de um cálculo complexo ou em massa."""
    
    # Mocks necessários para a inicialização do carrinho
    mock_estoque = mocker.Mock()
    
    # Configuração de um cenário pesado
    carrinho = Carrinho(estoque_repo=mock_estoque)
    NUM_ITERACOES = 10000 
    
    for _ in range(NUM_ITERACOES):
        carrinho.adicionar_item(produto_padrao, 1)

    start_time = time.perf_counter() # Início da medição
    
    carrinho.calcular_total() 
    
    end_time = time.perf_counter() # Fim da medição
    duration = end_time - start_time
    
    LIMITE_TEMPO_SEGUNDOS = 0.05 # 50 milissegundos
    
    print(f"\nTempo de Execução ({NUM_ITERACOES} itens): {duration:.4f}s")
    
    # O teste falha se for mais lento que o limite
    assert duration < LIMITE_TEMPO_SEGUNDOS