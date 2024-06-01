from flask import Blueprint, render_template

bp = Blueprint('error', __name__, url_prefix='/error')


@bp.route('/error', methods=('GET', 'POST'))
def error():
    """
    Função que exibe a página de erro.
    :return: Renderiza a página de erro
    """
    return render_template('error.html')