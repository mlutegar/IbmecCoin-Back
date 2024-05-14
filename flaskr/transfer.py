"""
Módulo que contém as funções relacionadas ao transferência de IbmecCoins.
- A rota /transferir: exibe a página de transferência de IbmecCoins.
- A rota /transferir/<id>: transfere IbmecCoins para outro usuário.
- A rota /transferir/<id>/confirmar: confirma a transferência de IbmecCoins para outro usuário.
"""
from flask import Blueprint, render_template, flash, request, g

from flaskr.dao.aluno_dao import AlunoDao
from flaskr.dao.transferencia_dao import TransferenciaDao
from flaskr.dao.user_dao import UserDao

bp = Blueprint('transfer', __name__, url_prefix='/transfer')

@bp.route('/transferir', methods=('GET', 'POST'))
def transferir():
    """
    Função que exibe a página de transferência de IbmecCoins.
    Essa função também é responsável por processar o post do formulário de transferência de IbmecCoins.
    Ele pega o valor "quantidade" e o valor "usuario" do formulario, verifica se eles estão vazios ou não e se
    a quantidade é um número válido. Se tudo estiver correto, ele chama a função transferir de IbmecCoinsDao e passa os
    valores como parâmetros.
    :return: renderiza a página de transferência de IbmecCoins
    """
    transfer = TransferenciaDao()
    alunoDao = AlunoDao()

    if request.method == 'POST':
        quantidade = request.form['quantidade']
        remetente = g.user['matricula']
        destinatario = request.form['usuario']

        if quantidade == "" or destinatario == "" or remetente == "":
            flash("Preencha todos os campos")
            return render_template('transfer/transferir.html')
        elif not quantidade.isnumeric():
            flash("Quantidade inválida")
            return render_template('transfer/transferir.html')

        remetente = alunoDao.select_user_by_matricula(destinatario)
        destinatario = alunoDao.select_user_by_matricula(destinatario)

        if remetente == -1 or destinatario == -1:
            flash("Usuário não encontrado")
            return render_template('transfer/transferir.html')

        situacao, mensagem = transfer.transferir(int(quantidade), g.user, destinatario)

        flash(mensagem)
    return render_template('transfer/transferir.html')
