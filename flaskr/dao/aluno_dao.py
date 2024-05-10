from flaskr.db import get_db

class AlunoDao:
    def __init__(self):
        pass

    # insert: insere um aluno no banco de dados
    def insert(self, id_user):
        db = get_db()

        try:
            db.execute(
                "INSERT INTO aluno (id_user) VALUES (?)",
                (id_user,),
            )
            db.commit()
        except db.IntegrityError:
            return f"User {id_user} is already registered."
        return None

    # select: seleciona um aluno no banco de dados
    def select(self, id_user):
        db = get_db()
        return db.execute(
            "SELECT * FROM aluno WHERE id_user = ?", (id_user,)
        ).fetchone()

    # select_user: seleciona um aluno no banco de dados dando join com a tabela user
    def select_user(self, id_user):
        db = get_db()
        return db.execute(
            "SELECT * FROM user u JOIN aluno a ON u.id_user = a.id_user WHERE u.id_user = ?", (id_user,)
        ).fetchone()

    # select_all: seleciona todos os alunos no banco de dados
    def select_all(self):
        db = get_db()
        return db.execute(
            "SELECT * FROM aluno"
        ).fetchall()

    # delete: deleta um aluno no banco de dados
    def delete(self, id_user):
        db = get_db()
        db.execute("DELETE FROM aluno WHERE id_user = ?", (id_user,))
        db.commit()

    # get_saldo: retorna o saldo de um aluno no banco de dados
    def get_saldo(self, id_user):
        db = get_db()
        return db.execute(
            "SELECT saldo FROM aluno WHERE id_user = ?", (id_user,)
        ).fetchone()

    # get_db: retorna o banco de dados
    def get_db(self):
        return get_db()
