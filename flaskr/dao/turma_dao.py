from flaskr.dao.aluno_dao import AlunoDAO
from flaskr.entities.turma import Turma
from flaskr.utils.db import get_db
from flaskr.dao.professor_dao import ProfessorDAO


class TurmaDAO:
    def __init__(self):
        self.lista_turmas = self.__inicializar_turmas()

    def insert_turma(self, nome: str, professor_matricula: int):
        professor = ProfessorDAO().get_professor(professor_matricula)

        turma = Turma(int(self.get_last_id_turma()) + 1, nome, professor, [])
        self.lista_turmas.append(turma)

        db = get_db()

        db.execute(
            "INSERT INTO turma (nome, professor_matricula) VALUES (?, ?)",
            (turma.nome, turma.professor.matricula)
        )

        db.commit()

        return turma

    def get_turma_by_id(self, id_turma: int):
        for turma in self.lista_turmas:
            if turma.id_turma == id_turma:
                return turma
        return None

    def get_turma_by_nome(self, nome: str) -> Turma:
        for turma in self.lista_turmas:
            if turma.nome == nome:
                return turma
        return None

    def get_all_turmas_by_professor_matricula(self, professor_matricula: int):
        turmas = []
        for turma in self.lista_turmas:
            if turma.professor.matricula == professor_matricula:
                turmas.append(turma)
        return turmas

    def remover_turma(self, turma):
        self.lista_turmas.remove(turma)
        
    def __inicializar_turmas(self):
        db = get_db()
        resultado = db.execute(
            "SELECT * FROM turma"
        ).fetchall()

        if not resultado:
            return []

        turmas = []
        for row in resultado:
            alunos = AlunoDAO().get_all_alunos_by_id_turma(row['id_turma'])
            professor = ProfessorDAO().get_professor(row['professor_matricula'])

            turma = Turma(
                row['id_turma'],
                row['nome'],
                professor,
                alunos
            )
            turmas.append(turma)

        return turmas

    def get_last_id_turma(self):
        if self.lista_turmas:
            return self.lista_turmas[-1].id_turma
        return 0
