from flaskr.entities.convite import Convite
from flaskr.utils.db import get_db


class ConviteDAO:
    """
    Classe responsável por realizar a comunicação com o banco de dados para a entidade Convite.
    """
    @staticmethod
    def insert_convite(grupo_id, convidado_matricula):
        """
        Insere um convite no banco de dados.
        :param grupo_id: O id do grupo que o convite pertence.
        :param convidado_matricula: A matrícula do usuário convidado.
        :return: Retorna True se o convite foi inserido com sucesso, False caso contrário.
        """
        db = get_db()
        try:
            db.execute(
                "INSERT INTO convite (grupo_id, convidado_matricula) VALUES (?, ?)",
                (grupo_id, convidado_matricula),
            )
            db.commit()
        except db.IntegrityError:
            return False
        return True

    @staticmethod
    def get_convite(matricula):
        """
        Busca um convite no banco de dados.
        :param matricula: A matrícula do usuário convidado.
        :return: Retorna um objeto do tipo Convite se o convite foi encontrado, None caso contrário.
        """
        db = get_db()
        query = "SELECT * FROM convite WHERE convidado_matricula = ?"
        result = db.execute(query, (matricula,)).fetchone()
        if result:
            convite = Convite(result['id_convite'], result['grupo_id'], result['convidado_matricula'])
            return convite
        return None

    @staticmethod
    def get_all_convite():
        """
        Busca todos os convites no banco de dados.
        :return: Retorna uma lista de objetos do tipo Convite se os convites foram encontrados, None caso contrário.
        """
        db = get_db()
        result = db.execute(
            "SELECT * FROM convite"
        ).fetchall()
        if result:
            lista = []
            for convite in result:
                lista.append(Convite(convite['id_convite'], convite['grupo_id'], convite['convidado_matricula']))
            return lista
        return None

    @staticmethod
    def delete_convite(id_convite):
        """
        Deleta um convite no banco de dados.
        :param id_convite: O id do convite a ser deletado.
        :return: Retorna True se o convite foi deletado com sucesso, False caso contrário.
        """
        db = get_db()
        try:
            db.execute(
                "DELETE FROM convite WHERE id_convite = ?",
                (id_convite,),
            )
            db.commit()
        except db.IntegrityError:
            return False
        return True

    @staticmethod
    def get_convite_by_grupo_id(grupo_id):
        """
        Busca todos os convites de um grupo no banco de dados.
        :param grupo_id: O id do grupo.
        :return: Retorna uma lista de objetos do tipo Convite se os convites foram encontrados, None caso contrário.
        """
        db = get_db()
        query = "SELECT * FROM convite WHERE grupo_id = ?"
        result = db.execute(query, (grupo_id,)).fetchall()
        if result:
            lista = []
            for convite in result:
                lista.append(Convite(convite['id_convite'], convite['grupo_id'], convite['convidado_matricula']))
            return lista
        return None
