from flask import Blueprint, render_template, session, request, flash
from flaskr.auth import login_required
from flaskr.dao.aluno_dao import AlunoDAO
from flaskr.dao.convite_dao import ConviteDAO
from flaskr.dao.turma_dao import TurmaDAO
from flaskr.dao.user_dao import UserDAO

bp = Blueprint('turma', __name__, url_prefix='/turma')


@login_required
@bp.route('/informacao/<turma_id>', methods=('GET', 'POST'))
def informacao(turma_id):
    """
    Exibe informações da turma
    :param turma_id: id da turma
    :return: informações da turma
    """
    user = UserDAO().get_user(session['id'])
    turma = TurmaDAO().get_turma_by_id(turma_id)

    if request.method == 'POST':
        matricula = request.form['matricula']
        if AlunoDAO().update_aluno_turma(matricula, turma.id_turma):
            flash('Convite enviado com sucesso')
        else:
            flash('Usuário não encontrado')

    return render_template('turma/informacao.html', turma_id=turma, user=user)
