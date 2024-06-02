from flask import Blueprint, request, jsonify
from flaskr.dao.aluno_dao import AlunoDAO
from flaskr.dao.item_comprado_dao import ItemCompradoDAO
from flaskr.dao.loja_dao import LojaDAO
from flaskr.dao.transacao_dao import TransacaoDAO
from flaskr.dao.user_dao import UserDAO

bp = Blueprint('loja', __name__, url_prefix='/loja')


@bp.route('/loja', methods=['POST'])
def loja():
    """
    Função que retorna em json os itens da loja.
    curl -X POST http://localhost:5000/loja/loja -H "Content-Type: application/json" -d "{\"matricula\": \"1\"}"
    """
    data = request.json
    matricula = data['matricula']

    user = UserDAO().get_user(matricula)
    if user.tipo == 'aluno':
        user = AlunoDAO().get_aluno(matricula)

    lista_itens = LojaDAO().get_all_items()

    if user is None or lista_itens is None:
        return jsonify({'message': 'Erro ao carregar a pagina da loja'}), 400

    return jsonify({'itens': [item.__dict__() for item in lista_itens], 'user': user.__dict__()}), 200

@bp.route('/criar', methods=['POST'])
def criar():
    """
    Função que cria um item na loja.
    curl -X POST http://localhost:5000/loja/criar -H "Content-Type: application/json" -d "{\"nome\": \"Prova\", \"valor\": \"500\"}"
    """
    data = request.json
    nome = data.get('nome')
    valor = data.get('valor')

    if not nome or not valor:
        return jsonify({'message': 'Preencha todos os campos'}), 400

    if LojaDAO().insert_item(nome, valor):
        return jsonify({'itens': [item.__dict__() for item in LojaDAO().get_all_items()]}), 200

    return jsonify({'message': 'Erro ao adicionar item'}), 400

@bp.route('/item', methods=['POST'])
def item():
    """
    Função que retorna em json um item da loja.
    curl -X POST http://localhost:5000/loja/item -H "Content-Type: application/json" -d "{\"id_item\": \"1\"}"
    """
    data = request.json
    id_item = data['id_item']

    item_obj = LojaDAO().get_item(id_item)

    if item_obj is None:
        return jsonify({'message': 'Erro ao carregar a pagina do item'}), 400

    return jsonify({'item': item_obj.__dict__()}), 200


@bp.route('/comprar', methods=['POST'])
def comprar():
    """
    Função que realiza a compra de um item na loja.

    """
    data = request.json
    id_item = data['id_item']
    matricula = data['matricula']

    if not matricula:
        return jsonify({'message': 'Faca login para comprar'}), 401

    user = AlunoDAO().get_aluno(matricula)
    item_obj = LojaDAO().get_item(id_item)

    if user is None or item_obj is None:
        return jsonify({'message': 'Erro ao realizar a compra'}), 400

    if user.saldo < item_obj.valor:
        return jsonify({'message': 'Saldo insuficiente'}), 400

    if ItemCompradoDAO().buy_item(item_obj.id_item, user.matricula):
        if TransacaoDAO().insert_transacao_loja(user.matricula, item_obj.id_item):
            return jsonify({'message': 'Item comprado com sucesso!'}), 200
        else:
            return jsonify({'message': 'Erro no processo de salvar transacao/buy item'}), 400

    return jsonify({'message': 'Erro ao comprar item'}), 400
