from datetime import datetime


class QrCode:
    def __init__(self, id_token, token, valor, validade_data):
        self.id_token = id_token
        self.token = token
        self.valor = valor
        self.validade_data = validade_data
        self.validade = True

        self.verifica_validade()

    def get_token(self):
        return self.token

    def set_validade_data(self, validade_data):
        self.validade_data = validade_data
        self.verifica_validade()

    def set_validade(self, validade):
        self.validade = validade

    def verifica_validade(self):
        if self.validade_data < datetime.now():
            self.validade = False
            return False

    def to_json(self):
        return {
            "id_token": self.id_token,
            "token": self.token,
            "valor": self.valor,
            "validade_data": self.validade_data,
            "validade": self.validade
        }

    def __str__(self):
        return f"QrCode[id_token={self.id_token}, token={self.token}, valor={self.valor}, validade_data={self.validade_data}, validade={self.validade}]"

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def from_json(json):
        return QrCode(
            json["id_token"],
            json["token"],
            json["valor"],
            json["validade_data"],
            json["validade"]
        )
