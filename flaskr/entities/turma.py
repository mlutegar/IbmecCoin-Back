from flaskr.entities.professor import Professor


class Turma:
    def __init__(self, id_turma: int, nome: str, professor: Professor, alunos: list):
        self.id_turma = id_turma
        self.nome = nome
        self.professor = professor
        self.turma = alunos

    def get_quantidade_turma(self):
        if self.turma is None:
            return 0
        return len(self.turma)

    def __str__(self):
        return f"Turma {self.nome} - Professor {self.professor.nome} - Alunos {self.get_quantidade_turma()}"