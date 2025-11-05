# src/carrinho.py (mínimo para passar no primeiro teste)

class ItemCarrinho:
    def __init__(self, produto, quantidade):
        self.produto = produto
        self.quantidade = quantidade

class Carrinho:
    def __init__(self):
        self.itens = []

    def adicionar_item(self, produto, quantidade):
        # Implementação mínima para o TDD passar
        self.itens.append(ItemCarrinho(produto, quantidade))

    def calcular_total(self):
        total = 0.0
        for item in self.itens:
            subtotal = item.produto.preco * item.quantidade
            desconto = 0.0
            
            # Lógica mínima da promoção para o TDD (10% de desconto)
            if item.quantidade >= 5:
                desconto = 0.10
                
            total += subtotal * (1 - desconto)
        return total
    
    def _calcular_desconto_item(self, quantidade):
        """Nova função para isolar a regra de negócio da promoção."""
        if quantidade >= 10:
            return 0.15
        elif quantidade >= 5:
            return 0.10
        return 0.0

    def calcular_total(self):
        total = 0.0
        for item in self.itens:
            subtotal = item.produto.preco * item.quantidade
            
            desconto = self._calcular_desconto_item(item.quantidade) # Usando a nova função
                
            total += subtotal * (1 - desconto)
        return total
        