from datetime import datetime

from flaskr.entities.aluno import Aluno
from flaskr.entities.item import Item


class ItemComprado:
    """
    Entidade ItemComprado
    """
    def __init__(self, item_id: int, aluno_matricula: int):
        self.item = item_id
        self.aluno = aluno_matricula
        self.data_compra = datetime.now()
