class User:
    def __init__(self, matricula: int, senha: str, tipo: str, nome: str, email: str):
        self.matricula = matricula
        self.senha = senha
        self.tipo = tipo
        self.nome = nome
        self.email = email

    def __dict__(self):
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
