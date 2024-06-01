from flask import Blueprint, render_template, flash, request, session

from flaskr.auth import login_required
from flaskr.dao.aluno_dao import AlunoDAO
from flaskr.dao.professor_dao import ProfessorDAO
from flaskr.dao.transacao_dao import TransacaoDAO
from flaskr.dao.turma_dao import TurmaDAO

bp = Blueprint('professor', __name__, url_prefix='/professor')


@login_required
@bp.route('/professor', methods=('GET', 'POST'))
def professor():
    """
    Função que exibe a página de um aluno.
    :return: Renderiza a página de beneficiar um aluno
    """
    if 'matricula' not in session:
        flash("Usuário não encontrado")
        return render_template('/')

    professor_obj = ProfessorDAO().get_professor(session['matricula'])

    matricula = session['matricula']
    if matricula is None:
        flash("Usuário não encontrado")
        return render_template('/')

    turmas = TurmaDAO().get_all_turmas_by_professor_matricula(professor_obj.matricula)

    return render_template('professor.html', professor=professor_obj, turmas=turmas)


@bp.route('/beneficiar', methods=('GET', 'POST'))
def beneficiar():
    """
    Função que exibe a página de beneficiar um aluno.
    :return: Renderiza a página de beneficiar um aluno
    """
    alunoDao = AlunoDAO()
    alunos = alunoDao.get_all_alunos()

    if request.method == 'POST':
        quantidade = request.form['quantidade']
        matricula = request.form['usuario']
        aluno = alunoDao.get_aluno(matricula)

        if quantidade == "" or matricula == "":
            flash("Preencha todos os campos")
            return render_template('professor/beneficiar.html',  alunos=alunos)

        if not quantidade.isnumeric():
            flash("Quantidade inválida")
            return render_template('professor/beneficiar.html',  alunos=alunos)

        if aluno is None:
            flash("Usuário não encontrado")
            return render_template('professor/beneficiar.html',  alunos=alunos)

        aluno.saldo += int(quantidade)

        if alunoDao.update_aluno(aluno):
            alunos = alunoDao.get_all_alunos()
            flash("Aluno beneficiado com sucesso")
            return render_template('professor/beneficiar.html', alunos=alunos)

    return render_template('professor/beneficiar.html', alunos=alunos)


@bp.route('/transacoes', methods=('GET', 'POST'))
def transacoes():
    """
    Função que exibe a página de transferências de todas as transferências dos alunos.
    :return: Renderiza a página de transferências de todas as transferências dos alunos
    """
    transacao = TransacaoDAO()
    transacoes = transacao.get_all_transacoes()

    if not transacoes:
        flash("Nenhuma transação encontrada")
        return render_template('professor/transacoes.html')

    return render_template('professor/transacoes.html', transacoes=transacoes)
