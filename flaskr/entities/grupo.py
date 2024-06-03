from flaskr.dao.aluno_dao import AlunoDAO


class Grupo:
    """
    Classe que representa um grupo de estudo
    """

    def __init__(self, id_grupo, nome, descricao, quantidade_max, matricula, membros: list = None):
        """
        Construtor da classe Grupo

        :param id_grupo: id do grupo
        :param nome: nome do grupo
        :param descricao: descrição do grupo
        :param quantidade_max: quantidade máxima de membros do grupo
        :param matricula: id do criador do grupo
        :param membros: lista de membros do grupo
        """
        self.id_grupo = id_grupo
        self.nome = nome
        self.descricao = descricao
        self.quantidade_max = quantidade_max
        self.matricula_criador = matricula
        self.membros = membros

    def __dict__(self):
        """
        Método que transforma o objeto em um dicionário

        :return: dicionário com os atributos do objeto
        """
        return {
            "id_grupo": self.id_grupo,
            "nome": self.nome,
            "descricao": self.descricao,
            "criador_id": self.matricula_criador,
            "membros": [membro.__dict__() for membro in self.membros] if self.membros else []
        }
