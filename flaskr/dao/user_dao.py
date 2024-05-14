# UserDao: classe responsável por realizar operações no banco de dados relacionadas a entidade User
from flaskr.db import get_db


class UserDao:
    def __init__(self):
        pass

    # insert: insere um usuário no banco de dados
    def insert(self, matricula, senha, tipo):
        db = get_db()

        try:
            db.execute(
                "INSERT INTO user (matricula, senha, tipo) VALUES (?, ?, ?)",
                (matricula, senha, tipo),
            )
            db.commit()
        except db.IntegrityError:
            return -1
        return 1

    # select: seleciona um usuário no banco de dados
    def select(self, matricula):
        db = get_db()
        return db.execute(
            "SELECT * FROM user WHERE matricula = ?", (matricula,)
        ).fetchone()

    # select_all: seleciona todos os usuários no banco de dados
    def select_all(self):
        db = get_db()
        return db.execute(
            "SELECT * FROM user"
        ).fetchall()

    # update: atualiza a senha de um usuário no banco de dados
    def update(self, matricula, senha):
        db = get_db()
        db.execute(
            "UPDATE user SET senha = ? WHERE matricula = ?",
            (senha, matricula),
        )
        db.commit()

    # delete: deleta um usuário no banco de dados
    def delete(self, matricula):
        db = get_db()
        db.execute("DELETE FROM user WHERE matricula = ?", (matricula,))
        db.commit()

    # get_saldo: retorna o saldo de um usuário no banco de dados
    def get_saldo(self, matricula):
        db = get_db()
        return db.execute(
            "SELECT saldo FROM user WHERE matricula = ?", (matricula,)
        ).fetchone()

    # get_db: retorna o banco de dados
    def get_db(self):
        return get_db()

    # get_id_by_matricula: retorna o id de um usuário a partir da matrícula
    def get_id_by_matricula(self, matricula):
        db = get_db()
        try:
            id = db.execute(
            "SELECT id_user FROM user WHERE matricula = ?", (matricula,)
            ).fetchone()
            id = id["id_user"]
        except db.IntegrityError:
            return -1
        return id

    # get_tipo_by_matricula: retorna o tipo de um usuário a partir da matrícula
    def get_tipo_by_matricula(self, matricula):
        db = get_db()
        try:
            tipo = db.execute(
            "SELECT tipo FROM user WHERE matricula = ?", (matricula,)
            ).fetchone()
        except db.IntegrityError:
            return -1

        if tipo is None:
            return -1

        return tipo["tipo"]

    # get_tipo_by_id: retorna o tipo de um usuário a partir do id
    def get_tipo_by_id(self, id):
        db = get_db()
        try:
            tipo = db.execute(
            "SELECT tipo FROM user WHERE id_user = ?", (id,)
            ).fetchone()
        except db.IntegrityError:
            return -1

        try:
            tipo = tipo["tipo"]
        except:
            return -1

        return tipo

    # select_professor: seleciona um professor no banco de dados com join com a tabela user
    def select_professor(self, id_user):
        db = get_db()

        return db.execute(
            "SELECT * FROM user u JOIN professor p ON u.id_user = p.id_user WHERE u.id_user = ?", (id_user,)
        ).fetchone()

    # select_aluno: seleciona um aluno no banco de dados com join com a tabela user
    def select_aluno(self, id_user):
        db = get_db()

        return db.execute(
            "SELECT * FROM user u JOIN aluno a ON u.id_user = a.id_user WHERE u.id_user = ?", (id_user,)
        ).fetchone()

    # select_aluno_by_matricula: seleciona um aluno no banco de dados com join com a tabela user
    def select_aluno_by_matricula(self, matricula):
        db = get_db()

        return db.execute(
            "SELECT * FROM user u JOIN aluno a ON u.id_user = a.id_user WHERE u.matricula = ?", (matricula,)
        ).fetchone()

    # select_professor_by_matricula: seleciona um professor no banco de dados com join com a tabela user
    def select_professor_by_matricula(self, matricula):
        db = get_db()

        return db.execute(
            "SELECT * FROM user u JOIN professor p ON u.id_user = p.id_user WHERE u.matricula = ?", (matricula,)
        ).fetchone()

    def get_id_by_matricula(self, matricula):
        db = get_db()

        user = db.execute(
            "SELECT id_user FROM user WHERE matricula = ?", (matricula,)
        ).fetchone()

        if user is None:
            return -1

        return user["id_user"]
