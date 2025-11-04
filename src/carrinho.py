class Carrinho:
    def __init__(self):
        self.itens = []

    def adicionar_item(self, produto):
        self.itens.append(produto)

    def calcular_total(self):
        return sum(item.preco for item in self.itens)
