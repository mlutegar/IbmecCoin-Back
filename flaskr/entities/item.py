class Item:
    """
    Entidade Item

    Atributos:
    id: int
    nome: str
    valor: float
    """
    def __init__(self, id, nome, valor):
        self.id = id
        self.nome = nome
        self.valor = valor

    def to_dict(self):
        return {
            'id_item': self.id,
            'nome': self.nome,
            'valor': self.valor
        }

    @staticmethod
    def from_dict(dict):
        return Item(
            id=dict['id_item'],
            nome=dict['nome'],
            valor=dict['valor']
        )

    @staticmethod
    def from_tuple(tuple):
        return Item(
            id=tuple[0],
            nome=tuple[1],
            valor=tuple[2]
        )

    def __str__(self):
        return f'Item({self.id}, {self.nome}, {self.valor})'

    def __repr__(self):
        return self.__str__()
