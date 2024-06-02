from flaskr.entities.professor import Professor


class Turma:
    """
    Entidade Turma

    Atributos:
    - id_turma: int
    - nome: str
    - professor: Professor
    - turma: list[Aluno]
    """
    def __init__(self, id_turma: int, nome: str, professor: Professor, alunos: list):
        self.id_turma = id_turma
        self.nome = nome
        self.professor = professor
        self.turma = alunos

    def get_quantidade_turma(self):
        if self.turma is None:
            return 0
        return len(self.turma)

    def to_dict(self):
        return {
            'id_turma': self.id_turma,
            'nome': self.nome,
            'professor': self.professor.to_dict(),
            'turma': [aluno.to_dict() for aluno in self.turma]
        }