# transferencia_dao.py
"""
Módulo responsável por realizar a transferência de saldo entre contas.
"""
from flaskr.dao.aluno_dao import AlunoDao
from flaskr.dao.user_dao import UserDao
from flaskr.db import get_db


class TransferenciaDao:
    def transferir(self, quantidade, remetente, destinatario):
        """
        Função que transfere saldo de uma conta para outra.

        :param quantidade: Quantidade de saldo a ser transferida
        :param remetente: Dicionário representando o usuário remetente
        :param destinatario: Dicionário representando o usuário destinatário
        :return: Tupla (bool, str) indicando sucesso/falha e mensagem correspondente
        """

        # Validações iniciais para garantir dados válidos
        try:
            if not remetente or not destinatario:
                raise ValueError("Remetente e destinatário devem ser especificados.")
            if remetente == destinatario:
                raise ValueError("Remetente e destinatário não podem ser a mesma pessoa.")
            if quantidade <= 0:
                raise ValueError("A quantidade deve ser maior que zero.")

            saldo_remetente = int(remetente['saldo'])
            if saldo_remetente < quantidade:
                raise ValueError("Saldo insuficiente para realizar a transferência.")

        except ValueError as ve:
            return False, f"Erro ao realizar transferência: {ve}"

        try:
            # Simulação de lógica de banco de dados para transferência
            self._registrar_transferencia(quantidade, remetente, destinatario)
            return True, f"Transferência de {quantidade} realizada com sucesso de {remetente['nome']} para {destinatario['nome']}."
        except Exception as e:
            return False, f"Erro ao realizar transferência: {str(e)}"

    def _registrar_transferencia(self, quantidade, remetente, destinatario):
        """
        Função interna para registrar a transferência no sistema de log ou banco de dados.
        :param quantidade: Quantidade de saldo a ser transferida
        :param remetente: Dicionário representando o usuário remetente
        :param destinatario: Dicionário representando o usuário destinatário
        :return: (bool, str) Status da operação e mensagem de resultado
        """
        # Supondo que 'debitar' e 'creditar' são métodos que retornam bool indicando sucesso
        if not self.debitar(quantidade, remetente):
            return False, f"Falha ao debitar {quantidade} do {remetente['nome']}."
        if not self.creditar(quantidade, destinatario):
            return False, f"Falha ao creditar {quantidade} para {destinatario['nome']}."

        try:
            db = get_db()
            with db:
                db.execute(
                    "INSERT INTO transacao (emissor_id, receptor_id, valor) VALUES (?, ?, ?)",
                    (remetente['matricula'], destinatario['matricula'], quantidade)
                )

            db.commit()

            return True, f"Transferência de {quantidade} de {remetente['id_user']} para {destinatario['id_user']} registrada com sucesso."
        except Exception as e:
            return False, f"Erro ao registrar transferência no banco de dados: {str(e)}"

    def creditar(self, quantidade, usuario):
        """
        Função que credita saldo em uma conta.

        :param quantidade: quantidade de saldo a ser creditada
        :param usuario: usuário para quem será creditada a quantidade de saldo
        :return: bool: True se a operação foi bem-sucedida, False caso contrário
        """
        if quantidade <= 0:
            print("Quantidade para crédito deve ser maior que zero.")
            return False

        try:
            matricula = usuario['matricula']
            alunoDao = AlunoDao()
            return alunoDao.creditar_saldo(matricula, quantidade)
        except Exception as e:
            print(f"Erro ao creditar saldo: {e}")
            return False

    def debitar(self, quantidade, usuario):
        """
        Função que debita saldo de uma conta.

        :param quantidade: quantidade de saldo a ser debitada
        :param usuario: usuário para quem será debitada a quantidade de saldo
        :return: bool: True se a operação foi bem-sucedida, False caso contrário
        """
        if quantidade <= 0:
            print("Quantidade para débito deve ser maior que zero.")
            return False

        try:
            matricula = usuario['matricula']
            alunoDao = AlunoDao()
            return alunoDao.debitar_saldo(matricula, quantidade)
        except Exception as e:
            print(f"Erro ao debitar saldo: {e}")
            return False

    def get_all_transacoes(self):
        """
        Função que retorna todas as transações registradas no sistema.
        :return: lista de dicionários representando as transações
        """
        try:
            db = get_db()
            transacoes = db.execute(
                "SELECT * FROM transacao"
            ).fetchall()

            return transacoes, "Transações obtidas com sucesso."
        except Exception as e:
            return [], f"Erro ao obter transações: {str(e)}"

    def criar_grupo(self, nome_grupo, remetente, quantidade):
        """
        Função que cria um grupo de transferência de saldo. O grupo pode ser composto por até 10 pessoas. O remetente é o criador do grupo.
        :param nome_grupo: o nome do grupo
        :param remetente: o usuário que está criando o grupo
        :param quantidade: o número de integrantes que o grupo terá
        :return: Tupla (bool, str) indicando sucesso/falha e mensagem correspondente
        """
        try:
            if not remetente:
                raise ValueError("Remetente deve ser especificado.")
            if quantidade <= 0 or quantidade > 10:
                raise ValueError("O número de integrantes deve ser entre 1 e 10.")

            db = get_db()
            with db:
                db.execute(
                    "INSERT INTO grupo_transferencia (nome, valor_max, crador_id) VALUES (?, ?, ?)",
                    (nome_grupo, quantidade, remetente['id_user'])
                )

            db.commit()

            return True, f"Grupo {nome_grupo} criado com sucesso por {remetente['nome']}."
        except Exception as e:
            return False, f"Erro ao criar grupo: {str(e)}"
