from flaskr.entities.user import User


class Professor(User):
    def __init__(self, matricula: int, senha: str, nome: str, email: str):
        super().__init__(matricula, senha, "professor", nome, email)

    def __dict__(self):
        user_dict = super().__dict__()
        return user_dict
