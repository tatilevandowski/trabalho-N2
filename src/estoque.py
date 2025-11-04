# src/estoque.py

class EstoqueRepository:
    """Interface ou classe para interagir com o estoque."""
    
    def consultar_quantidade(self, produto_id: int) -> int:
        raise NotImplementedError
        
    def reservar(self, produto_id: int, quantidade: int):
        raise NotImplementedError
        
    def liberar(self, produto_id: int, quantidade: int):
        raise NotImplementedError