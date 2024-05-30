from flaskr.db import get_db
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
    def insert_grupo(nome, valor_max, criador_matricula):
        """
        Insere um grupo no banco de dados
        :param nome: nome do grupo
        :param valor_max: valor máximo de saldo que um aluno pode ter no grupo
        :param criador_matricula: matrícula do criador do grupo
        :return: True se o grupo foi inserido com sucesso, False caso contrário
        """
        db = get_db()
        try:
            db.execute(
                "INSERT INTO grupo (nome, valor_max, criador_matricula) VALUES (?, ?, ?)",
                (nome, valor_max, criador_matricula),
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
            grupo = Grupo(result['id_grupo'], result['nome'], result['valor_max'], result['criador_matricula'])
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
                lista.append(Grupo(grupo['id_grupo'], grupo['nome'], grupo['valor_max'], grupo['criador_matricula']))
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
