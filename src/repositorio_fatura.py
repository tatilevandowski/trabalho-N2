# src/repositorio_fatura.py
from src.fatura import Fatura 

class InMemoryFaturaRepository:
    def __init__(self):
        self._faturas = {}
        
    def salvar(self, fatura: Fatura):
        self._faturas[fatura.id] = fatura
        
    def buscar_por_id(self, fatura_id):
        return self._faturas.get(fatura_id)