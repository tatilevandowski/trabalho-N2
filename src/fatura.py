# src/fatura.py

import uuid
from typing import List

# Assumindo que ItemCarrinho é importável ou definível
# from .carrinho import ItemCarrinho 

class Fatura:
    """Entidade Fatura, gerada após a compra."""
    def __init__(self, total_final: float, status: str, itens: List, id: uuid.UUID = None):
        # Gera um ID se não for fornecido (útil para o repositório)
        self.id = id if id else uuid.uuid4()
        self.total_final = total_final
        self.status = status # Ex: "PAGO", "PENDENTE", "CANCELADO"
        self.itens = itens # Lista de ItemCarrinho que foram comprados

