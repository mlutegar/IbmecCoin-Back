from flaskr.dao.aluno_dao import AlunoDAO
from flaskr.dao.loja_dao import LojaDAO
from flaskr.entities.aluno import Aluno
from flaskr.entities.item import Item
from flaskr.utils.db import get_db


class ItemCompradoDAO:
    """
    Classe que representa o DAO de Item Comprado
    """
    @staticmethod
    def buy_item(id_item: int, aluno_matricula: int):
        """
        Compra um item na loja.
        :param id_item: Item a ser comprado
        :param aluno_matricula: Aluno que está comprando o item
        :return: True se o item foi comprado com sucesso, False caso contrário
        """
        item = LojaDAO.get_item(id_item)
        aluno = AlunoDAO().get_aluno(aluno_matricula)

        if not item or not aluno or aluno.saldo < item.valor:
            return False

        db = get_db()
        try:
            db.execute(
                "INSERT INTO item_comprado (id_item, aluno_id) VALUES (?, ?)",
                (item.id_item, aluno.matricula),
            )
            db.execute(
                "UPDATE aluno SET saldo = ? WHERE matricula = ?",
                (aluno.saldo - item.valor, aluno.matricula),
            )
            db.commit()
        except db.IntegrityError:
            return False
        return True

    @staticmethod
    def get_all_items_by_matricula(aluno_matricula):
        """
        Seleciona todos os itens comprados por um aluno.
        :param aluno_matricula: matrícula do aluno
        :return: Lista de objetos do tipo Item, ou None se não houver itens
        """
        aluno = AlunoDAO().get_aluno(aluno_matricula)

        if not aluno:
            return None

        db = get_db()

        resultado = db.execute(
            "SELECT * FROM item_loja WHERE id_item IN (SELECT id_item FROM item_comprado WHERE aluno_id = ?)",
            (aluno_matricula,)
        ).fetchall()

        if not resultado:
            return None

        items = []
        for row in resultado:
            item = Item(
                row['id_item'],
                row['nome'],
                row['valor']
            )
            items.append(item)

        return items
