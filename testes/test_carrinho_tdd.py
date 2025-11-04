from src.carrinho import Carrinho

def test_calculo_total_com_promocao_progressiva_desconto_10_porcento(produto_padrao):
    """Teste que deve falhar, pois a funcionalidade não existe."""
    carrinho = Carrinho() # A ser criada em src/carrinho.py
    carrinho.adicionar_item(produto_padrao, 5)
    
    # 5 * 2000.00 = 10000.00
    # Desconto 10%: 10000.00 * 0.90 = 9000.00
    total_esperado = 9000.00
    
    assert carrinho.calcular_total() == total_esperado