from flask import Blueprint, request, jsonify
from flaskr.dao.aluno_dao import AlunoDAO
from flaskr.dao.turma_dao import TurmaDAO
from flaskr.dao.user_dao import UserDAO

bp = Blueprint('turma', __name__, url_prefix='/turma')


@bp.route('/informacao', methods=['POST'])
def informacao():
    """
    Função que exibe as informações de uma turma.
    curl -X POST http://localhost:5000/turma/informacao -H "Content-Type: application/json" -d "{\"id_turma\": \"1\", \"matricula\": \"123\"}"
    """
    data = request.json
    id_turma = int(data['id_turma'])
    matricula = data['matricula']

    if matricula is None:
        return jsonify({'message': 'Usuario nao encontrado'}), 400

    user = UserDAO().get_user(matricula)
    turma = TurmaDAO().get_turma_by_id(id_turma)

    if turma is None or user is None:
        return jsonify({'message': 'Turma nao encontrada'}), 400

    return jsonify({'turma': turma.__dict__(), 'user': user.__dict__()}), 200


@bp.route('/adicionar_aluno', methods=['POST'])
def adicionar_aluno():
    """
    Função que adiciona um aluno a uma turma.
    curl -X POST http://localhost:5000/turma/adicionar_aluno -H "Content-Type: application/json" -d "{\"id_turma\": \"1\", \"matricula\": \"123\"}"
    """
    data = request.json
    id_turma = int(data['id_turma'])
    matricula_aluno_novo = data['matricula_aluno_novo']

    if matricula_aluno_novo is None:
        return jsonify({'message': 'Usuario nao encontrado'}), 400

    user = UserDAO().get_user(matricula_aluno_novo)
    turma = TurmaDAO().get_turma_by_id(id_turma)

    if turma is None or user is None:
        return jsonify({'message': 'Turma nao encontrada'}), 400

    aluno = AlunoDAO().get_aluno(matricula_aluno_novo)

    if aluno.id_turma == turma.id_turma:
        return jsonify({'message': 'Aluno ja esta na turma'}), 400

    if aluno is None:
        return jsonify({'message': 'Usuario nao encontrado'}), 400

    aluno.id_turma = turma.id_turma

    if AlunoDAO().update_aluno(aluno):
        return jsonify({'message': 'Aluno adicionado com sucesso', 'aluno': aluno.__dict__()}), 200
    else:
        return jsonify({'message': 'Erro ao atualizar turma'}), 400


@bp.route('/criar', methods=('GET', 'POST'))
def criar():
    """
    Cria uma nova turma
    :return: página de criação de turma
    """
    data = request.json
    matricula = data['matricula']
    nome = data['nome']

    user = UserDAO().get_user(matricula)

    if user.tipo != 'professor':
        return jsonify({'message': 'Usuario nao e professor'}), 400

    if nome is None:
        return jsonify({'message': 'Nome da turma não pode ser vazio'}), 401

    turma = TurmaDAO().insert_turma(nome, user.matricula)
    if turma:
        return jsonify({'turma': turma.__dict__()}), 200
    else:
        return jsonify({'message': 'Erro ao criar turma'}), 400


@bp.route('/entrar', methods=('GET', 'POST'))
def entrar():
    """
    Entra em uma turma
    :return: página de entrada em turma
    """
    data = request.json
    matricula = data['matricula']
    nome_turma = data['nome']

    user = UserDAO().get_user(matricula)
    turma = TurmaDAO().get_turma_by_nome(nome_turma)

    if turma is None:
        return jsonify({'message': 'Turma não encontrada'}), 400

    if AlunoDAO().update_entrar_turma(user.matricula, turma.id_turma):
        turma_atualizada = TurmaDAO().get_turma_by_nome(nome_turma)
        user_atualizado = UserDAO().get_user(matricula)
        return jsonify({'turma': turma_atualizada.__dict__(), 'user': user_atualizado.__dict__()}), 200
    else:
        return jsonify({'message': 'Erro ao entrar na turma'}), 400
