from flask import Blueprint, request, jsonify
from flaskr.dao.aluno_dao import AlunoDAO
from flaskr.dao.convite_dao import ConviteDAO
from flaskr.dao.grupo_dao import GrupoDAO
from flaskr.dao.transacao_dao import TransacaoDAO

bp = Blueprint('grupo', __name__, url_prefix='/grupo')


@bp.route('/informacao', methods=['POST'])
def informacao():
    """
    Função que exibe as informações do grupo do aluno.
    curl -X POST http://localhost:5000/grupo/informacao -H "Content-Type: application/json" -d "{\"matricula\": \"1\"}"
    """
    data = request.json
    matricula = data['matricula']

    aluno = AlunoDAO().get_aluno(matricula)
    id_grupo = aluno.id_grupo
    grupo = GrupoDAO().get_grupo_by_id(id_grupo)

    if aluno is None or grupo is None:
        return jsonify({'message': 'Erro ao carregar informações do grupo'}), 400

    return jsonify({'grupo': grupo.__dict__(), 'aluno': aluno.__dict__()}), 200


@bp.route('/criar', methods=['POST'])
def criar():
    """
    Função que cria um grupo.
    curl -X POST http://localhost:5000/grupo/criar -H "Content-Type: application/json" -d "{\"matricula\": \"1\", \"nome\": \"Grupo 1\", \"descricao\": \"Descricao do grupo\"}"
    """
    data = request.json
    matricula = data['matricula']
    nome = data['nome']
    descricao = data['descricao']

    aluno = AlunoDAO().get_aluno(matricula)
    grupoDao = GrupoDAO()

    grupo = grupoDao.insert_grupo(nome, 5, descricao, aluno.matricula)
    if grupo is None:
        return jsonify({'message': 'Grupo ja existe'}), 400

    aluno.id_grupo = grupo.id_grupo

    if not AlunoDAO().update_aluno(aluno):
        return jsonify({'message': 'Erro ao atualizar aluno'}), 400

    return jsonify({
            'message': 'Grupo criado com sucesso',
            'grupo': grupo.__dict__(),
            'aluno': aluno.__dict__()
        }), 200

@bp.route('/sair', methods=['POST'])
def sair():
    """
    Função que remove o aluno do grupo.
    curl -X POST http://localhost:5000/grupo/sair -H "Content-Type: application/json" -d "{\"matricula\": \"1\"}"
    """
    data = request.json
    matricula = data['matricula']

    aluno = AlunoDAO().get_aluno(matricula)

    if aluno.id_grupo is None:
        return jsonify({'message': 'Aluno nao esta em nenhum grupo'}), 400

    grupo = GrupoDAO().get_grupo_by_id(aluno.id_grupo)

    if not AlunoDAO().update_sair_grupo(aluno.matricula):
        return jsonify({'message': 'Erro ao sair do grupo'}), 400

    return jsonify({'message': 'Aluno removido do grupo', 'grupo': grupo.__dict__(), 'aluno': aluno.__dict__()}), 200

@bp.route('/transferir', methods=['POST'])
def transferir():
    """
    Função que realiza a transferência de IbmecCoins.
    curl -X POST http://localhost:5000/grupo/transferir -H "Content-Type: application/json" -d "{\"matricula\": \"1\", \"usuario\": \"2\", \"quantidade\": \"10\"}"
    """
    data = request.json
    remetente_matricula = data['matricula']
    destinatario_matricula = data['usuario']
    quantidade = int(data['quantidade'])

    remetente = AlunoDAO().get_aluno(remetente_matricula)
    destinatario = AlunoDAO().get_aluno(destinatario_matricula)

    if destinatario is None or quantidade == "":
        return jsonify({'message': 'Usuario nao encontrado'}), 400

    if not TransacaoDAO().insert_transacao(remetente.matricula, destinatario.matricula, quantidade):
        return jsonify({'message': 'Nao foi possivel processar a transferencia'}), 400

    return jsonify({'message': 'Transferencia realizada com sucesso', 'aluno': remetente.__dict__(),
                    'grupo': GrupoDAO().get_grupo_by_id(remetente.get_id_grupo()).__dict__()}), 200


