from flask import render_template, Blueprint

from flaskr.dao.entities.aluno_dao import AlunoDao

bp = Blueprint('debugger', __name__, url_prefix='/debugger')

@bp.route('/debugger', methods=('GET', 'POST'))
def debugger():
    aluno_dao = AlunoDao()

    alunos = aluno_dao.select_all()
    return render_template('/debugger.html', alunos=alunos)