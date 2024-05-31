from flaskr.dao.user_dao import UserDAO
from flaskr.utils.db import get_db
from flaskr.entities.aluno import Aluno


class AlunoDAO(UserDAO):
    """
    Classe que representa o DAO de aluno.

    Métodos:
    - insert_aluno(matricula, senha, tipo, email): insere um aluno no banco de dados
    - get_aluno_by_matricula(matricula): seleciona um aluno no banco de dados
    - get_all(): seleciona todos os alunos no banco de dados
    - get_all_aluno_by_grupo_id(grupo_id): seleciona todos os alunos no banco de dados de um grupo específico
    - update_aluno(matricula, **kwargs): atualiza os campos de um aluno no banco de dados com base nos argumentos fornecidos
    """

    def insert_aluno(self, nome, matricula, senha, email):
        """
        Insere um aluno no banco de dados.
        :param nome: nome do aluno
        :param matricula: matrícula do aluno
        :param senha: senha do aluno
        :param email: email do aluno
        :return: True se o aluno foi inserido com sucesso, False caso contrário
        """
        if not super().insert_user(nome, matricula, senha, "aluno", email):
            return False

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

    def get_aluno(self, matricula):
        """
        Seleciona um aluno no banco de dados.
        :param matricula: matrícula do aluno
        :return: Objeto do tipo Aluno, ou None se o aluno não for encontrado
        """
        user = super().get_user(matricula)

        if not user:
            return None

        db = get_db()
        resultado = db.execute(
            "SELECT * FROM aluno WHERE matricula = ?", (matricula,)
        ).fetchone()

        if resultado:
            aluno = Aluno(
                user.matricula,
                user.senha,
                user.nome,
                user.email,
                resultado['grupo_id'],
                resultado['saldo'],
                resultado['id_turma']
            )
            return aluno
        return None

    def get_all_alunos(self):
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
            user = super().get_user(row['matricula'])

            aluno = Aluno(
                user.matricula,
                user.senha,
                user.nome,
                user.email,
                row['grupo_id'],
                row['saldo'],
                row['id_turma']
            )
            alunos.append(aluno)

        return alunos

    def get_all_aluno_by_id_grupo(self, grupo_id):
        """
        Seleciona todos os alunos no banco de dados de um grupo específico.
        :return: Lista de objetos do tipo Aluno, ou None se não houver alunos
        """
        db = get_db()
        resultado = db.execute(
            "SELECT * FROM aluno WHERE grupo_id = ?", (grupo_id,)
        ).fetchall()

        if not resultado:
            return None

        alunos = []
        for row in resultado:
            user = super().get_user(row['matricula'])

            aluno = Aluno(
                user.matricula,
                user.senha,
                user.nome,
                user.email,
                row['grupo_id'],
                row['saldo'],
                row['id_turma']
            )
            alunos.append(aluno)

        return alunos

    def get_all_alunos_by_id_turma(self, id_turma):
        """
        Seleciona todos os alunos no banco de dados de uma turma específica.
        :return: Lista de objetos do tipo Aluno, ou None se não houver alunos
        """
        db = get_db()
        resultado = db.execute(
            "SELECT * FROM aluno WHERE id_turma = ?", (id_turma,)
        ).fetchall()

        if not resultado:
            return None

        alunos = []
        for row in resultado:
            user = super().get_user(row['matricula'])

            aluno = Aluno(
                user.matricula,
                user.senha,
                user.nome,
                user.email,
                row['grupo_id'],
                row['saldo'],
                row['id_turma']
            )
            alunos.append(aluno)

        return alunos

    def update_aluno(self, matricula, **kwargs):
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

    def update_aumentar_saldo(self, matricula, valor):
        """
        Atualiza o saldo de um aluno no banco de dados.
        :param matricula: Matrícula do aluno
        :param valor: Valor a ser adicionado ao saldo
        :return: True se o saldo foi atualizado com sucesso, False caso contrário
        """
        db = get_db()
        try:
            db.execute(
                "UPDATE aluno SET saldo = saldo + ? WHERE matricula = ?",
                (valor, matricula)
            )
            db.commit()
        except db.IntegrityError:
            return False
        return True

    def update_diminuir_saldo(self, matricula, valor):
        """
        Atualiza o saldo de um aluno no banco de dados.
        :param matricula: Matrícula do aluno
        :param valor: Valor a ser subtraído do saldo
        :return: True se o saldo foi atualizado com sucesso, False caso contrário
        """
        db = get_db()
        try:
            db.execute(
                "UPDATE aluno SET saldo = saldo - ? WHERE matricula = ?",
                (valor, matricula)
            )
            db.commit()
        except db.IntegrityError:
            return False
        return True

    def update_aluno_turma(self, matricula, id_turma):
        """
        Atualiza a turma de um aluno no banco de dados.
        :param matricula: Matrícula do aluno
        :param id_turma: ID da turma
        :return: True se a turma foi atualizada com sucesso, False caso contrário
        """
        db = get_db()
        try:
            db.execute(
                "UPDATE aluno SET id_turma = ? WHERE matricula = ?",
                (id_turma, matricula)
            )
            db.commit()
        except db.IntegrityError:
            return False
        return True
