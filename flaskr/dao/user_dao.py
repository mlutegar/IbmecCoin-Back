# UserDao: classe responsável por realizar operações no banco de dados relacionadas a entidade User
from flaskr.utils.db import get_db
from flaskr.entities.user import User


class UserDAO:
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
    def insert_user(nome, matricula, senha, tipo, email):
        """
        Insere um usuário no banco de dados
        :param nome: nome do usuário
        :param matricula: matrícula do usuário
        :param senha: senha do usuário
        :param tipo: tipo do usuário
        :param email: email do usuário
        :return: True se o usuário foi inserido com sucesso, False caso contrário
        """

        db = get_db()
        try:
            db.execute(
                "INSERT INTO user (nome, matricula, senha, tipo, email) VALUES (?, ?, ?, ?, ?)",
                (nome, matricula, senha, tipo, email),
            )
            db.commit()
        except db.IntegrityError:
            return False
        return True

    @staticmethod
    def get_user(matricula: int):
        """
        Seleciona um usuário no banco de dados.
        :param matricula: Matrícula do usuário
        :return: Objeto do tipo User, ou None se o usuário não for encontrado
        """
        db = get_db()
        query = "SELECT * FROM user WHERE matricula = ?"
        result = db.execute(query, (matricula,)).fetchone()
        if result:
            user = User(result['matricula'], result['senha'], result['tipo'], result['nome'], result['email'])
            return user
        return None

    @staticmethod
    def get_user_by_matricula(user_matricula: int):
        """
        Seleciona um usuário no banco de dados.
        :param user_matricula: Matrícula do usuário
        :return: Objeto do tipo User, ou None se o usuário não for encontrado
        """
        db = get_db()
        query = "SELECT * FROM user WHERE matricula = ?"
        result = db.execute(query, (user_matricula,)).fetchone()
        if result:
            user = User(result['matricula'], result['senha'], result['tipo'], result['nome'], result['email'])
            return user
        return None

    @staticmethod
    def get_all_user():
        """
        Seleciona todos os usuários no banco de dados
        :return: Lista de objetos do tipo User, ou None se não houver usuários
        """
        db = get_db()
        result = db.execute(
            "SELECT * FROM user"
        ).fetchall()
        if result:
            lista = []
            for user in result:
                lista.append(User(user['matricula'], user['senha'], user['tipo'], user['id'], user['email']))
            return lista
        return None

    @staticmethod
    def update_user(user: User):
        """
        Atualiza os campos de um usuário no banco de dados com base nos argumentos fornecidos.
        :param user: Objeto do tipo User
        :return: True se o usuário foi atualizado com sucesso, False caso contrário
        """
        db = get_db()
        try:
            db.execute(
                "UPDATE user SET nome = ?, senha = ?, tipo = ?, email = ? WHERE matricula = ?",
                (user.nome, user.senha, user.tipo, user.email, user.matricula)
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
