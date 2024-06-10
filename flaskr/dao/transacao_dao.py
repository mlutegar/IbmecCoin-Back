import datetime

from flaskr.dao.aluno_dao import AlunoDAO
from flaskr.dao.loja_dao import LojaDAO
from flaskr.entities.transacao import Transacao
from flaskr.utils.db import get_db


class TransacaoDAO:
    """
    Classe que representa um DAO (Data Access Object) para operações de transferência de saldo entre contas.

    Métodos:
        - insert_transacao(quantidade, remetente, destinatario):
        Função que registra a transação de uma conta para outra.
        - get_all_transacoes(): Função que retorna todas as transações registradas no sistema.
    """

    def __init__(self):
        pass

    @staticmethod
    def insert_transacao(emissor_id: int, receptor_id: int, valor: int):
        """
        Função que registra a transação de uma conta para outra.
        :param emissor_id: ID do aluno que está enviando o saldo.
        :param receptor_id: ID do aluno que está recebendo o saldo.
        :param valor: Valor da transação.
        :return: None
        """
        transacao = Transacao(emissor_id, receptor_id, valor, datetime.datetime.now())

        db = get_db()

        try:
            db.execute(
                "INSERT INTO transacao (emissor_id, receptor_id, valor, data) VALUES (?, ?, ?, ?)",
                (transacao.emissor_id, transacao.receptor_id, transacao.valor, transacao.data),
            )
            db.commit()
        except db.IntegrityError:
            return False
        return True

    @staticmethod
    def insert_transacao_loja(aluno_matricula, id_item):
        """
        Função que registra a transação de compra de um item na loja.
        :param aluno_matricula: Matrícula do aluno que comprou o item.
        :param id_item: ID do item comprado.
        :return: None
        """
        item = LojaDAO().get_item(id_item)
        aluno = AlunoDAO().get_aluno(aluno_matricula)
        transacao = Transacao(aluno_matricula, 'loja', item.valor, datetime.datetime.now())

        if item is None or aluno is None or aluno.saldo < item.valor:
            return False

        db = get_db()

        try:
            db.execute(
                "INSERT INTO transacao (emissor_id, receptor_id, valor, data) VALUES (?, ?, ?, ?)",
                (aluno.matricula, 'loja', transacao.valor, transacao.data),
            )
            db.commit()
        except db.IntegrityError:
            return False

        AlunoDAO().update_diminuir_saldo(aluno.matricula, item.valor)
        return True

    @staticmethod
    def get_all_transacoes():
        """
        Função que retorna todas as transações registradas no sistema.
        :return: Lista de transações.
        """
        transacoes = []
        db = get_db()

        resultado = db.execute(
            "SELECT * FROM transacao"
        ).fetchall()
        if not resultado:
            return None
        for row in resultado:
            transacoes.append(Transacao(row['emissor_id'], row['receptor_id'], row['valor'], row['data']))
        return transacoes

    @staticmethod
    def get_transacoes_aluno(matricula):
        """
        Função que retorna todas as transações de um aluno.
        :param matricula: Matrícula do aluno.
        :return: Lista de transações.
        """
        lista_transacoes = []

        db = get_db()

        resultado = db.execute(
            "SELECT * FROM transacao WHERE emissor_id = ? OR receptor_id = ?",
            (matricula, matricula)
        ).fetchall()

        if not resultado:
            return None

        for row in resultado:
            lista_transacoes.append(Transacao(row['emissor_id'], row['receptor_id'], row['valor'], row['data']))

        return lista_transacoes
