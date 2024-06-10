from flaskr.entities.aluno import Aluno
from flaskr.entities.item import Item
from flaskr.entities.professor import Professor


class Turma:
    """
    Entidade Turma

    Atributos:
    - id_turma: int
    - nome: str
    - professor: Professor
    - turma: list[tuple[Aluno, float]]
    """
    def __init__(
            self,
            id_turma: int,
            nome: str,
            professor: Professor,
            alunos: list[tuple[Aluno, float]],
            itens: list[Item]):
        self.id_turma = id_turma
        self.nome = nome
        self.professor = professor
        self.alunos = alunos  # alunos agora é uma lista de tuplas (Aluno, saldo_aluno)
        self.itens = itens if itens else []

    def get_quantidade_turma(self):
        if self.alunos is None:
            return 0
        return len(self.alunos)

    def __dict__(self):
        return {
            'id_turma': self.id_turma,
            'nome': self.nome,
            'professor': self.professor.__dict__(),
            'alunos': [{
                'aluno': aluno[0].__dict__(),
                'saldo_turma': aluno[1]} for aluno in self.alunos] if self.alunos else [],
            'itens': [item.__dict__() for item in self.itens]
        }

    def adicionar_aluno(self, aluno, saldo):
        self.alunos.append((aluno, saldo))
