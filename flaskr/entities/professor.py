from flaskr.entities.user import User


class Professor(User):
    def __init__(self, matricula: int, senha: str, nome: str, email: str):
        super().__init__(matricula, senha, "professor", nome, email)
