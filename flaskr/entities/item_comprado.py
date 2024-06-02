from datetime import datetime

from flaskr.entities.aluno import Aluno
from flaskr.entities.item import Item


class ItemComprado:
    """
    Entidade ItemComprado
    """
    def __init__(self, id_item: int, aluno_matricula: int):
        self.item = id_item
        self.aluno = aluno_matricula
        self.data_compra = datetime.now()

    def to_dict(self):
        return {
            "item": self.item,
            "aluno": self.aluno,
            "data_compra": self.data_compra
        }