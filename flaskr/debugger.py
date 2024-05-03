from flask import render_template, Blueprint

from flaskr.auth import bp
from flaskr.dao.aluno_dao import AlunoDao

bp = Blueprint('debugger', __name__, url_prefix='/debugger')

@bp.route('/debugger', methods=('GET', 'POST'))
def debugger():
    aluno_dao = AlunoDao()
    aluno1 = aluno_dao.select(123456)
    alunos = aluno_dao.select_all()
    return render_template('/debugger.html', alunos=alunos, aluno1=aluno1)