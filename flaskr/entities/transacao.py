class Transacao:
    def __init__(self, emissor_id, receptor_id, valor, data):
        self.emissor_id = emissor_id
        self.receptor_id = receptor_id
        self.valor = valor
        self.data = data
