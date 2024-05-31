from flaskr.entities.user import User


class Professor(User):
    def __init__(self, matricula, senha, nome, email):
        super().__init__(matricula, senha, "professor", nome, email)
        self.id_turma = None

    def set_id_turma(self, id_turma):
        self.id_turma = id_turma

    def __str__(self):
        return f"Professor {self.matricula} {self.nome} {self.email} {self.senha} {self.tipo} {self.id_turma}"

    def __repr__(self):
        return f"Professor {self.matricula} {self.nome} {self.email} {self.senha} {self.tipo} {self.id_turma}"

    def to_dict(self):
        user_dict = super().to_dict()
        user_dict.update({
            "id_turma": self.id_turma
        })
        return user_dict

    def to_dict_without_senha(self):
        user_dict = super().to_dict_without_senha()
        user_dict.update({
            "id_turma": self.id_turma
        })
        return user_dict
