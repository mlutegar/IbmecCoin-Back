from datetime import datetime


class QrCode:
    def __init__(self, id_token, token, valor, validade_data, qtd_usos, validade=True):
        self.id_token = id_token
        self.token = token
        self.valor = valor
        self.validade_data = validade_data
        self.qtd_usos = qtd_usos
        self.verifica_validade()
        self.validade = validade

    def verifica_validade(self):
        if isinstance(self.validade_data, str):
            self.validade_data = datetime.strptime(self.validade_data, "%Y-%m-%d %H:%M:%S")
        elif isinstance(self.validade_data, int):
            self.validade_data = datetime.fromtimestamp(self.validade_data)
        if self.validade_data < datetime.now():
            self.validade = False
            return False
        return True

    def to_dict(self):
        return {
            "id_token": self.id_token,
            "token": self.token,
            "valor": self.valor,
            "validade_data": self.validade_data,
            "qtd_usos": self.qtd_usos,
            "validade": self.validade
        }