from flask import Blueprint, render_template, flash, request, session

from flaskr.auth import login_required
from flaskr.dao.aluno_dao import AlunoDAO
from flaskr.dao.professor_dao import ProfessorDAO
from flaskr.dao.transacao_dao import TransacaoDAO

bp = Blueprint('professor', __name__, url_prefix='/professor')


@login_required
@bp.route('/professor', methods=('GET', 'POST'))
def professor():
    """
    Função que exibe a página de um aluno.
    :return: Renderiza a página de beneficiar um aluno
    """
    matricula = session['matricula']
    if matricula is None:
        flash("Usuário não encontrado")
        return render_template('/')

    professorDao = ProfessorDAO()
    professor_obj = professorDao.get_professor(matricula)

    return render_template('professor.html', professor=professor_obj)


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
            return render_template('professor/beneficiar.html')

        if not quantidade.isnumeric():
            flash("Quantidade inválida")
            return render_template('professor/beneficiar.html')

        if aluno is None:
            flash("Usuário não encontrado")
            return render_template('professor/beneficiar.html')

        aluno.saldo += int(quantidade)

        alunoDao.update_aluno(aluno)
        flash("Aluno beneficiado com sucesso")

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
