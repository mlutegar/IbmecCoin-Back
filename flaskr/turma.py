from flask import Blueprint, render_template, session, request, flash
from flaskr.auth import login_required
from flaskr.dao.aluno_dao import AlunoDAO
from flaskr.dao.convite_dao import ConviteDAO
from flaskr.dao.turma_dao import TurmaDAO
from flaskr.dao.user_dao import UserDAO

bp = Blueprint('turma', __name__, url_prefix='/turma')


@login_required
@bp.route('/informacao/<int:id_turma>', methods=('GET', 'POST'))
def informacao(id_turma):
    """
    Exibe informações da turma
    :param id_turma: id da turma
    :return: informações da turma
    """
    matricula = session['matricula']
    if matricula is None:
        flash("Usuário não encontrado")
        return render_template('/')

    user = UserDAO().get_user(matricula)
    turma = TurmaDAO().get_turma_by_id(id_turma)

    if turma is None or user is None:
        flash("Turma não encontrada")
        return render_template('/')

    if request.method == 'POST':
        matricula = request.form['matricula']
        if AlunoDAO().update_aluno_turma(matricula, turma.id_turma):
            flash('Convite enviado com sucesso')
        else:
            flash('Usuário não encontrado')

    return render_template('turma/informacao.html', turma=turma, user=user)

@bp.route('/criar', methods=('GET', 'POST'))
def criar():
    """
    Cria uma nova turma
    :return: página de criação de turma
    """
    user = UserDAO().get_user(session['matricula'])

    if request.method == 'POST':
        nome = request.form['nome']
        turma = TurmaDAO().insert_turma(nome, user.id_usuario)
        if turma:
            return render_template('turma/informacao.html', id_turma=turma)
        else:
            flash('Erro ao criar turma')

@bp.route('/entrar', methods=('GET', 'POST'))
def entrar():
    """
    Entra em uma turma
    :return: página de entrada em turma
    """
    user = UserDAO().get_user(session['matricula'])

    if request.method == 'POST':
        nome_turma = request.form['nome']
        if AlunoDAO().update_aluno_turma(user.matricula, nome_turma):
            id_turma = TurmaDAO().get_turma_by_nome(nome_turma).id_turma
            return render_template('turma/informacao.html', id_turma=id_turma)
        else:
            flash('Erro ao entrar na turma')

    return render_template('turma/entrar.html')
