from flask import Blueprint, request, jsonify
from flaskr.dao.aluno_dao import AlunoDAO
from flaskr.dao.convite_dao import ConviteDAO
from flaskr.dao.grupo_dao import GrupoDAO
from flaskr.dao.transacao_dao import TransacaoDAO
from flaskr.entities.grupo import Grupo

bp = Blueprint('grupo', __name__, url_prefix='/grupo')


@bp.route('/informacao', methods=['POST'])
def informacao():
    """
    Função que exibe as informações do grupo do aluno.
    Curl -X POST http://localhost:5000/grupo/informacao -H "Content-Type: application/json" -d "{\"matricula\": \"202208385192\", \"id_turma\": \"1\"}"
    """
    data = request.json
    matricula = data['matricula']
    id_turma = data['id_turma']

    aluno = AlunoDAO().get_aluno(matricula)
    grupo = GrupoDAO().get_grupo_by_matricula_aluno(matricula, id_turma)

    if aluno is None or grupo is None:
        return jsonify({'message': 'Erro ao carregar informações do grupo'}), 400

    return jsonify({'grupo': grupo.__dict__(), 'aluno': aluno.__dict__()}), 200


@bp.route('/criar', methods=['POST'])
def criar():
    """
    Função que cria um grupo.
    curl -X POST http://localhost:5000/grupo/criar -H "Content-Type: application/json" -d "{\"matricula\": \"202208385192\", \"nome\": \"Grupo 1\", \"descricao\": \"Descricao do grupo\", \"id_turma\": \"1\"}"
    """
    # Pegar valores
    data = request.json
    matricula = data.get('matricula')
    nome = data.get('nome')
    descricao = data.get('descricao')
    id_turma = data.get('id_turma')

    if matricula is None or nome is None or descricao is None or id_turma is None:
        return jsonify({'message': 'Dados inválidos'}), 400

    aluno = AlunoDAO().get_aluno(matricula)
    if not aluno:
        return jsonify({'message': 'Aluno não encontrado'}), 404

    grupoDao = GrupoDAO()
    grupo = grupoDao.insert_grupo(nome, 5, descricao, aluno.matricula, id_turma)
    if grupo is None:
        return jsonify({'message': 'Grupo já existe'}), 400

    if not AlunoDAO().update_entrar_grupo(grupo.id_grupo, id_turma, aluno.matricula):
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
    curl -X POST http://localhost:5000/grupo/sair -H "Content-Type: application/json" -d "{\"matricula\": \"202208385192\", \"id_turma\": \"1\"}"
    """
    data = request.json
    matricula = data['matricula']
    id_turma = data['id_turma']

    aluno = AlunoDAO().get_aluno(matricula)
    grupo = GrupoDAO().get_grupo_by_matricula_aluno(aluno.matricula, id_turma)

    if not AlunoDAO().update_sair_grupo(aluno.matricula, grupo.id_turma):
        return jsonify({'message': 'Erro ao sair do grupo'}), 400

    return jsonify({'message': 'Aluno removido do grupo', 'grupo': grupo.__dict__(), 'aluno': aluno.__dict__()}), 200


@bp.route('/transferir', methods=['POST'])
def transferir():
    """
    Função que realiza a transferência de IbmecCoins.
    curl -X POST http://localhost:5000/grupo/transferir -H "Content-Type: application/json" -d "{\"matricula\": \"202208385192\", \"usuario\": \"202208385371\", \"quantidade\": \"10\", \"id_turma\": \"1\"}"
    """
    data = request.json
    remetente_matricula = data['matricula']
    destinatario_matricula = data['usuario']
    quantidade = int(data['quantidade'])
    id_turma = data['id_turma']

    remetente = AlunoDAO().get_aluno(remetente_matricula)
    destinatario = AlunoDAO().get_aluno(destinatario_matricula)
    grupo: Grupo = GrupoDAO().get_grupo_by_matricula_aluno(remetente.matricula, id_turma)

    if destinatario is None:
        return jsonify({'message': 'Destinário nao encontrado'}), 400

    if remetente is None:
        return jsonify({'message': 'Remetente nao encontrado'}), 400

    if grupo is None:
        return jsonify({'message': 'Grupo nao encontrado'}), 400

    if not TransacaoDAO().insert_transacao(remetente.matricula, destinatario.matricula, quantidade):
        return jsonify({'message': 'Nao foi possivel processar a transferencia'}), 400

    if not AlunoDAO().transferir_saldo_grupo(remetente.matricula, destinatario.matricula, quantidade, id_turma):
        return jsonify({'message': 'Erro ao transferir saldo'}), 400

    return jsonify({'message': 'Transferencia realizada com sucesso', 'aluno': remetente.__dict__(),
                    'grupo': grupo.__dict__()}), 200


@bp.route('/convidar', methods=['POST'])
def convidar():
    """
    Função que convida um aluno para o grupo.
    curl -X POST http://localhost:5000/grupo/convidar -H "Content-Type: application/json" -d "{\"matricula\": \"202208385192\", \"destinatario\": \"202208385371\", \"id_turma\": \"1\"}"
    """
    data = request.json
    remetente_matricula = data['matricula']
    destinatario_matricula = data['destinatario']
    id_turma = data['id_turma']

    remetente = AlunoDAO().get_aluno(remetente_matricula)
    destinatario = AlunoDAO().get_aluno(destinatario_matricula)

    if remetente is None:
        return jsonify({'message': 'Remetente nao encontrado'}), 400

    if destinatario is None:
        return jsonify({'message': 'Destinario nao encontrado'}), 400

    grupo = GrupoDAO().get_grupo_by_matricula_aluno(remetente.matricula, id_turma)

    if grupo is None:
        return jsonify({'message': 'Grupo nao encontrado'}), 400

    if not ConviteDAO().insert_convite(grupo.id_grupo, grupo.id_turma, destinatario.matricula):
        return jsonify({'message': 'Convite nao enviado'}), 400

    return jsonify(
        {'message': 'Convite enviado com sucesso',
         'grupo': grupo.__dict__(),
         'aluno': remetente.__dict__()}
    ), 200


@bp.route('/convites', methods=['POST'])
def convites():
    """
    Função que exibe os convites recebidos.
    curl -X POST http://localhost:5000/grupo/convites -H "Content-Type: application/json" -d "{\"matricula\": \"202208385192\"}"
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
    curl -X POST http://localhost:5000/grupo/aceitar -H "Content-Type: application/json" -d "{\"matricula\": \"202208385371\", \"id_convite\": \"1\"}"
    """
    data = request.json
    matricula = data['matricula']
    id_convite = data['id_convite']

    user = AlunoDAO().get_aluno(matricula)
    convite = ConviteDAO().get_convite(id_convite)

    if convite is None:
        return jsonify({'message': 'Convite nao encontrado'}), 400

    if AlunoDAO().update_entrar_grupo(convite.id_grupo, convite.id_turma, convite.convidado_matricula):
        grupo = GrupoDAO().get_grupo_by_id(convite.id_grupo)
        ConviteDAO().delete_convite(convite.id_convite)

        return jsonify({
            'message': 'Convite aceito com sucesso',
            'grupo': grupo.__dict__(),
            'aluno': user.__dict__()
        }), 200

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


@bp.route('/grupos', methods=['GET'])
def grupos():
    """
    Função que exibe todos os grupos.
    curl -X GET http://localhost:5000/grupo/grupos
    """
    lista_grupos: list = GrupoDAO().get_all_grupo()

    if lista_grupos is None:
        return jsonify({'message': 'Nenhum grupo encontrado'}), 400

    return jsonify({'grupos': [grupo.__dict__() for grupo in lista_grupos]}), 200
