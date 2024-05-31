from flask import Blueprint, render_template, flash, request, g, session

from flaskr.auth import login_required
from flaskr.dao.aluno_dao import AlunoDAO
from flaskr.dao.transacao_dao import TransacaoDAO

bp = Blueprint('aluno', __name__, url_prefix='/aluno')


@login_required
@bp.route('/aluno', methods=('GET', 'POST'))
def aluno():
    """
    Função que exibe a página de um aluno.
    :return: Renderiza a página de beneficiar um aluno
    """
    matricula = session['matricula']
    if matricula is None:
        flash("Usuário não encontrado")
        return render_template('/')

    alunoDao = AlunoDAO()
    aluno_obj = alunoDao.get_aluno(matricula)

    return render_template('aluno.html', aluno=aluno_obj)


@login_required
@bp.route('/historico', methods=('GET', 'POST'))
def historico():
    """
    Função que exibe o histórico de transações de um aluno.
    :return: Renderiza a página de histórico de transações de um aluno
    """
    try:
        matricula = session['matricula']
        aluno_obj = AlunoDAO().get_aluno(matricula)
        transacoes_list = TransacaoDAO().get_transacoes_aluno(matricula)
    except Exception as e:
        flash("Erro ao buscar histórico de transações: " + str(e))
        return render_template('/')

    return render_template('aluno/historico.html', aluno=aluno_obj, transacoes=transacoes_list)
