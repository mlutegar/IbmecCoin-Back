class Convite:
    def __init__(self, id_convite, id_grupo, convidado_matricula):
        self.id_convite = id_convite
        self.id_grupo = id_grupo
        self.convidado_matricula = convidado_matricula

    def __dict__(self):
        return {
            "id_convite": self.id_convite,
            "id_grupo": self.id_grupo,
            "convidado_matricula": self.convidado_matricula
        }