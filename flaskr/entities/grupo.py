from flaskr.dao.aluno_dao import AlunoDao


class Grupo:
    """
    Classe que representa um grupo de estudo

    :param id_grupo: id do grupo
    :param nome: nome do grupo
    :param descricao: descrição do grupo
    :param criador_id: id do criador do grupo
    """
    def __init__(self, id_grupo, nome, descricao, criador_id):
        """
        Construtor da classe Grupo

        :param id_grupo: id do grupo
        :param nome: nome do grupo
        :param descricao: descrição do grupo
        :param criador_id: id do criador do grupo
        """
        self.id_grupo = id_grupo
        self.nome = nome
        self.descricao = descricao
        self.criador_id = criador_id
        self.membros = AlunoDao().get_all_aluno_by_grupo_id(id_grupo)

    def add_member(self, aluno):
        """
        Adiciona um membro ao grupo

        :param aluno: objeto do tipo Aluno
        """
        self.membros.append(aluno)

    def get_group_descricao(self):
        """
        Retorna a descrição do grupo

        :return: descrição do grupo
        """
        return self.descricao

    def get_group_members(self):
        """
        Retorna os membros do grupo

        :return: lista de membros do grupo
        """
        return self.membros
