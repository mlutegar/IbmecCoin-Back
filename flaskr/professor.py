from flask import Blueprint, request, jsonify
from flaskr.dao.aluno_dao import AlunoDAO
from flaskr.dao.professor_dao import ProfessorDAO
from flaskr.dao.transacao_dao import TransacaoDAO
from flaskr.dao.turma_dao import TurmaDAO

bp = Blueprint('professor', __name__, url_prefix='/professor')


@bp.route('/informacao', methods=['POST'])
def informacao():
    """
    Função que exibe as informações de um professor e suas turmas.
    curl -X POST http://localhost:5000/professor/informacao -H "Content-Type: application/json" -d "{\"matricula\": \"1\"}"
    """
    data = request.json
    matricula = data['matricula']

    professor_obj = ProfessorDAO().get_professor(matricula)

    if professor_obj is None:
        return jsonify({'message': 'Professor nao encontrado'}), 400

    turmas = TurmaDAO().get_all_turmas_by_professor_matricula(professor_obj.matricula)

    if professor_obj and turmas:
        return jsonify({
            'professor': professor_obj.__dict__(),
            'turmas': [turma.__dict__() for turma in turmas]
        }), 200

    return jsonify({'message': 'Erro na requisicao'}), 401


@bp.route('/beneficiar', methods=['POST'])
def beneficiar():
    """
    Função que beneficia um aluno com uma quantia.
    curl -X POST http://localhost:5000/professor/beneficiar -H "Content-Type: application/json" -d "{\"matricula\": \"1\", \"usuario\": \"2\", \"quantidade\": \"10\"}"
    """
    data = request.json
    quantidade = data['quantidade']
    matricula = data['usuario']

    alunoDao = AlunoDAO()
    aluno = alunoDao.get_aluno(matricula)

    if not quantidade or not matricula:
        return jsonify({'message': 'Preencha todos os campos'}), 400

    if not quantidade.isnumeric():
        return jsonify({'message': 'Quantidade invalida'}), 400

    if aluno is None:
        return jsonify({'message': 'Usuario nao encontrado'}), 400

    aluno.saldo += int(quantidade)

    if alunoDao.update_aluno(aluno):
        return jsonify({'message': 'Aluno beneficiado com sucesso', 'aluno': aluno.__dict__()}), 200

    return jsonify({'message': 'Erro ao beneficiar aluno'}), 400


@bp.route('/transacoes', methods=['POST'])
def transacoes():
    """
    Função que retorna todas as transações dos alunos.
    curl -X POST http://localhost:5000/professor/transacoes -H "Content-Type: application/json"
    """
    transacao = TransacaoDAO()
    transacoes = transacao.get_all_transacoes()

    if not transacoes:
        return jsonify({'message': 'Nenhuma transacao encontrada'}), 400

    return jsonify({'transacoes': [trans.__dict__() for trans in transacoes]}), 200
