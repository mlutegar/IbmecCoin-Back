from flaskr.dao.aluno_dao import AlunoDAO
from flaskr.entities.turma import Turma
from flaskr.utils.db import get_db


class TurmaDAO:
    def __init__(self):
        self.__turmas = self.__inicializar_turmas()

    def criar_turma(self, nome: str, professor_id: int):
        turma = Turma(int(self.get_last_id_turma()) + 1, nome, professor_id, [])
        self.__turmas.append(turma)

        db = get_db()

        db.execute(
            "INSERT INTO turma (nome, professor_id) VALUES (?, ?)",
            (nome, professor_id)
        )

        db.commit()

        return turma

    def listar_turmas(self):
        return self.__turmas

    def adicionar_turma(self, turma):
        self.__turmas.append(turma)

    def get_turma_by_id(self, id_turma: int):
        for turma in self.__turmas:
            if turma.id_turma == id_turma:
                return turma
        return None

    def remover_turma(self, turma):
        self.__turmas.remove(turma)

    def __inicializar_turmas(self):
        db = get_db()
        resultado = db.execute(
            "SELECT * FROM turma"
        ).fetchall()

        if not resultado:
            return []

        turmas = []
        for row in resultado:
            alunos = AlunoDAO().get_all_alunos_by_turma_id(row['id_turma'])

            turma = Turma(
                row['turma_id'],
                row['nome'],
                row['professor'],
                alunos
            )
            turmas.append(turma)

        return turmas

    def get_last_id_turma(self):
        db = get_db()
        return db.execute(
            "SELECT MAX(id_turma) FROM turma"
        ).fetchone()

