class Transacao:
    def __init__(self, emissor_id, receptor_id, valor, data):
        self.emissor_id = emissor_id
        self.receptor_id = receptor_id
        self.valor = valor
        self.data = data

    def __dict__(self):
        return {
            "emissor_id": self.emissor_id,
            "receptor_id": self.receptor_id,
            "valor": self.valor,
            "data": self.data
        }