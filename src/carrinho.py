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