from flaskr.entities.professor import Professor


class Turma:
    def __init__(self, id_turma: int, nome: str, professor: Professor, alunos: list):
        self.id_turma = id_turma
        self.nome = nome
        self.professor = professor
        self.turma = alunos

    def get_quantidade_turma(self):
        return len(self.turma)
