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
    def insert_grupo(nome, valor_max, descricao, criador_matricula):
        """
        Insere um grupo no banco de dados
        :param nome: nome do grupo
        :param valor_max: valor máximo de saldo que um aluno pode ter no grupo
        :param descricao: descrição do grupo
        :param criador_matricula: matrícula do criador do grupo
        :return: True se o grupo foi inserido com sucesso, False caso contrário
        """
        db = get_db()
        try:
            db.execute(
                "INSERT INTO grupo (nome, quantidade_max, descricao, criador_matricula) VALUES (?, ?, ?, ?)",
                (nome, valor_max, descricao, criador_matricula),
            )
            db.commit()
        except db.IntegrityError:
            return False
        return True

    @staticmethod
    def get_grupo_by_id(id_grupo):
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
                result['criador_matricula'],
                alunos
            )
            return grupo
        return None

    @staticmethod
    def get_grupo_by_matricula(matricula):
        """
        Seleciona um grupo no banco de dados.
        :param matricula: Matrícula do criador do grupo
        :return: Objeto do tipo Grupo, ou None se o grupo não for encontrado
        """
        db = get_db()
        query = "SELECT * FROM grupo WHERE criador_matricula = ?"
        result = db.execute(query, (matricula,)).fetchone()
        if result:
            alunos = AlunoDAO().get_all_aluno_by_id_grupo(result['id_grupo'])
            grupo = Grupo(
                result['id_grupo'],
                result['nome'],
                result['descricao'],
                result['criador_matricula'],
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
                    grupo['criador_matricula'],
                    alunos
                )
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
    def convidar_aluno(destinatario, grupo):
        """
        Convida um aluno para um grupo
        :param destinatario: Aluno destinatário
        :param grupo: Objeto do tipo Grupo
        :return: True se o convite foi enviado com sucesso, False caso contrário
        """
        db = get_db()
        try:
            db.execute(
                "INSERT INTO convite (grupo_id, convidado_matricula) VALUES (?, ?)",
                (grupo.id_grupo, destinatario.matricula),
            )
            db.commit()
        except db.IntegrityError:
            return False
        return True
