from flaskr.db import get_db

class ProfessorDao:
    def __init__(self):
        pass

    def insert(self, id_user):
        db = get_db()
        try:
            db.execute(
                "INSERT INTO professor (id_user) VALUES (?)",
                (id_user,),
            )
            db.commit()
        except db.IntegrityError:
            print(f"User {id_user} is already registered.")
            return -1
        return None

    def select(self, id_user):
        db = get_db()

        return db.execute(
            "SELECT * FROM professor WHERE id_user = ?", (id_user,)
        ).fetchone()

    def select_all(self):
        db = get_db()

        return db.execute(
            "SELECT * FROM professor"
        ).fetchall()
