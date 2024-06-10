from datetime import datetime


class ItemComprado:
    """
    Entidade ItemComprado
    """
    def __init__(self, id_item: int, aluno_matricula: int):
        self.item = id_item
        self.aluno = aluno_matricula
        self.data_compra = datetime.now()

    def __dict__(self):
        return {
            "item": self.item,
            "aluno": self.aluno,
            "data_compra": self.data_compra
        }
