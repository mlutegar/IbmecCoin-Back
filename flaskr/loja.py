from flask import Blueprint, render_template, flash, request, g, session

from flaskr.auth import login_required
from flaskr.dao.aluno_dao import AlunoDAO
from flaskr.dao.item_comprado_dao import ItemCompradoDAO
from flaskr.dao.loja_dao import LojaDAO
from flaskr.dao.transacao_dao import TransacaoDAO

bp = Blueprint('loja', __name__, url_prefix='/loja')


@login_required
@bp.route('/loja', methods=('GET', 'POST'))
def loja():
    """
    Função que renderiza a página da loja
    :return: Renderiza a página da loja
    """
    matricula = session['matricula']

    aluno = AlunoDAO().get_aluno(matricula)
    lista_itens = LojaDAO().get_all_items()

    if aluno is None or lista_itens is None:
        flash('Erro ao carregar a página da loja')
        return render_template('/')

    return render_template('loja/loja.html', itens=lista_itens, aluno=aluno)

@bp.route('/item/<id_item>', methods=('GET', 'POST'))
def item(id_item):
    """
    Função que renderiza a página de um item
    :param id_item: id do item
    :return: Renderiza a página do item
    """
    item = LojaDAO().get_item(id_item)

    if item is None:
        flash('Erro ao carregar a página do item')
        return render_template('/')

    return render_template('loja/item.html', item=item)

@bp.route('/comprar/<id_item>', methods=('GET', 'POST'))
def comprar(id_item):
    """
    Função que realiza a compra de um item
    :param id_item: id do item
    :return: Redireciona para a página da loja
    """
    matricula = session['matricula']

    aluno = AlunoDAO().get_aluno(matricula)
    item_obj = LojaDAO().get_item(id_item)

    if aluno is None or item_obj is None:
        flash('Erro ao realizar a compra')
        return render_template('loja/loja.html', itens=LojaDAO().get_all_items(), aluno=aluno)

    if aluno.saldo < item_obj.valor:
        flash('Saldo insuficiente')
        return render_template('loja/loja.html', itens=LojaDAO().get_all_items(), aluno=aluno)

    ItemCompradoDAO().buy_item(item_obj.id_item, aluno.matricula)
    TransacaoDAO().insert_transacao_loja(aluno.matricula, item_obj.id_item)
    flash('Compra realizada com sucesso')

    return render_template('loja/comprar.html')

