from flaskr.db import get_db


class QrCodeDAO:

    def insert_qrcode(self, token, valor, validade):
        db = get_db()
        try:
            db.execute(
                "INSERT INTO qrcode (token, valor, validade) VALUES (?, ?, ?)",
                (token, valor, validade,)
            )
            db.commit()
        except db.IntegrityError:
            return f"Token {token} is already registered."
        return None

    def get_qrcode(self, token):
        db = get_db()
        return db.execute(
            "SELECT * FROM qrcode WHERE token = ?", (token,)
        ).fetchone()

    def get_lastqrcode(self):
        """
        Função que recupera o último token gerado
        :return: o último token gerado
        """
        db = get_db()
        token = db.execute(
            "SELECT * FROM qrcode ORDER BY id_token DESC LIMIT 1"
        ).fetchone()

        if token is not None:
            return token['token']

        return 0

    def get_all_qrcode(self):
        db = get_db()
        return db.execute(
            "SELECT * FROM qrcode"
        ).fetchall()

    def update_qrcode(self, id_token, **kwargs):
        """
        Função que atualiza o token
        :param id_token: id do token
        :param kwargs: dicionário de campos a serem atualizados
        :return: True se o token foi atualizado com sucesso, False caso contrário
        """
        db = get_db()
        set_clause = ", ".join(f"{key} = ?" for key in kwargs)
        values = list(kwargs.values()) + [id_token]
        query = f"UPDATE token_qr_code SET {set_clause} WHERE id_token = ?"

        try:
            db.execute(query, values)
            db.commit()
        except db.IntegrityError:
            return False
        return True
