class Item:
    """
    Entidade Item

    Atributos:
    id: int
    nome: str
    valor: float
    """
    def __init__(self, id_item, id_turma, nome, valor):
        self.id_item = id_item
        self.id_turma = id_turma
        self.nome = nome
        self.valor = valor

    def __dict__(self):
        return {
            'id_item': self.id_item,
            'id_turma': self.id_turma,
            'nome': self.nome,
            'valor': self.valor
        }
