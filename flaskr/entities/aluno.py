from flaskr.entities.user import User


class Aluno(User):
    def __init__(self, matricula, senha, nome, email, grupo_id, saldo, turma_id):
        super().__init__(matricula, senha, "aluno", nome, email)
        self.grupo_id = grupo_id
        self.saldo = saldo
        self.turma_id = turma_id

    def get_grupo_id(self):
        return self.grupo_id

    def __str__(self):
        return (f"Aluno {self.matricula} {self.nome} {self.email} {self.senha} {self.tipo} "
                f"{self.grupo_id} {self.saldo} {self.turma_id}")

    def __repr__(self):
        return (f"Aluno {self.matricula} {self.nome} {self.email} {self.senha} {self.tipo} "
                f"{self.grupo_id} {self.saldo} {self.turma_id}")

    def to_dict(self):
        user_dict = super().to_dict()
        user_dict.update({
            "grupo_id": self.grupo_id,
            "saldo": self.saldo,
            "turma_id": self.turma_id
        })
        return user_dict

    def to_dict_without_senha(self):
        user_dict = super().to_dict_without_senha()
        user_dict.update({
            "grupo_id": self.grupo_id,
            "saldo": self.saldo,
            "turma_id": self.turma_id
        })
        return user_dict
