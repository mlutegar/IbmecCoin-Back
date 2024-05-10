from flaskr.db import get_db

class ProfessorDao:
    def __init__(self):
        self.db = get_db()

    def insert(self, id_user):
        try:
            self.db.execute(
                "INSERT INTO professor (id_user) VALUES (?,)",
                (id_user,),
            )
            self.db.commit()
        except self.db.IntegrityError:
            return f"User {id_user} is already registered."
        return None

    def select(self, id_user):
        return self.db.execute(
            "SELECT * FROM professor WHERE id_user = ?", (id_user,)
        ).fetchone()

    def select_all(self):
        return self.db.execute(
            "SELECT * FROM professor"
        ).fetchall()
