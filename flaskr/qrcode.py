import functools
import qrcode
import secrets

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr.db import get_db
from flaskr.dao.token_qr_code_dao import TokenQrCodeDao

bp = Blueprint('qrcode', __name__, url_prefix='/qrcode')

def criarToken():
    return secrets.token_urlsafe()

def gerar_qrcode(link):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    return img


@bp.route('/registro_token/', methods=('GET', 'POST'))
def registro_token():
    tk = TokenQrCodeDao()

    if request.method == 'POST':
        error = None
        token = criarToken()
        if error is None:
            try:
                tk.insert(token)
                return redirect(url_for("qrcode.exibir_token", token=token))
            except IntegrityError:
                error = f"O {token} is already registered."
                flash(error)
                return redirect(url_for("index"))


# exibir token : função que recebe como parâmetro o token, gera o qrcode e exibe na tela
@bp.route('/exibir-token/<token>', methods=('GET'))
def exibir_token(token):
    tk = TokenQrCodeDao()
    img = gerar_qrcode(token)

    return render_template('auth/exibir-token.html', img=img)
