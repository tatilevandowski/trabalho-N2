# src/produto.py

class Produto:
    """Entidade básica do catálogo."""
    def __init__(self, id: int, nome: str, preco: float):
        self.id = id
        self.nome = nome
        self.preco = preco

