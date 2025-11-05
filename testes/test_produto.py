# src/tests/test_produto.py

from src.produto import Produto 

def test_produto_e_instanciado_corretamente():
    """Verifica se a entidade Produto é criada com os atributos corretos."""
    
    produto = Produto(id=1, nome="Teclado Mecânico", preco=350.50)
    
    # Assertivas de Estado
    assert produto.id == 1
    assert produto.nome == "Teclado Mecânico"
    assert produto.preco == 350.50
    assert isinstance(produto, Produto)