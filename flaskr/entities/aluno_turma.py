class AlunoTurma:
    """
    Entidade Aluno Turma

    Atributos:
    - id_aluno_turma: int
    - aluno_matricula: int
    - turma_id: int
    - saldo: int
    """

    def __init__(self, id_aluno_turma: int, aluno_matricula: int, turma_id: int, saldo: int):
        self.id_aluno_turma = id_aluno_turma
        self.aluno_matricula = aluno_matricula
        self.turma_id = turma_id
        self.saldo = saldo
