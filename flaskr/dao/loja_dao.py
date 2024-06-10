from flaskr.entities.item import Item
from flaskr.utils.db import get_db


class LojaDAO:
    @staticmethod
    def insert_item(id_turma, nome, valor):
        """
        Insere um item na loja.
        :param id_turma: Id da turma
        :param nome: nome do item
        :param valor: valor do item
        :return: True se o item foi inserido com sucesso, False caso contrário
        """
        db = get_db()
        try:
            db.execute(
                "INSERT INTO item_loja (id_turma, nome, valor) VALUES (?, ?, ?)",
                (id_turma, nome, valor),
            )
            db.commit()
        except db.IntegrityError:
            return False
        return True

    @staticmethod
    def get_item(id_item):
        """
        Seleciona um item na loja.
        :param id_item: Id do item
        :return: Objeto do tipo Item, ou None se o item não for encontrado
        """
        db = get_db()
        resultado = db.execute(
            "SELECT * FROM item_loja WHERE id_item = ?", (id_item,)
        ).fetchone()

        if resultado:
            item = Item(
                resultado['id_item'],
                resultado['id_turma'],
                resultado['nome'],
                resultado['valor']
            )
            return item
        return None

    @staticmethod
    def get_all_items():
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
                row['id_turma'],
                row['nome'],
                row['valor']
            )
            items.append(item)

        return items

    def get_all_itens_global(self):
        """
        Retorna uma lista de todos os itens que estão disponíveis na loja global. Ele busca todos os itens no banco de
        dados e a partir do id dos itens ele cria uma lista de objetos Item e adiciona todos os itens nessa lista.
        E retorna essa lista.

        :return: list
        """
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM item_loja where id_turma is null")
        itens = cursor.fetchall()

        lista_itens = []
        for item in itens:
            item_obj = self.get_item(item[0])
            lista_itens.append(item_obj)
        return lista_itens

    def get_all_itens_by_id_turma(self, id_turma: int):
        """
        Retorna uma lista de itens que estão disponíveis na loja de uma turma. Ele busca todos os itens no banco de
        dados pelo o id da turma, e a partir do id dos itens ele cria uma lista de objetos Item e adiciona todos os
        itens nessa lista. E retorna essa lista.

        :param id_turma: int

        :return: list
        """
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM item_loja WHERE id_turma=?", (id_turma,))
        itens = cursor.fetchall()

        lista_itens = []
        for item in itens:
            item_obj = self.get_item(item[0])
            lista_itens.append(item_obj)
        return lista_itens

    @staticmethod
    def update_item(id_item, **kwargs):
        """
        Atualiza os campos de um item na loja com base nos argumentos fornecidos.
        :param id_item: Id do item
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

    # curl -X DELETE http://localhost:5000/loja/item/1
    @staticmethod
    def delete_item(id_item):
        """
        Deleta um item na loja.
        :param id_item: Id do item
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
