import secrets
import segno
from datetime import datetime, timedelta
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flaskr.dao.qrcode_dao import QrCodeDAO

bp = Blueprint('qrcode', __name__, url_prefix='/qrcode')


@bp.route('/foto/<token>', methods=('GET', 'POST'))
def foto(token):
    """
    Função que exibe a foto do qrcode na tela a partir de um token. Se o token não for passado, um novo token é gerado.
    :param token: Token a ser utilizado no qrcode
    :return: Renderiza a página com a foto do qrcode
    """

    if token == "last":
        token = recuperarUltimoToken()

    if token == "new":
        token = criar_token(1, datetime.today() + timedelta(days=1))

    img = gerarQrcode(token)

    return render_template('qrcode/foto.html', token=token, img=img)


@bp.route('/leitor', methods=('GET', 'POST'))
def leitor():
    """
    Função que exibe a página do leitor de qrcode, permite que o usuário adiciona o token manualmente ou escaneie o
    qrcode que resgatará o token e verificará se o token é válido e caso for, adicionará saldo na conta do usuário
    aluno
    :return: renderiza a página do leitor de qrcode
    """
    if request.method == 'POST':
        token = request.form['token']
        tk = QrCodeDAO()
        if tk.get_qrcode(token) is not None:
            return redirect(url_for("qrcode.validar", token=token))
        else:
            flash("Token inválido")
            return redirect(url_for("qrcode.leitor"))
    return render_template('qrcode/leitor.html')


@bp.route('/validar/<token>', methods=('GET', 'POST'))
def validar(token):
    """
    Função que valida um token, adiciona saldo na conta do usuário aluno e o desativa.
    :param token: Token a ser utilizado no qrcode
    :return: Renderiza a página de sucesso
    """
    tk = QrCodeDAO()
    tk.get_qrcode(token)
    return render_template('qrcode/validar.html', token=token)


def criar_token(valor, validade):
    """
    Função que cria um token para ser utilizado no qrcode
    :return: token gerado pelo método token_urlsafe
    """
    tk = QrCodeDAO()
    token = secrets.token_urlsafe()

    if tk.insert_qrcode(token, valor, validade):
        return token

    return None



def recuperarUltimoToken():
    """
    Função que recupera o último token gerado
    :return: o último token gerado
    """
    tk = QrCodeDAO()
    return tk.get_last_qrcode()


def gerarQrcode(token):
    """
    Função que gera uma imagem de qrcode, usando a biblioteca segno, a partir de um token e retorna a imagem em formato
    base64
    :param token:
    :return: uma string com a imagem em formato base64
    """
    qr = segno.make_qr(token)
    return qr.svg_data_uri(scale=5)

#
#
# @bp.route('/registro_token/', methods=('GET', 'POST'))
# def registro_token():
#     tk = TokenQrCodeDao()
#
#     if request.method == 'POST':
#         error = None
#         token = criarToken()
#         if error is None:
#             try:
#                 tk.insert(token)
#                 return redirect(url_for("qrcode.exibir_token", token=token))
#             except IntegrityError:
#                 error = f"O {token} is already registered."
#                 flash(error)
#                 return redirect(url_for("index"))
#
#
# # exibir token : função que recebe como parâmetro o token, gera o qrcode e exibe na tela
# @bp.route('/exibir-token/<token>', methods=('GET'))
# def exibir_token(token):
#     tk = TokenQrCodeDao()
#     img = gerar_qrcode(token)
#
#     return render_template('auth/exibir-token.html', img=img)
