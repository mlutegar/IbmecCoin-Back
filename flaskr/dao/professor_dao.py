from flaskr.db import get_db

class ProfessorDao:
    def __init__(self):
        self.db = get_db()

    def insert(self, matricula, senha):
        try:
            self.db.execute(
                "INSERT INTO professor (matricula, senha) VALUES (?, ?)",
                (matricula, senha),
            )
            self.db.commit()
        except self.db.IntegrityError:
            return f"User {matricula} is already registered."
        return None

    def select(self, matricula):
        return self.db.execute(
            "SELECT * FROM professor WHERE matricula = ?", (matricula,)
        ).fetchone()

    def select_all(self):
        return self.db.execute(
            "SELECT * FROM professor"
        ).fetchall()