@bp.route('/convidar', methods=['POST'])
def convidar():
    """
    Função que convida um aluno para o grupo.
    curl -X POST http://localhost:5000/grupo/convidar -H "Content-Type: application/json" -d "{\"matricula\": \"1\", \"destinatario\": \"2\"}"
    """
    data = request.json
    remetente_matricula = data['matricula']
    destinatario_matricula = data['destinatario']

    alunoDao = AlunoDAO()
    grupoDao = GrupoDAO()
    conviteDao = ConviteDAO()
    remetente = alunoDao.get_aluno(remetente_matricula)
    grupo = grupoDao.get_grupo_by_id(remetente.get_id_grupo())
    destinatario = alunoDao.get_aluno(destinatario_matricula)

    if destinatario is None:
        return jsonify({'message': 'Usuario nao encontrado'}), 400

    if not conviteDao.insert_convite(grupo.id_grupo, destinatario.matricula):
        return jsonify({'message': 'Convite nao enviado'}), 400

    return jsonify(
        {'message': 'Convite enviado com sucesso', 'grupo': grupo.__dict__(), 'aluno': remetente.__dict__()}), 200


@bp.route('/convites', methods=['POST'])
def convites():
    """
    Função que exibe os convites recebidos.
    curl -X POST http://localhost:5000/grupo/convites -H "Content-Type: application/json" -d "{\"matricula\": \"1\"}"
    """
    data = request.json
    matricula = data['matricula']
    aluno = AlunoDAO().get_aluno(matricula)

    if aluno is None:
        return jsonify({'message': 'Aluno nao encontrado'}), 400

    convites_lista = ConviteDAO().get_all_convites_by_matricula(aluno.matricula)
    if convites_lista is None:
        return jsonify({
            'message': 'Nenhum convite encontrado',
            'convites': [],
            'aluno': aluno.__dict__()
                        }), 400

    return jsonify({'convites': [convite.__dict__() for convite in convites_lista], 'aluno': aluno.__dict__()}), 200


@bp.route('/aceitar', methods=['POST'])
def aceitar():
    """
    Função que aceita um convite de um grupo.
    curl -X POST http://localhost:5000/grupo/aceitar -H "Content-Type: application/json" -d "{\"matricula\": \"1\", \"id_convite\": \"123\"}"
    """
    data = request.json
    matricula = data['matricula']
    id_convite = data['id_convite']

    user = AlunoDAO().get_aluno(matricula)
    convite = ConviteDAO().get_convite(id_convite)

    if convite is None:
        return jsonify({'message': 'Convite nao encontrado'}), 400

    if AlunoDAO().update_entrar_grupo(convite.id_grupo, convite.convidado_matricula):
        grupo = GrupoDAO().get_grupo_by_id(convite.id_grupo)
        user.id_grupo = grupo.id_grupo
        AlunoDAO().update_aluno(user)
        ConviteDAO().delete_convite(convite.id_convite)

        return jsonify(
            {'message': 'Convite aceito com sucesso', 'grupo': grupo.__dict__(), 'aluno': user.__dict__()}), 200

    return jsonify({'message': 'Erro ao aceitar convite'}), 400

@bp.route('/recusar', methods=['POST'])
def recusar():
    """
    Função que recusa um convite de um grupo.
    curl -X POST http://localhost:5000/grupo/recusar -H "Content-Type: application/json" -d "{\"id_convite\": \"1\"}"
    """
    data = request.json
    id_convite = data['id_convite']

    convite = ConviteDAO().get_convite(id_convite)

    if convite is None:
        return jsonify({'message': 'Convite nao encontrado'}), 400

    ConviteDAO().delete_convite(convite.id_convite)

    return jsonify({'message': 'Convite recusado com sucesso'}), 200

