# src/exceptions.py

# Exceções de Regras de Negócio e Validação

class QuantidadeInvalidaError(ValueError):
    """Lançada quando a quantidade de um produto é zero ou negativa."""
    pass

class CupomInvalidoError(ValueError):
    """Lançada quando um cupom é inválido, expirado ou não se aplica."""
    pass

class PagamentoRecusadoError(Exception):
    """Lançada quando o gateway de pagamento recusa a transação."""
    pass

class EstoqueInsuficienteError(Exception): # <--- A EXCEÇÃO QUE FALTAVA
    """Lançada quando a quantidade em estoque é menor que a solicitada."""
    pass

class FaturaNaoEncontradaError(Exception):
    """Lançada quando uma fatura é buscada mas não existe no repositório."""
    pass