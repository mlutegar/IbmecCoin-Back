"""
Módulo que contém as funções relacionadas ao transferência de IbmecCoins.
- A rota /transferir: exibe a página de transferência de IbmecCoins.
- A rota /transferir/<id>: transfere IbmecCoins para outro usuário.
- A rota /transferir/<id>/confirmar: confirma a transferência de IbmecCoins para outro usuário.
"""
from flask import Blueprint

bp = Blueprint('transfer', __name__, url_prefix='/transfer')

@bp.route('/transferir', methods=('GET', 'POST'))
def transferir():
    """
    Função que exibe a página de transferência de IbmecCoins.
    :return: renderiza a página de transferência de IbmecCoins
    """
    return render_template('transfer/transferir.html')