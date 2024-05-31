class Turma:
    def __init__(self, turma_id: int, nome: str, professor_id: int, alunos: list):
        self.id_turma = turma_id
        self.nome = nome
        self.professor = professor_id
        self.turma = alunos
