from flaskr.entities.user import User


class Professor(User):
    def __init__(self, matricula, senha, nome, email):
        super().__init__(matricula, senha, "professor", nome, email)
        self.turma_id = None

    def set_turma_id(self, turma_id):
        self.turma_id = turma_id

    def __str__(self):
        return f"Professor {self.matricula} {self.nome} {self.email} {self.senha} {self.tipo} {self.turma_id}"

    def __repr__(self):
        return f"Professor {self.matricula} {self.nome} {self.email} {self.senha} {self.tipo} {self.turma_id}"

    def to_dict(self):
        user_dict = super().to_dict()
        user_dict.update({
            "turma_id": self.turma_id
        })
        return user_dict

    def to_dict_without_senha(self):
        user_dict = super().to_dict_without_senha()
        user_dict.update({
            "turma_id": self.turma_id
        })
        return user_dict
