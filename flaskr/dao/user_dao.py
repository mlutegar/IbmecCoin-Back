# UserDao: classe responsável por realizar operações no banco de dados relacionadas a entidade User
from flaskr.db import get_db


class UserDao:
    """
    Classe responsável por realizar operações no banco de dados relacionadas a entidade User

    Métodos:
    - insert_user(matricula, senha, tipo): Insere um usuário no banco de dados
    - get_user_by_matricula(matricula): Seleciona um usuário no banco de dados
    - get_user_by_id(id_user): Seleciona um usuário no banco de dados
    - get_all_user(): Seleciona todos os usuários no banco de dados
    - update_user(matricula, senha): Atualiza a senha de um usuário no banco de dados
    - delete_user(matricula): Deleta um usuário do banco de dados
    """
    @staticmethod
    def insert_user(matricula, senha, tipo):
        """
        Insere um usuário no banco de dados
        :param matricula: matrícula do usuário
        :param senha: senha do usuário
        :param tipo: tipo do usuário
        :return: True se o usuário foi inserido com sucesso, False caso contrário
        """
        db = get_db()
        try:
            db.execute(
                "INSERT INTO user (matricula, senha, tipo) VALUES (?, ?, ?)",
                (matricula, senha, tipo),
            )
            db.commit()
        except db.IntegrityError:
            return False
        return True

    @staticmethod
    def get_user_by_matricula(matricula: str):
        """
        Seleciona um usuário no banco de dados.
        :param matricula: matrícula do usuário
        :return: Dicionário contendo os dados do usuário, ou None se o usuário não for encontrado
        """
        db = get_db()
        query = "SELECT * FROM user WHERE matricula = ?"
        result = db.execute(query, (matricula,)).fetchone()
        if result:
            return dict(result)
        return None

    @staticmethod
    def get_user_by_id(id_user: int):
        """
        Seleciona um usuário no banco de dados.
        :param id_user: id do usuário
        :return: Dicionário contendo os dados do usuário, ou None se o usuário não for encontrado
        """
        db = get_db()
        query = "SELECT * FROM user WHERE id = ?"
        result = db.execute(query, (id_user,)).fetchone()
        if result:
            return dict(result)
        return None

    @staticmethod
    def get_all_user():
        """
        Seleciona todos os usuários no banco de dados
        :return: Lista de dicionários contendo os dados dos usuários, ou None se não houver usuários
        """
        db = get_db()
        result = db.execute(
            "SELECT * FROM user"
        ).fetchall()
        if result:
            return result
        return None

    @staticmethod
    def update_user(matricula, senha):
        """
        Atualiza a senha de um usuário no banco de dados
        :param matricula: matrícula do usuário
        :param senha: nova senha do usuário
        :return: True se a senha foi atualizada com sucesso, False caso contrário
        """
        db = get_db()
        try:
            db.execute(
                "UPDATE user SET senha = ? WHERE matricula = ?",
                (senha, matricula),
            )
            db.commit()
        except db.IntegrityError:
            return False
        return True

    @staticmethod
    def delete_user(matricula):
        """
        Deleta um usuário do banco de dados
        :param matricula: matrícula do usuário
        :return: True se o usuário foi deletado com sucesso, False caso contrário
        """
        db = get_db()
        try:
            db.execute("DELETE FROM user WHERE matricula = ?", (matricula,))
            db.commit()
        except db.IntegrityError:
            return False
        return True
