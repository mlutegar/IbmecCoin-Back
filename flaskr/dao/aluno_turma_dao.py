from flaskr.entities.aluno_turma import AlunoTurma
from flaskr.utils.db import get_db


class AlunoTurmaDAO:
    """
    Classe DAO para a entidade Aluno Turma

    :author: Michel Lutegar

    :method create: Cria uma nova relação entre aluno e turma
    :method get_all_alunos_by_id_turma: Retorna uma lista de alunos que estão inscritos em uma turma
    :method get_all_turmas_by_id_aluno: Retorna uma lista de turmas que um aluno está inscrito
    """

    def create(self, aluno_matricula: int, turma_id: int):
        """
        Cria uma nova relação entre aluno e turma. Ele cria um objeto AlunoTurma e insere no banco de dados.

        :param aluno_matricula: int
        :param turma_id: int

        :return: AlunoTurma
        """
        obj = AlunoTurma(0, aluno_matricula=aluno_matricula, turma_id=turma_id, saldo=0)

        db = get_db()
        cursor = db.cursor()
        cursor.execute(""
                       "INSERT INTO aluno_turma (aluno_matricula, turma_id, saldo) "
                       "VALUES (?, ?, ?)",
                       (obj.aluno_matricula, obj.turma_id, obj.saldo)
                       )
        db.commit()
        obj.id_aluno_turma = cursor.lastrowid
        return obj

    def get_saldo_aluno(self, matricula: int, id_turma: int):
        """
        Retorna o saldo de um aluno em uma turma.

        :param matricula: int
        :param id_turma: int

        :return: int
        """
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT saldo FROM aluno_turma WHERE aluno_matricula=? AND turma_id=?", (matricula, id_turma))
        saldo = cursor.fetchone()
        return saldo[0] if saldo else None


