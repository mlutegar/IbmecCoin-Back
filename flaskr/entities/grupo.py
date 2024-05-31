from flaskr.dao.aluno_dao import AlunoDAO


class Grupo:
    """
    Classe que representa um grupo de estudo
    """

    def __init__(self, id_grupo, nome, descricao, matricula, membros=None):
        """
        Construtor da classe Grupo

        :param id_grupo: id do grupo
        :param nome: nome do grupo
        :param descricao: descrição do grupo
        :param matricula: id do criador do grupo
        :param membros: lista de membros do grupo
        """
        self.id_grupo = id_grupo
        self.nome = nome
        self.descricao = descricao
        self.criador_id = matricula
        self.membros = AlunoDAO().get_all_aluno_by_grupo_id(id_grupo)
        if membros is None:
            self.add_member(AlunoDAO().get_aluno(matricula))


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
