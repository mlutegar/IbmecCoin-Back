from flask import Blueprint, render_template, session, request, flash, redirect, url_for
from flaskr.auth import login_required
from flaskr.dao.aluno_dao import AlunoDAO
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
        aluno = AlunoDAO().get_aluno(matricula)

        if aluno is None:
            flash('Usuário não encontrado')
            return render_template('turma/informacao.html', turma=turma, user=user)

        aluno.id_turma = turma.id_turma

        if AlunoDAO().update_aluno(aluno):
            flash('Aluno adicionado com sucesso')
            turma = TurmaDAO().get_turma_by_id(id_turma)
            return render_template('turma/informacao.html', turma=turma, user=user)
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

        if nome is None:
            flash('Nome da turma não pode ser vazio')
            return render_template('turma/criar.html')

        turma = TurmaDAO().insert_turma(nome, user.matricula)
        if turma:
            return redirect(url_for('index'))
        else:
            flash('Erro ao criar turma')

    return render_template('turma/criar.html')


@bp.route('/entrar', methods=('GET', 'POST'))
def entrar():
    """
    Entra em uma turma
    :return: página de entrada em turma
    """
    user = UserDAO().get_user(session['matricula'])

    if request.method == 'POST':
        nome_turma = request.form['nome']
        turma = TurmaDAO().get_turma_by_nome(nome_turma)

        if turma is None:
            flash('Turma não encontrada')
            return render_template('turma/entrar.html')

        if AlunoDAO().update_aluno_turma(user.matricula, turma.id_turma):
            turma_atualizada = TurmaDAO().get_turma_by_nome(nome_turma)
            user_atualizado = UserDAO().get_user(session['matricula'])
            return render_template('turma/informacao.html', turma=turma_atualizada, user=user_atualizado)
        else:
            flash('Erro ao entrar na turma')

    return render_template('turma/entrar.html')
