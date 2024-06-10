from flaskr.dao.aluno_dao import AlunoDAO
from flaskr.utils.db import get_db
from flaskr.entities.grupo import Grupo


class GrupoDAO:
    """
    Classe responsável por realizar operações no banco de dados relacionadas a entidade Grupo

    Métodos:
    - insert_grupo(nome, valor_max, criador_matricula): Insere um grupo no banco de dados
    - get_grupo_by_id(id_grupo): Seleciona um grupo no banco de dados
    - get_all_grupo(): Seleciona todos os grupos no banco de dados
    - update_grupo(id_grupo, **kwargs): Atualiza os campos de um grupo no banco de dados
    """

    @staticmethod
    def insert_grupo(nome, valor_max, descricao, criador_matricula, id_turma) -> Grupo | None:
        """
        Insere um grupo no banco de dados
        :param nome: nome do grupo
        :param valor_max: valor máximo de saldo que um aluno pode ter no grupo
        :param descricao: descrição do grupo
        :param criador_matricula: matrícula do criador do grupo
        :param id_turma: id da turma
        :return: Grupo inserido com sucesso, ou None em caso de falha
        """
        grupo = Grupo(
            None,
            nome,
            descricao,
            valor_max,
            criador_matricula,
            id_turma,
            []
        )

        db = get_db()
        try:
            cursor = db.execute(
                "INSERT INTO grupo (nome, quantidade_max, descricao, criador_matricula, id_turma) "
                "VALUES (?, ?, ?, ?, ?)",
                (grupo.nome, grupo.quantidade_max, grupo.descricao, grupo.matricula_criador, grupo.id_turma)
            )
            db.commit()
            grupo.id_grupo = cursor.lastrowid  # Atribui o ID gerado ao grupo
        except db.IntegrityError:
            return None

        return grupo

    def get_grupo_by_id(self, id_grupo):
        """
        Seleciona um grupo no banco de dados.
        :param id_grupo: Id do grupo
        :return: Objeto do tipo Grupo, ou None se o grupo não for encontrado
        """
        db = get_db()
        query = "SELECT * FROM grupo WHERE id_grupo = ?"
        result = db.execute(query, (id_grupo,)).fetchone()
        if result:
            alunos = AlunoDAO().get_all_aluno_by_id_grupo(id_grupo)
            grupo = Grupo(
                result['id_grupo'],
                result['nome'],
                result['descricao'],
                result['quantidade_max'],
                result['criador_matricula'],
                result['id_turma'],
                alunos
            )
            return grupo
        return None

    def get_grupo_by_matricula_aluno(self, matricula, id_turma):
        """
        Seleciona um grupo no banco de dados.

        :param matricula: Matrícula do criador do grupo
        :param id_turma: Id da turma

        :return: Objeto do tipo Grupo, ou None se o grupo não for encontrado
        """
        db = get_db()
        query = "SELECT id_grupo FROM aluno_turma WHERE aluno_matricula = ? AND turma_id = ?"
        result = db.execute(query, (matricula, id_turma)).fetchone()

        grupo = self.get_grupo_by_id(result['id_grupo'])

        if grupo:
            alunos = AlunoDAO().get_all_aluno_by_id_grupo(grupo.id_grupo)
            grupo = Grupo(
                grupo.id_grupo,
                grupo.nome,
                grupo.descricao,
                grupo.quantidade_max,
                grupo.matricula_criador,
                grupo.id_turma,
                alunos
            )
            return grupo
        return None

    @staticmethod
    def get_all_grupo():
        """
        Seleciona todos os grupos no banco de dados
        :return: Lista de objetos do tipo Grupo, ou None se não houver grupos
        """
        db = get_db()
        result = db.execute(
            "SELECT * FROM grupo"
        ).fetchall()
        if result:
            lista = []
            for grupo in result:
                alunos = AlunoDAO().get_all_aluno_by_id_grupo(grupo['id_grupo'])
                grupo = Grupo(
                    grupo['id_grupo'],
                    grupo['nome'],
                    grupo['descricao'],
                    grupo['quantidade_max'],
                    grupo['criador_matricula'],
                    grupo['id_turma'],
                    alunos
                )
                lista.append(grupo)
            return lista
        return None

    def get_all_grupos_by_matricula_aluno(self, matricula):
        """
        Seleciona todos os grupos no banco de dados
        :return: Lista de objetos do tipo Grupo, ou None se não houver grupos
        """
        db = get_db()
        query = "SELECT id_grupo FROM aluno_turma WHERE aluno_matricula = ?"
        result = db.execute(query, (matricula,)).fetchall()
        if result:
            lista = []
            for grupo in result:
                grupo = self.get_grupo_by_id(grupo['id_grupo'])
                if grupo:
                    lista.append(grupo)
            return lista
        return None

    @staticmethod
    def update_grupo(id_grupo, **kwargs):
        """
        Atualiza os campos de um grupo no banco de dados com base nos argumentos fornecidos.
        :param id_grupo: Id do grupo
        :param kwargs: Dicionário de campos a serem atualizados
        :return: True se o grupo foi atualizado com sucesso, False caso contrário
        """
        db = get_db()
        set_clause = ", ".join(f"{key} = ?" for key in kwargs)
        values = list(kwargs.values()) + [id_grupo]
        query = f"UPDATE grupo SET {set_clause} WHERE id_grupo = ?"
        try:
            db.execute(query, values)
            db.commit()
        except db.IntegrityError:
            return False
        return True

    @staticmethod
    def convidar_aluno(destinatario, grupo, id_turma):
        """
        Convida um aluno para um grupo
        :param destinatario: Aluno destinatário
        :param grupo: Objeto do tipo Grupo
        :param id_turma: Id da turma
        :return: True se o convite foi enviado com sucesso, False caso contrário
        """
        db = get_db()
        try:
            db.execute(
                "INSERT INTO convite (id_grupo, convidado_matricula, id_turma) VALUES (?, ?, ?)",
                (grupo.id_grupo, destinatario.matricula, id_turma),
            )
            db.commit()
        except db.IntegrityError:
            return False
        return True
