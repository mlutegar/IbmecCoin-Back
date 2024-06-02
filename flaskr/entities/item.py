class Item:
    """
    Entidade Item

    Atributos:
    id: int
    nome: str
    valor: float
    """
    def __init__(self, id_item, nome, valor):
        self.id_item = id_item
        self.nome = nome
        self.valor = valor

    def to_dict(self):
        return {
            'id_item': self.id_item,
            'nome': self.nome,
            'valor': self.valor
        }
