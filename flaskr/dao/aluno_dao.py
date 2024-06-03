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
    - get_all_aluno_by_id_grupo(id_grupo): seleciona todos os alunos no banco de dados de um grupo específico
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
                resultado['id_grupo'],
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
                row['id_grupo'],
                row['saldo'],
                row['id_turma']
            )
            alunos.append(aluno)

        return alunos

    def get_all_aluno_by_id_grupo(self, id_grupo):
        """
        Seleciona todos os alunos no banco de dados de um grupo específico.
        :return: Lista de objetos do tipo Aluno, ou None se não houver alunos
        """
        db = get_db()
        resultado = db.execute(
            "SELECT * FROM aluno WHERE id_grupo = ?", (id_grupo,)
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
                row['id_grupo'],
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
                row['id_grupo'],
                row['saldo'],
                row['id_turma']
            )
            alunos.append(aluno)

        return alunos

    def update_aluno(self, aluno: Aluno):
        """
        Atualiza os campos de um usuário no banco de dados com base nos argumentos fornecidos.
        :param aluno: Objeto do tipo Aluno
        :return: True se o usuário foi atualizado com sucesso, False caso contrário
        """
        user = super().update_user(aluno)

        if not user:
            return False

        db = get_db()
        try:
            db.execute(
                "UPDATE aluno SET id_grupo = ?, saldo = ?, id_turma = ? WHERE matricula = ?",
                (aluno.id_grupo, aluno.saldo, aluno.id_turma, aluno.matricula)
            )
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

    def update_entrar_turma(self, matricula: int, id_turma: int):
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

    def update_entrar_grupo(self, id_grupo, convidado_matricula):
        """
        Aceita um convite no banco de dados.
        :param id_grupo: ID do grupo
        :param convidado_matricula: Matrícula do convidado
        :return: Retorna True se o convite foi aceito com sucesso, False caso contrário.
        """
        db = get_db()
        try:
            db.execute(
                "UPDATE aluno SET id_grupo = ? WHERE matricula = ?",
                (id_grupo, convidado_matricula),
            )
            db.commit()
        except db.IntegrityError:
            return False
        return True

    def update_sair_grupo(self, matricula):
        """
        Remove um aluno de um grupo no banco de dados.
        :param matricula: Matrícula do aluno
        :return: Retorna True se o aluno foi removido do grupo com sucesso, False caso contrário.
        """
        db = get_db()
        try:
            db.execute(
                "UPDATE aluno SET id_grupo = NULL WHERE matricula = ?",
                (matricula,),
            )
            db.commit()
        except db.IntegrityError:
            return False
        return True