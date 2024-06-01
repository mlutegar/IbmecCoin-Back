class User:
    def __init__(self, matricula: int, senha: str, tipo: str, nome: str, email: str):
        self.matricula = matricula
        self.senha = senha
        self.tipo = tipo
        self.nome = nome
        self.email = email

    def __str__(self):
        return f"User {self.matricula} {self.nome} {self.email} {self.senha} {self.tipo}"

    def __repr__(self):
        return f"User {self.matricula} {self.nome} {self.email} {self.senha} {self.tipo}"

    def to_dict(self):
        return {
            "matricula": self.matricula,
            "senha": self.senha,
            "tipo": self.tipo,
            "nome": self.nome,
            "email": self.email
        }

    def to_dict_without_senha(self):
        return {
            "matricula": self.matricula,
            "tipo": self.tipo,
            "nome": self.nome,
            "email": self.email
        }

    def update_senha(self, senha):
        self.senha = senha
        return self
