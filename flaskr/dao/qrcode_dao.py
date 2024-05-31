from flaskr.utils.db import get_db
from flaskr.entities.qr_code import QrCode


class QrCodeDAO:
    """
    Classe que representa o DAO de QR Code

    Métodos
    - insert_qrcode: insere um novo token
    - get_qrcode: recupera um token
    - get_last_qrcode: recupera o último token gerado
    - get_all_qrcode: recupera todos os tokens
    - update_qrcode: atualiza um token
    """

    def __init__(self):
        self.lista_qrcode = self.__inicializa_qrcode()

    def insert_qrcode(self, token: str, valor: int, validade_data, qtd_usos):
        """
        Função que insere um novo token
        :param token: token a ser inserido
        :param valor: valor do token
        :param validade_data: validade do token
        :param qtd_usos: quantidade de usos do token
        :return: True se o token foi inserido com sucesso, False caso contrário
        """
        qrcode = QrCode(self.__get_last_id_lista_qrcode() + 1, token, valor, qtd_usos, validade_data)

        db = get_db()
        try:
            db.execute(
                "INSERT INTO qrcode (token, valor, validade_data, qtd_usos, validade) VALUES (?, ?, ?, ?, ?)",
                (qrcode.token, qrcode.valor, qrcode.validade_data, qrcode.qtd_usos, qrcode.validade)
            )
            db.commit()
        except db.IntegrityError:
            return False
        return True

    @staticmethod
    def get_qrcode(token):
        """
        Função que recupera um token
        :param token: token a ser recuperado
        :return: token recuperado
        """
        db = get_db()
        resultado = db.execute(
            "SELECT * FROM qrcode WHERE token = ?", (token,)
        ).fetchone()

        if not resultado:
            return None

        token = QrCode(
            resultado['id_token'],
            resultado['token'],
            resultado['valor'],
            resultado['validade_data'],
            resultado['qtd_usos'],
        )

        return token

    @staticmethod
    def get_last_qrcode():
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

        return None

    @staticmethod
    def get_all_qrcode():
        """
        Função que recupera todos os tokens
        :return: lista de tokens recuperados
        """
        db = get_db()
        resultado = db.execute(
            "SELECT * FROM qrcode"
        ).fetchall()

        if not resultado:
            return None

        qrcodes = []

        for qr_code in resultado:
            qrcode = QrCode(
                qr_code['id_token'],
                qr_code['token'],
                qr_code['valor'],
                qr_code['validade_data'],
                qr_code['qtd_usos'],
                qr_code['validade']
            )
            qrcodes.append(qrcode)

        return qrcodes

    @staticmethod
    def update_qrcode(id_token, **kwargs):
        """
        Função que atualiza o token
        :param id_token: id do token
        :param kwargs: dicionário de campos a serem atualizados
        :return: True se o token foi atualizado com sucesso, False caso contrário
        """
        db = get_db()
        set_clause = ", ".join(f"{key} = ?" for key in kwargs)
        values = list(kwargs.values()) + [id_token]
        query = f"UPDATE qrcode SET {set_clause} WHERE id_token = ?"

        try:
            db.execute(query, values)
            db.commit()
        except db.IntegrityError:
            return False
        return True

    def __inicializa_qrcode(self):
        db = get_db()

        resultado = db.execute(
            "SELECT * FROM qrcode"
        ).fetchall()

        if not resultado:
            return None

        qr_codes = []

        for qr_code in resultado:
            qrcode = QrCode(
                qr_code['id_token'],
                qr_code['token'],
                qr_code['valor'],
                qr_code['validade_data'],
                qr_code['qtd_usos'],
                qr_code['validade']
            )
            qr_codes.append(qrcode)

        return qr_codes

    def __get_last_id_lista_qrcode(self):
        if self.lista_qrcode:
            return self.lista_qrcode[-1].id_token
        return 0
