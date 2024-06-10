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
    curl -X POST http://localhost:5000/professor/informacao -H "Content-Type: application/json" -d "{\"matricula\": \"15912411702\"}"
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
    curl -X POST http://localhost:5000/professor/beneficiar -H "Content-Type: application/json" -d "{\"usuario\": \"202208385192\", \"quantidade\": \"10\"}"
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

    if alunoDao.update_aumentar_saldo(aluno.matricula, int(quantidade)):
        return jsonify({'message': 'Aluno beneficiado com sucesso', 'aluno': aluno.__dict__()}), 200

    return jsonify({'message': 'Erro ao beneficiar aluno'}), 400


@bp.route('/transacoes', methods=['GET'])
def transacoes():
    """
    Função que retorna todas as transações dos alunos.
    curl -X GET http://localhost:5000/professor/transacoes
    """
    transacao = TransacaoDAO()
    aluno = AlunoDAO()
    transacoes = transacao.get_all_transacoes()

    if not transacoes:
        return jsonify({'message': 'Nenhuma transacao encontrada'}), 400

    transacoes_com_nomes = []
    for trans in transacoes:
        emissor = aluno.get_aluno(trans.emissor_id)
        receptor = aluno.get_aluno(trans.receptor_id)
        transacao_dict = trans.__dict__()
        transacao_dict['emissor_nome'] = emissor.nome if emissor else 'Desconhecido'
        transacao_dict['receptor_nome'] = receptor.nome if receptor else 'Loja'
        transacoes_com_nomes.append(transacao_dict)

    return jsonify({'transacoes': transacoes_com_nomes}), 200

