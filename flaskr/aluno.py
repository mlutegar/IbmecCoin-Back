from flask import Blueprint, request, jsonify
from flaskr.dao.aluno_dao import AlunoDAO
from flaskr.dao.transacao_dao import TransacaoDAO

bp = Blueprint('aluno', __name__, url_prefix='/aluno')

@bp.route('/aluno', methods=['POST'])
def aluno():
    """
    Função que exibe as informações de um aluno.
    curl -X POST http://localhost:5000/aluno/aluno -H "Content-Type: application/json" -d "{\"matricula\": \"1\"}"
    """
    data = request.json
    matricula = data.get('matricula')

    aluno_obj = AlunoDAO().get_aluno(matricula)
    if aluno_obj is None:
        return jsonify({'message': 'Aluno nao encontrado'}), 400

    return jsonify({'aluno': aluno_obj.__dict__()}), 200

@bp.route('/historico', methods=['POST'])
def historico():
    """
    Função que exibe o histórico de transações de um aluno.
    curl -X POST http://localhost:5000/aluno/historico -H "Content-Type: application/json" -d "{\"matricula\": \"1\"}"
    """
    data = request.json
    matricula = data.get('matricula')

    try:
        aluno_obj = AlunoDAO().get_aluno(matricula)
        transacoes_list = TransacaoDAO().get_transacoes_aluno(matricula)
    except Exception as e:
        return jsonify({'message': 'Erro ao buscar historico de transacoes: ' + str(e)}), 400

    return jsonify({'aluno': aluno_obj.__dict__(), 'transacoes': [trans.__dict__() for trans in transacoes_list]}), 200
