from flaskr.db import get_db
from flaskr.dao.user_dao import UserDao
from flaskr.entities.professor import Professor


class ProfessorDao(UserDao):
    """
    Classe que representa o DAO de professor.

    Métodos
    """

    @staticmethod
    def insert_professor(matricula, senha, tipo, email):
        """
        Insere um professor no banco de dados.
        :param matricula: Matrícula do professor
        :param senha: Senha do professor
        :param tipo: Tipo do professor
        :param email: Email do professor
        :return: True se o professor foi inserido com sucesso, False caso contrário
        """
        super().insert_user(matricula, senha, tipo, email)

        db = get_db()

        try:
            db.execute(
                "INSERT INTO professor (matricula) VALUES (?)",
                (matricula,),
            )
            db.commit()
        except db.IntegrityError:
            return False
        return True

    @staticmethod
    def get_professor(matricula):
        """
        Seleciona um professor no banco de dados.
        :param matricula: Matrícula do professor
        :return: Objeto do tipo Professor, ou None se o professor não for encontrado
        """
        db = get_db()

        try:
            resultado = db.execute(
                "SELECT * FROM professor WHERE matricula = ?", (matricula,)
            ).fetchone()
        except db.IntegrityError:
            return None

        if resultado:
            professor = Professor(
                resultado['matricula'],
                resultado['senha'],
                resultado['tipo'],
                resultado['nome'],
                resultado['email'],
            )
            if resultado['turma_id']:
                professor.set_turma_id(resultado['turma_id'])
            return professor
        return None

    @staticmethod
    def get_all_professor():
        """
        Seleciona todos os professores no banco de dados.
        :return: Lista de objetos do tipo Professor, ou None se não houver professores
        """
        db = get_db()

        resultado = db.execute(
            "SELECT * FROM professor"
        ).fetchall()

        if not resultado:
            return None

        professores = []
        for row in resultado:
            professor = Professor(
                row['matricula'],
                row['senha'],
                row['tipo'],
                row['nome'],
                row['email'],
            )
            if row['turma_id']:
                professor.set_turma_id(row['turma_id'])
            professores.append(professor)

        return professores

    @staticmethod
    def update_professor(matricula, **kwargs):
        """
        Atualiza os campos de um professor no banco de dados com base nos argumentos fornecidos.
        :param matricula: Matrícula do professor
        :param kwargs: Dicionário de campos a serem atualizados
        :return: True se o professor foi atualizado com sucesso, False caso contrário
        """
        super().update_user(matricula, **kwargs)

        db = get_db()
        set_clause = ", ".join(f"{key} = ?" for key in kwargs)
        values = list(kwargs.values()) + [matricula]
        query = f"UPDATE professor SET {set_clause} WHERE matricula = ?"

        try:
            db.execute(query, values)
            db.commit()
        except db.IntegrityError:
            return False
        return True
