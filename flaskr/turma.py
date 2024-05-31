from flask import Blueprint, render_template
from flaskr.auth import login_required

bp = Blueprint('turma', __name__, url_prefix='/turma')


@login_required
@bp.route('/informacao/<turma_id>', methods=('GET', 'POST'))
def informacao(turma_id):
    """
    Exibe informações da turma
    :param turma_id: id da turma
    :return: informações da turma
    """

    turma_id = int(turma_id)
    return render_template('turma/informacao.html', turma_id=turma_id)
