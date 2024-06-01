from flaskr.utils.db import get_db
from flaskr.dao.user_dao import UserDAO
from flaskr.entities.professor import Professor


class ProfessorDAO(UserDAO):
    """
    Classe que representa o DAO de professor.

    Métodos
    """

    def insert_professor(self, nome, matricula, senha, email):
        """
        Insere um professor no banco de dados.
        :param nome: Nome do professor
        :param matricula: Matrícula do professor
        :param senha: Senha do professor
        :param email: Email do professor
        :return: True se o professor foi inserido com sucesso, False caso contrário
        """
        super().insert_user(nome, matricula, senha, "professor", email)

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

    def get_professor(self, matricula: int):
        """
        Seleciona um professor no banco de dados.
        :param matricula: Matrícula do professor
        :return: Objeto do tipo Professor, ou None se o professor não for encontrado
        """
        user = super().get_user(matricula)
        if not user:
            return None

        db = get_db()

        try:
            resultado = db.execute(
                "SELECT * FROM professor WHERE matricula = ?", (matricula,)
            ).fetchone()
        except db.IntegrityError:
            return None

        if resultado:
            professor = Professor(
                user.matricula,
                user.senha,
                user.nome,
                user.email
            )
            return professor
        return None

    def get_all_professor(self):
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
            user = super().get_user(row['matricula'])

            professor = Professor(
                user.matricula,
                user.senha,
                user.nome,
                user.email
            )
            professores.append(professor)
        return professores
