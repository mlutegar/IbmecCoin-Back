class Convite:
    def __init__(self, id_convite, id_grupo, id_turma, convidado_matricula):
        self.id_convite = id_convite
        self.id_grupo = id_grupo
        self.id_turma = id_turma
        self.convidado_matricula = convidado_matricula

    def __dict__(self):
        return {
            "id_convite": self.id_convite,
            "id_grupo": self.id_grupo,
            "id_turma": self.id_turma,
            "convidado_matricula": self.convidado_matricula
        }
