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
                resultado['saldo']
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
                row['saldo'],
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
            "SELECT aluno_matricula, saldo FROM aluno_turma WHERE id_grupo = ?", (id_grupo,)
        ).fetchall()

        if not resultado:
            return None

        alunos = []
        for row in resultado:
            user = self.get_aluno(row['aluno_matricula'])

            aluno = Aluno(
                user.matricula,
                user.senha,
                user.nome,
                user.email,
                row['saldo']
            )
            alunos.append(aluno)

        return alunos

    def get_all_alunos_by_id_turma(self, turma_id: int):
        """
        Retorna uma lista de alunos que estão inscritos em uma turma. Ele busca todos as relações aluno-turma no banco
        de dados pelo o id, e a partir do id do alunos ele cria uma lista de objetos Aluno e adiciona todos os alunos
        nessa lista. E retorna essa lista.

        :param turma_id: int

        :return: list
        """
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT aluno_matricula, saldo FROM aluno_turma WHERE turma_id=?", (turma_id,))
        alunos_turma = cursor.fetchall()

        tupla_aluno_saldo = []
        for aluno_turma in alunos_turma:
            aluno = self.get_aluno(aluno_turma[0])
            tupla_aluno_saldo.append((aluno, aluno_turma[1]))

        return tupla_aluno_saldo

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
                "UPDATE aluno_turma SET turma_id = ? WHERE aluno_matricula = ?",
                (id_turma, matricula),
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
                "INSERT INTO aluno_turma (aluno_matricula, turma_id) VALUES (?, ?)",
                (matricula, id_turma),
            )
            db.commit()
        except db.IntegrityError:
            return False
        return True

    def update_entrar_grupo(self, id_grupo, id_turma, convidado_matricula):
        """
        Aceita um convite no banco de dados.
        :param id_grupo: ID do grupo
        :param id_turma: ID da turma
        :param convidado_matricula: Matrícula do convidado
        :return: Retorna True se o convite foi aceito com sucesso, False caso contrário.
        """
        db = get_db()
        verificacao = self.update_sair_grupo(convidado_matricula, id_turma)
        try:
            if verificacao:
                db.execute(
                    "UPDATE aluno_turma SET id_grupo = ? WHERE aluno_matricula = ? AND turma_id = ?",
                    (id_grupo, convidado_matricula, id_turma),
                )
            else:
                db.execute(
                    "INSERT INTO aluno_turma (aluno_matricula, turma_id, id_grupo) VALUES (?, ?, ?)",
                    (convidado_matricula, id_turma, id_grupo),
                )
            db.commit()
        except db.IntegrityError as e:
            print(f'IntegrityError: {e}')
            return False
        return True

    def update_sair_grupo(self, matricula, id_turma):
        """
        Remove um aluno de um grupo no banco de dados.
        :param matricula: Matrícula do aluno
        :param id_turma: ID da turma
        :return: Retorna True se o aluno foi removido do grupo com sucesso, False caso contrário.
        """
        db = get_db()
        try:
            db.execute(
                "UPDATE aluno_turma SET id_grupo = NULL WHERE aluno_matricula = ? AND turma_id = ?",
                (matricula, id_turma),
            )
            db.commit()
        except db.IntegrityError:
            return False
        return True

    def verificar_aluno_turma(self, matricula, id_turma):
        """
        Verifica se um aluno está em uma turma.
        :param matricula: Matrícula do aluno
        :param id_turma: ID da turma
        :return: Retorna True se o aluno está na turma, False caso contrário.
        """
        db = get_db()
        resultado = db.execute(
            "SELECT * FROM aluno_turma WHERE aluno_matricula = ? AND turma_id = ?", (matricula, id_turma)
        ).fetchone()

        if resultado:
            return True
        return False

    def transferir_saldo_grupo(self, remetente_matricula, destinatario_matricula, quantidade, id_turma):
        """
        Transfere saldo de um aluno para outro aluno.
        :param remetente_matricula: Matrícula do remetente
        :param destinatario_matricula: Matrícula do destinatário
        :param quantidade: Quantidade de saldo a ser transferida
        :param id_turma: ID da turma
        :return: Retorna True se a transferência foi realizada com sucesso, False caso contrário.
        """
        db = get_db()
        try:
            db.execute(
                "UPDATE aluno_turma SET saldo = saldo - ? WHERE aluno_matricula = ? AND turma_id = ?",
                (quantidade, remetente_matricula, id_turma),
            )
            db.execute(
                "UPDATE aluno_turma SET saldo = saldo + ? WHERE aluno_matricula = ? AND turma_id = ?",
                (quantidade, destinatario_matricula, id_turma),
            )
            db.commit()
        except db.IntegrityError:
            return False
        return True