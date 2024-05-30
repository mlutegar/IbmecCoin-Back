class User:
    def __init__(self, id_user, matricula, nome, email, senha, tipo):
        self.id_user = id_user
        self.matricula = matricula
        self.nome = nome
        self.email = email
        self.senha = senha
        self.tipo = tipo

    def __str__(self):
        return f"User {self.id_user} {self.matricula} {self.nome} {self.email} {self.senha} {self.tipo}"

    def __repr__(self):
        return f"User {self.id_user} {self.matricula} {self.nome} {self.email} {self.senha} {self.tipo}"

    def to_dict(self):
        return {
            "id_user": self.id_user,
            "matricula": self.matricula,
            "nome": self.nome,
            "email": self.email,
            "senha": self.senha,
            "tipo": self.tipo
        }

    def to_dict_without_senha(self):
        return {
            "id_user": self.id_user,
            "matricula": self.matricula,
            "nome": self.nome,
            "email": self.email,
            "tipo": self.tipo
        }
