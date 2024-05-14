from flaskr.dao.user_dao import UserDao
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

    # select_uder_by_matricula: seleciona um aluno no banco de dados dando join com a tabela user
    def select_user_by_matricula(self, matricula):
        db = get_db()
        aluno = db.execute(
            "SELECT * FROM user u JOIN aluno a ON u.id_user = a.id_user WHERE u.matricula = ?", (matricula,)
        ).fetchone()

        if aluno is None:
            return -1

        return aluno


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

    def select_aluno_by_matricula(self, matricula):
        db = get_db()

        return db.execute(
            "SELECT * FROM user u JOIN aluno a ON u.id_user = a.id_user WHERE u.matricula = ?", (matricula,)
        ).fetchone()

    def creditar_saldo(self, matricula, quantidade):
        db = get_db()

        userDao = UserDao()
        id = userDao.get_id_by_matricula(matricula)

        saldo = db.execute(
            "SELECT saldo FROM aluno WHERE id_user = ?", (id,)
        ).fetchone()

        saldo = saldo["saldo"]
        saldo += quantidade

        db.execute(
            "UPDATE aluno SET saldo = ? WHERE id_user = ?",
            (saldo, id),
        )

        db.commit()
        return saldo

    def debitar_saldo(self, matricula, quantidade):
        db = get_db()

        userDao = UserDao()
        id = userDao.get_id_by_matricula(matricula)

        saldo = db.execute(
            "SELECT saldo FROM aluno WHERE id_user = ?", (id,)
        ).fetchone()

        saldo = saldo["saldo"]
        saldo -= quantidade

        db.execute(
            "UPDATE aluno SET saldo = ? WHERE id_user = ?",
            (saldo, id),
        )

        db.commit()
        return saldo

    def get_all_user_alunos(self):
        db = get_db()
        rows = db.execute(
            "SELECT u.matricula, a.nome, a.email, a.saldo, a.turma_id "
            "FROM user u JOIN aluno a ON u.id_user = a.id_user"
        ).fetchall()

        alunos = []
        for row in rows:
            aluno = {
                "matricula": row["matricula"],
                "nome": row["nome"],
                "email": row["email"],
                "saldo": row["saldo"],
                "turma_id": row["turma_id"],
            }
            alunos.append(aluno)

        if len(alunos) == 0:
            return [], "Nenhum aluno encontrado."

        return alunos, "Alunos encontrados com sucesso."