class Convite:
    def __init__(self, id_convite, grupo_id, convidado_matricula):
        self.id_convite = id_convite
        self.grupo_id = grupo_id
        self.convidado_matricula = convidado_matricula

    def to_json(self):
        return {
            "id_convite": self.id_convite,
            "grupo_id": self.grupo_id,
            "convidado_matricula": self.convidado_matricula
        }