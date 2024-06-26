from flaskr.entities.user import User


class Aluno(User):
    def __init__(self, matricula, senha, nome, email, id_grupo, saldo, id_turma):
        super().__init__(matricula, senha, "aluno", nome, email)
        self.id_grupo = id_grupo
        self.saldo = saldo
        self.id_turma = id_turma

    def get_id_grupo(self):
        return self.id_grupo

    def __dict__(self):
        user_dict = super().__dict__()
        user_dict.update({
            "id_grupo": self.id_grupo,
            "saldo": self.saldo,
            "id_turma": self.id_turma
        })
        return user_dict

    def to_dict_without_senha(self):
        user_dict = super().to_dict_without_senha()
        user_dict.update({
            "id_grupo": self.id_grupo,
            "saldo": self.saldo,
            "id_turma": self.id_turma
        })
        return user_dict
