from flask import Blueprint, render_template, flash, request, session, jsonify

from flaskr.auth import login_required
from flaskr.dao.aluno_dao import AlunoDAO
from flaskr.dao.professor_dao import ProfessorDAO
from flaskr.dao.transacao_dao import TransacaoDAO
from flaskr.dao.turma_dao import TurmaDAO

bp = Blueprint('professor', __name__, url_prefix='/professor')


@login_required
@bp.route('/informacao', methods=['POST'])
def informacao():
    """
    Função que exibe a página de um aluno.
    :return: Renderiza a página de beneficiar um aluno
    """
    data = request.json
    matricula = data['matricula']

    professor_obj = ProfessorDAO().get_professor(matricula)
    turmas = TurmaDAO().get_all_turmas_by_professor_matricula(professor_obj.matricula)

    if professor_obj and turmas:
        return jsonify({
            'professor': professor_obj.__dict__(),
            'turmas': [turma.__dict__() for turma in turmas]
        }), 200

    return jsonify({'message': 'Erro na requisição'}), 401


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
            return render_template('professor/beneficiar.html', alunos=alunos)

        if not quantidade.isnumeric():
            flash("Quantidade inválida")
            return render_template('professor/beneficiar.html', alunos=alunos)

        if aluno is None:
            flash("Usuário não encontrado")
            return render_template('professor/beneficiar.html', alunos=alunos)

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
