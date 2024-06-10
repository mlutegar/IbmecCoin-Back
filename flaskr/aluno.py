from flask import Blueprint, request, jsonify
from flaskr.dao.aluno_dao import AlunoDAO
from flaskr.dao.grupo_dao import GrupoDAO
from flaskr.dao.transacao_dao import TransacaoDAO
from flaskr.dao.turma_dao import TurmaDAO
from flaskr.entities.aluno import Aluno

bp = Blueprint('aluno', __name__, url_prefix='/aluno')


@bp.route('/informacao', methods=['POST'])
def aluno():
    """
    Função que exibe as informações de um aluno.
    curl -X POST http://localhost:5000/aluno/informacao -H "Content-Type: application/json" -d "{\"matricula\": \"202208385192\"}"
    """
    data = request.json
    matricula = data.get('matricula')

    aluno_obj = AlunoDAO().get_aluno(matricula)
    turmas = TurmaDAO().get_all_turmas_by_id_aluno(matricula)
    grupos = GrupoDAO().get_all_grupos_by_matricula_aluno(matricula)

    if aluno_obj and turmas:
        return jsonify({
            'aluno': aluno_obj.__dict__(),
            'turmas': [turma.__dict__() for turma in turmas],
            'grupos': [grupo.__dict__() for grupo in grupos]
        }), 200

    return jsonify({'message': 'Aluno nao encontrado'}), 400


@bp.route('/alunos', methods=['GET'])
def alunos():
    """
    Função que exibe as informações de todos os alunos.
    curl -X GET http://localhost:5000/aluno/alunos
    """
    alunos_list = AlunoDAO().get_all_alunos()
    return jsonify({'alunos': [aluno.__dict__() for aluno in alunos_list]}), 200


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

    if not aluno_obj:
        return jsonify({'message': 'Aluno nao encontrado'}), 400

    transacoes_com_nomes = []
    for trans in transacoes_list:
        emissor = AlunoDAO().get_aluno(trans.emissor_id)
        receptor = AlunoDAO().get_aluno(trans.receptor_id)
        transacao_dict = trans.__dict__()
        transacao_dict['emissor_nome'] = emissor.nome if emissor else 'Desconhecido'
        transacao_dict['receptor_nome'] = receptor.nome if receptor else 'Loja'
        transacoes_com_nomes.append(transacao_dict)

    return jsonify({
        'aluno': aluno_obj.__dict__(),
        'transacoes': transacoes_com_nomes
    }), 200
