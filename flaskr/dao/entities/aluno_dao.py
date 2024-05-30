from flaskr.dao.entities.user_dao import UserDao
from flaskr.db import get_db
from flaskr.entities.aluno import Aluno


class AlunoDao(UserDao):
    """
    Classe que representa o DAO de aluno.
    """

    @staticmethod
    def insert_aluno(matricula, senha, tipo, email):
        """
        Insere um aluno no banco de dados.
        :param matricula: matrícula do aluno
        :param senha: senha do aluno
        :param tipo: tipo do aluno
        :param email: email do aluno
        :return: True se o aluno foi inserido com sucesso, False caso contrário
        """
        super().insert_user(matricula, senha, tipo, email)

        db = get_db()
        try:
            db.execute(
                "INSERT INTO aluno (matricula) VALUES (?)",
                (matricula,),
            )
            db.commit()
        except db.IntegrityError:
            return False
        return True

    @staticmethod
    def select_aluno_by_matricula(matricula):
        """
        Seleciona um aluno no banco de dados.
        :param matricula: matrícula do aluno
        :return: Objeto do tipo Aluno, ou None se o aluno não for encontrado
        """
        db = get_db()
        resultado = db.execute(
            "SELECT * FROM aluno WHERE id_user = ?", (matricula,)
        ).fetchone()

        if resultado:
            aluno = Aluno(
                resultado['matricula'],
                resultado['senha'],
                resultado['tipo'],
                resultado['nome'],
                resultado['email'],
                resultado['grupo_id'],
                resultado['saldo'],
                resultado['turma_id']
            )
            return aluno
        return None

    @staticmethod
    def select_all():
        """
        Seleciona todos os alunos no banco de dados.
        :return: Lista de objetos do tipo Aluno, ou None se não houver alunos
        """
        db = get_db()
        resultado = db.execute(
            "SELECT * FROM aluno"
        ).fetchall()

        if not resultado:
            return None

        alunos = []
        for row in resultado:
            aluno = Aluno(
                row['matricula'],
                row['senha'],
                row['tipo'],
                row['nome'],
                row['email'],
                row['grupo_id'],
                row['saldo'],
                row['turma_id']
            )
            alunos.append(aluno)

        return alunos

    @staticmethod
    def update_aluno(matricula, **kwargs):
        """
        Atualiza os campos de um usuário no banco de dados com base nos argumentos fornecidos.
        :param matricula: Matrícula do usuário
        :param kwargs: Dicionário de campos a serem atualizados
        :return: True se o usuário foi atualizado com sucesso, False caso contrário
        """
        super().update_user(matricula, **kwargs)
        db = get_db()
        set_clause = ", ".join(f"{key} = ?" for key in kwargs)
        values = list(kwargs.values()) + [matricula]
        query = f"UPDATE aluno SET {set_clause} WHERE matricula = ?"
        try:
            db.execute(query, values)
            db.commit()
        except db.IntegrityError:
            return False
        return True
