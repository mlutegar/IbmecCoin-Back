# utils.py
from flask import g

from flaskr.dao.transacao_dao import TransacaoDAO


def validar_campos_transferencia(quantidade, destinatario):
    """
    Valida os campos do formulário de transferência.
    :param quantidade: Quantidade de IbmecCoins a ser transferida.
    :param destinatario: Matrícula do destinatário.
    """
    if quantidade == "" or destinatario == "":
        return False
    elif not quantidade.isnumeric():
        return False
    return True


def processar_transferencia(remetente, destinatario, quantidade):
    """
    Processa a transferência de IbmecCoins.
    """
    if validar_campos_transferencia(destinatario, quantidade):
        return False
    transacao = TransacaoDAO()
    return transacao.insert_transacao(quantidade, remetente, destinatario)
