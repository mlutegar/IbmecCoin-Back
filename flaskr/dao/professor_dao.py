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

    def get_professor(self, matricula):
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
                user.email,
            )
            if resultado['turma_id']:
                professor.set_turma_id(resultado['turma_id'])
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
                user.email,
            )
            if row['turma_id']:
                professor.set_turma_id(row['turma_id'])
            professores.append(professor)

        return professores

    def update_professor(self, matricula, **kwargs):
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
