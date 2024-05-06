from flaskr.db import get_db

class TokenQrCodeDao:
    def __init__(self):
        self.db = get_db()

    def insert(self, token):
        try:
            self.db.execute(
                "INSERT INTO token_qr_code (token) VALUES (?)",
                (token),
            )
            self.db.commit()
        except self.db.IntegrityError:
            return f"Token {token} is already registered."
        return None

    def select(self, token):
        return self.db.execute(
            "SELECT * FROM token_qr_code WHERE token = ?", (token,)
        ).fetchone()

    def select_all(self):
        return self.db.execute(
            "SELECT * FROM token_qr_code"
        ).fetchall()

    def ativar(self, token):
        self.db.execute(
            "UPDATE token_qr_code SET ativo = 1 WHERE token = ?", (token,)
        )
        self.db.commit()
        return None

    def desativar(self, token):
        self.db.execute(
            "UPDATE token_qr_code SET ativo = 0 WHERE token = ?", (token,)
        )
        self.db.commit()
        return None