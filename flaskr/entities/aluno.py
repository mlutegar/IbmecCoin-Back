from flaskr.entities.user import User


class Aluno(User):
    def __init__(self, matricula, senha, nome, email, saldo):
        super().__init__(matricula, senha, "aluno", nome, email)
        self.saldo = saldo

    def __dict__(self):
        user_dict = super().__dict__()
        user_dict.update({
            "saldo": self.saldo
        })
        return user_dict

    def to_dict_without_senha(self):
        user_dict = super().to_dict_without_senha()
        user_dict.update({
            "saldo": self.saldo
        })
        return user_dict
