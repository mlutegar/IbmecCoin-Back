import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db
from flaskr.dao.token_qr_code_dao import TokenQrCodeDao

bp = Blueprint('qrcode', __name__, url_prefix='/qrcode')

def criarToken():
    return "abcdef"
    # return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))


def gerar_qrcode(link):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    return img


@bp.route('/registro_token/<token>', methods=('GET', 'POST'))
def registro_token(token):
    tk = TokenQrCodeDao()

    if request.method == 'POST':
        error = None

        if error is None:
            try:
                tk.insert(token)
            # except db.IntegrityError:
            except:
                error = f"O {token} is already registered."
            else:
                return redirect(url_for("qrcode/exibir-token.html"))
        flash(error)
    return render_template('qrcode/registro-token.html', token=token)


# exibir token : função que recebe como parâmetro o token, gera o qrcode e exibe na tela
@bp.route('/exibir-token', methods=('GET', 'POST'))
def exibir_token(token):
    tk = TokenQrCodeDao()
    img = gerar_qrcode(token)

    return render_template('auth/exibir-token.html', img=img)
