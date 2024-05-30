from flask import Blueprint, render_template, request, g, flash
from flaskr.dao.aluno_dao import AlunoDao
from flaskr.dao.transferencia_dao import TransferenciaDao
from flaskr.dao.user_dao import UserDao
from flaskr.utils.transfer import processar_transferencia, processar_grupo

bp = Blueprint('transfer', __name__, url_prefix='/transfer')

@bp.route('/transferir', methods=('GET', 'POST'))
def transferir():
    """
    Função que exibe a página de transferência de IbmecCoins.
    Essa função também é responsável por processar o post do formulário de transferência de IbmecCoins.
    """
    transfer = TransferenciaDao()
    alunoDao = AlunoDao()

    if request.method == 'POST':
        situacao, mensagem = processar_transferencia(request, alunoDao, transfer)
        flash(mensagem)
        if not situacao:
            return render_template('transfer/transferir.html')

    return render_template('transfer/transferir.html')

@bp.route('/grupo', methods=('GET', 'POST'))
def grupo():
    """
    Função que exibe a página de transferência de IbmecCoins para um grupo.
    Essa função é responsável por mostrar o nome do grupo, o número de integrantes e quais são os integrantes do grupo.
    """
    transfer = TransferenciaDao()
    alunoDao = AlunoDao()
    userDao = UserDao()

    if request.method == 'POST':
        situacao, mensagem = processar_grupo(request, alunoDao, transfer)
        flash(mensagem)
        if not situacao:
            return render_template('transfer/grupo.html')

    # Obtém o grupo e seus membros para exibição na página
    grupo_info = alunoDao.get_group_info(g.user['matricula'])
    membros = alunoDao.get_group_members(grupo_info['id']) if grupo_info else []

    return render_template('transfer/grupo.html', grupo=grupo_info, membros=membros)
