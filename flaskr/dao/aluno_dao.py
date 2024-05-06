from flaskr.db import get_db

class AlunoDao:
    def __init__(self):
        self.db = get_db()

    def insert(self, matricula, senha):
        try:
            self.db.execute(
                "INSERT INTO aluno (matricula, senha) VALUES (?, ?)",
                (matricula, senha),
            )
            self.db.commit()
        except self.db.IntegrityError:
            return f"User {matricula} is already registered."
        return None

    def select(self, matricula):
        return self.db.execute(
            "SELECT * FROM aluno WHERE matricula = ?", (matricula,)
        ).fetchone()

    def select_all(self):
        return self.db.execute(
            "SELECT * FROM aluno"
        ).fetchall()

    def update(self, matricula, senha):
        self.db.execute(
            "UPDATE aluno SET senha = ? WHERE matricula = ?",
            (senha, matricula),
        )
        self.db.commit()

    def delete(self, matricula):
        self.db.execute("DELETE FROM aluno WHERE matricula = ?", (matricula,))
        self.db.commit()

    def get_saldo(self, matricula):
        return self.db.execute(
            "SELECT saldo FROM aluno WHERE matricula = ?", (matricula,)
        ).fetchone()
