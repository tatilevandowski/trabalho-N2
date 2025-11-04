# tests/conftest.py

import sys
import os

import pytest
from src.produto import Produto
from src.estoque import EstoqueRepository
from unittest.mock import MagicMock

# 1. Fixture de Entidade
@pytest.fixture(scope="function")
def produto_padrao():
    """Retorna uma instância básica e limpa de Produto."""
    return Produto(id=1, nome="Notebook", preco=2000.00)

# 2. Stub: EstoqueRepository (simulando que está em memória)
@pytest.fixture(scope="function")
def mock_estoque_repo(mocker):
    """Stub de EstoqueRepository que simula as operações de estoque."""
    
    # Simula o repositório, garantindo que podemos espiar (spy) as chamadas
    repo = mocker.Mock(spec=EstoqueRepository)
    
    # Comportamento: 10 unidades disponíveis por padrão
    repo.consultar_quantidade.return_value = 10
    
    # Stubs para os métodos de alteração (não fazem nada de fato)
    repo.reservar = mocker.stub(name="reservar")
    repo.liberar = mocker.stub(name="liberar")
    
    return repo