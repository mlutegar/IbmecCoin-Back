from flaskr.entities.user import User


class Aluno(User):
    def __init__(self, id_user, matricula, nome, email, senha, tipo, id_aluno, grupo_id, saldo, turma_id):
        super().__init__(id_user, matricula, nome, email, senha, tipo)
        self.id_aluno = id_aluno
        self.grupo_id = grupo_id
        self.saldo = saldo
        self.turma_id = turma_id

    def __str__(self):
        return (f"Aluno {self.id_aluno} {self.id_user} {self.matricula} {self.nome} {self.email} "
                f"{self.senha} {self.tipo} {self.grupo_id} {self.saldo} {self.turma_id}")

    def __repr__(self):
        return (f"Aluno {self.id_aluno} {self.id_user} {self.matricula} {self.nome} {self.email} "
                f"{self.senha} {self.tipo} {self.grupo_id} {self.saldo} {self.turma_id}")

    def to_dict(self):
        user_dict = super().to_dict()
        user_dict.update({
            "id_aluno": self.id_aluno,
            "grupo_id": self.grupo_id,
            "saldo": self.saldo,
            "turma_id": self.turma_id
        })
        return user_dict

    def to_dict_without_senha(self):
        user_dict = super().to_dict_without_senha()
        user_dict.update({
            "id_aluno": self.id_aluno,
            "grupo_id": self.grupo_id,
            "saldo": self.saldo,
            "turma_id": self.turma_id
        })
        return user_dict
