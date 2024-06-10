from flask import Blueprint, request, jsonify
from flaskr.dao.aluno_dao import AlunoDAO
from flaskr.dao.item_comprado_dao import ItemCompradoDAO
from flaskr.dao.loja_dao import LojaDAO
from flaskr.dao.transacao_dao import TransacaoDAO
from flaskr.dao.user_dao import UserDAO

bp = Blueprint('loja', __name__, url_prefix='/loja')


@bp.route('/itens', methods=['GET'])
def itens():
    """
    Função que retorna em json os itens da loja.
    curl -X GET http://localhost:5000/loja/itens
    """
    lista_itens = LojaDAO().get_all_items()

    if lista_itens is None:
        return jsonify({'message': 'Erro ao carregar a pagina da loja'}), 400

    return jsonify({'itens': [item.__dict__() for item in lista_itens]}), 200


@bp.route('/itens-globais', methods=['GET'])
def itens_globais():
    """
    Função que retorna em json os itens da loja.
    curl -X GET http://localhost:5000/loja/itens-globais
    """
    lista_itens = LojaDAO().get_all_itens_global()

    if lista_itens is None:
        return jsonify({'message': 'Erro ao carregar a pagina da loja'}), 400

    return jsonify({'itens': [item.__dict__() for item in lista_itens]}), 200


@bp.route('/itens-turma/<int:id_turma>', methods=['GET'])
def itens_turma(id_turma):
    """
    Função que retorna em json os itens da loja de uma turma.
    curl -X GET http://localhost:5000/loja/itens-turma/1
    """
    lista_itens = LojaDAO().get_all_itens_by_id_turma(id_turma)

    if lista_itens is None:
        return jsonify({'message': 'Erro ao carregar a pagina da loja'}), 400

    return jsonify({'itens': [item.__dict__() for item in lista_itens]}), 200

@bp.route('/criar', methods=['POST'])
def criar():
    """
    Função que cria um item na loja.
    curl -X POST http://localhost:5000/loja/criar -H "Content-Type: application/json" -d "{\"nome\": \"Prova\", \"valor\": \"500\", \"id_turma\": \"1\"}"
    """
    data = request.json
    nome = data.get('nome')
    valor = data.get('valor')
    id_turma = data.get('id_turma')

    if not nome or not valor or not id_turma:
        return jsonify({'message': 'Preencha todos os campos'}), 400

    if LojaDAO().insert_item(id_turma, nome, valor):
        return jsonify({'itens': [item.__dict__() for item in LojaDAO().get_all_items()]}), 200

    return jsonify({'message': 'Erro ao adicionar item'}), 400


@bp.route('/item/<int:id_item>', methods=['GET'])
def item(id_item):
    """
    Função que retorna em json um item da loja.
    curl -X GET http://localhost:5000/loja/item/1
    """
    item_obj = LojaDAO().get_item(id_item)

    if item_obj is None:
        return jsonify({'message': 'Erro ao carregar a pagina do item'}), 400

    return jsonify({'item': item_obj.__dict__()}), 200


@bp.route('/comprar', methods=['POST'])
def comprar():
    """
    Função que realiza a compra de um item na loja.
    curl -X POST http://localhost:5000/loja/comprar -H "Content-Type: application/json" -d "{\"id_item\": \"1\", \"matricula\": \"202208385192\", \"id_turma\": \"1\"}"
    curl -X POST http://localhost:5000/loja/comprar -H "Content-Type: application/json" -d "{\"id_item\": \"1\", \"matricula\": \"202208385192\", \"id_turma\": \"0\"}"

    """
    data = request.json
    id_item = data['id_item']
    matricula = data['matricula']
    id_turma = data['id_turma']

    if not matricula:
        return jsonify({'message': 'Faca login para comprar'}), 401

    user = AlunoDAO().get_aluno(matricula)
    item_obj = LojaDAO().get_item(id_item)
    user_saldo = UserDAO().get_saldo_by_turma(matricula, id_turma)

    if user is None or item_obj is None:
        return jsonify({'message': 'Erro ao realizar a compra'}), 400

    if user_saldo is None:
        return jsonify({
            'message': 'Erro ao carregar saldo',
            'saldo': user_saldo
            }), 400

    if user_saldo < item_obj.valor:
        return jsonify({'message': 'Saldo insuficiente'}), 400

    if ItemCompradoDAO().buy_item(item_obj.id_item, user.matricula):
        if TransacaoDAO().insert_transacao_loja(user.matricula, item_obj.id_item):
            return jsonify({'message': 'Item comprado com sucesso!'}), 200
        else:
            return jsonify({'message': 'Erro no processo de salvar transacao/buy item'}), 400

    return jsonify({'message': 'Erro ao comprar item'}), 400
