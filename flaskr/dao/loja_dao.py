from flaskr.dao.aluno_dao import AlunoDAO
from flaskr.entities.item import Item
from flaskr.utils.db import get_db


class LojaDAO:
    def insert_item(self, nome, valor):
        """
        Insere um item na loja.
        :param nome: nome do item
        :param valor: valor do item
        :return: True se o item foi inserido com sucesso, False caso contrário
        """
        db = get_db()
        try:
            db.execute(
                "INSERT INTO item_loja (nome, valor) VALUES (?, ?)",
                (nome, valor),
            )
            db.commit()
        except db.IntegrityError:
            return False
        return True

    @staticmethod
    def get_item(id_item):
        """
        Seleciona um item na loja.
        :param id_item: id do item
        :return: Objeto do tipo Item, ou None se o item não for encontrado
        """
        db = get_db()
        resultado = db.execute(
            "SELECT * FROM item_loja WHERE id_item = ?", (id_item,)
        ).fetchone()

        if resultado:
            item = Item(
                resultado['id_item'],
                resultado['nome'],
                resultado['valor']
            )
            return item
        return None

    def get_all_items(self):
        """
        Seleciona todos os itens na loja.
        :return: Lista de objetos do tipo Item, ou None se não houver itens
        """
        db = get_db()
        resultado = db.execute(
            "SELECT * FROM item_loja"
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

    def update_item(self, id_item, **kwargs):
        """
        Atualiza os campos de um item na loja com base nos argumentos fornecidos.
        :param id_item: id do item
        :param kwargs: Dicionário de campos a serem atualizados
        :return: True se o item foi atualizado com sucesso, False caso contrário
        """
        db = get_db()
        set_clause = ", ".join(f"{key} = ?" for key in kwargs)
        values = list(kwargs.values()) + [id_item]
        query = f"UPDATE item_loja SET {set_clause} WHERE id_item = ?"
        try:
            db.execute(query, values)
            db.commit()
        except db.IntegrityError:
            return False
        return True

    def delete_item(self, id_item):
        """
        Deleta um item na loja.
        :param id_item: id do item
        :return: True se o item foi deletado com sucesso, False caso contrário
        """
        db = get_db()
        try:
            db.execute(
                "DELETE FROM item_loja WHERE id_item = ?", (id_item,)
            )
            db.commit()
        except db.IntegrityError:
            return False
        return True
