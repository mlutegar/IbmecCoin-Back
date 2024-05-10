from flaskr.db import get_db

class TokenQrCodeDao:
    def __init__(self):
        pass

    def insert(self, token):
        db = get_db()
        try:
            db.execute(
                "INSERT INTO token_qr_code (token) VALUES (?)",
                (token,)
            )
            db.commit()
        except db.IntegrityError:
            return f"Token {token} is already registered."
        return None

    def select(self, token):
        db = get_db()
        return db.execute(
            "SELECT * FROM token_qr_code WHERE token = ?", (token,)
        ).fetchone()

    def select_last(self):
        """
        Função que recupera o último token gerado
        :return: o último token gerado
        """
        db = get_db()
        token = db.execute(
            "SELECT * FROM token_qr_code ORDER BY id_token DESC LIMIT 1"
        ).fetchone()

        if token is not None:
            return token['token']

        return 0

    def select_all(self):
        db = get_db()
        return db.execute(
            "SELECT * FROM token_qr_code"
        ).fetchall()

    def ativar(self, token):
        db = get_db()
        db.execute(
            "UPDATE token_qr_code SET ativo = 1 WHERE token = ?", (token,)
        )
        db.commit()
        return None

    def desativar(self, token):
        db = get_db()
        db.execute(
            "UPDATE token_qr_code SET ativo = 0 WHERE token = ?", (token,)
        )
        db.commit()
        return None