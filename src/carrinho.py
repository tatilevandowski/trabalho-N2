# src/carrinho.py

import uuid # Necessário para gerar IDs de fatura
from .fatura import Fatura
from .exceptions import CupomInvalidoError, PagamentoRecusadoError, QuantidadeInvalidaError, EstoqueInsuficienteError
# Certifique-se de que a classe Fatura existe em src/entidades.py ou similar
# from .entidades import Fatura 

# Helper class para representar um item no carrinho
class ItemCarrinho:
    def __init__(self, produto, quantidade):
        self.produto = produto
        self.quantidade = quantidade

class Carrinho:
    """
    Entidade Carrinho, responsável pela lógica de negócio:
    - Adicionar itens (com reserva de estoque - Stub)
    - Calcular total (com promoção e cupom)
    - Finalizar compra (com frete e pagamento simulados - Mocks)
    """
    
    # Única implementação do construtor, injetando todas as dependências (Stubs/Mocks)
    def __init__(self, estoque_repo, frete_api=None, gateway_pagamento=None):
        self.estoque_repo = estoque_repo
        self.frete_api = frete_api 
        self.gateway_pagamento = gateway_pagamento
        self.itens = []
        self.cupom = None
        self.fatura_repo = None # Será injetado apenas no finalize_compra para cobrir o requisito
        
    def _calcular_desconto_item(self, quantidade):
        """Nova função para isolar a regra de negócio da promoção progressiva (TDD Refatorar)."""
        if quantidade >= 10:
            return 0.15 # 15% de desconto
        elif quantidade >= 5:
            return 0.10 # 10% de desconto
        return 0.0

    def adicionar_item(self, produto, quantidade):
        # 3. Testes de Exceção: Casos inválidos (qtd <= 0)
        if quantidade <= 0:
            raise QuantidadeInvalidaError("A quantidade do produto deve ser positiva.")

        # --- Regra de Negócio: Reserva e Exceção de Estoque ---
        if self.estoque_repo:
            
            # 1. Consulta o estoque (Usa o Stub)
            estoque_disponivel = self.estoque_repo.consultar_quantidade(produto.id)
            
            # 2. Verifica a regra e LANÇA a exceção (Necessário para o teste passar!)
            if estoque_disponivel < quantidade:
                raise EstoqueInsuficienteError(
                    f"Estoque insuficiente para {produto.nome}. Disponível: {estoque_disponivel}"
                )

            # 3. Chamada ao Stub: Reserva de Estoque (Item 4) - SÓ RESERVA SE HOUVER ESTOQUE
            self.estoque_repo.reservar(produto.id, quantidade)
            
        # 4. Adiciona o Item ao carrinho
        self.itens.append(ItemCarrinho(produto, quantidade))
        
    def aplicar_cupom(self, cupom):
        # 3. Testes de Exceção: Cupom expirado
        if not hasattr(cupom, 'is_valido') or not cupom.is_valido():
             raise CupomInvalidoError("Cupom expirado ou inválido.")
        self.cupom = cupom
        
    def calcular_total(self):
        """Calcula o total dos produtos aplicando a promoção progressiva."""
        total = 0.0
        for item in self.itens:
            subtotal = item.produto.preco * item.quantidade
            
            # Aplica a promoção progressiva (TDD)
            desconto_promocao = self._calcular_desconto_item(item.quantidade)
            
            total_item_com_promocao = subtotal * (1 - desconto_promocao)
            
            total += total_item_com_promocao
        
        # Aplicar desconto de cupom (Se existir)
        if self.cupom:
            total *= (1 - self.cupom.percentual_desconto) # Assumindo que o cupom tem percentual_desconto
            
        return round(total, 2) # Garante precisão

    def calcular_total_com_frete(self):
        """Calcula o total final, incluindo o frete (Mock de FreteAPI)."""
        if not self.frete_api:
            # Deve ser injetado para o teste de integração/fluxo completo
            raise ValueError("API de Frete não configurada.") 
            
        total_produtos = self.calcular_total()
        
        # Simula a chamada ao Mock de Frete (Item 4)
        frete = self.frete_api.calcular_frete(self.itens)
        
        return round(total_produtos + frete, 2)
        
    def finalizar_compra(self, dados_pagamento, repo_fatura, servico_email):
        """
        Orquestra a finalização da compra, interagindo com Mocks/Stubs. (Item 6)
        repo_fatura e servico_email são injetados no método para flexibilidade no Teste de Integração.
        """
        if not self.gateway_pagamento:
             raise ValueError("Gateway de Pagamento não configurado.")
             
        total = self.calcular_total_com_frete()
        
        # Chamada ao Mock: Processa o pagamento simulado (Item 5)
        # O Mock simulará aprovado/negado/latência
        resultado = self.gateway_pagamento.processar_pagamento(total, dados_pagamento)
        
        # 3. Testes de Exceção: Pagamento recusado
        if resultado.get("status") != "APROVADO":
            raise PagamentoRecusadoError("Transação negada pelo gateway de pagamento.")
            
        # Lógica de sucesso
        fatura_id = uuid.uuid4()
        fatura = Fatura(id=fatura_id, total_final=total, status="PAGO", itens=self.itens)
        
        # Repositório em memória (Item 6)
        repo_fatura.salvar(fatura) 
        
        # Stub de e-mail (Item 5)
        servico_email.enviar_confirmacao(fatura)
        
        return fatura