import secrets
import segno
from datetime import datetime, timedelta
from flask import Blueprint, flash, redirect, render_template, request, url_for, session

from flaskr.dao.aluno_dao import AlunoDAO
from flaskr.dao.qrcode_dao import QrCodeDAO

bp = Blueprint('qrcode', __name__, url_prefix='/qrcode')


@bp.route('/criar', methods=('GET', 'POST'))
def criar():
    """
    Função que exibe a página de criação de qrcode, permitindo que o usuário adicione o valor, a validade e a quantidade
    de usos do qrcode
    :return: renderiza a página de criação de qrcode
    """
    if request.method == 'POST':
        valor = request.form['valor']
        validade = request.form['validade_data']
        validade = datetime.strptime(validade, '%Y-%m-%d')
        qtd_usos = request.form['qtd_usos']

        tk = QrCodeDAO()
        token = secrets.token_urlsafe()

        if tk.insert_qrcode(token, int(valor), validade, int(qtd_usos)):
            flash("Token criado com sucesso")
            return redirect(url_for('qrcode.foto', token=token))
        else:
            flash("Erro ao criar o token")
            return redirect(url_for('error.erro'))

    return render_template('qrcode/criar.html')


@bp.route('/foto/<token>', methods=('GET', 'POST'))
def foto(token):
    """
    Função que exibe a foto do qrcode na tela a partir de um token. Se o token não for passado, um novo token é gerado.
    :param token: Token a ser utilizado no qrcode
    :return: Renderiza a página com a foto do qrcode
    """

    if token == "last":
        token = recuperarUltimoToken()

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
    if 'matricula' not in session:
        return redirect(url_for('auth.login'))

    aluno = AlunoDAO().get_aluno(session['matricula'])
    qrcode = QrCodeDAO().get_qrcode(token)

    if qrcode is None:
        flash("Token não existe")
        return redirect(url_for("qrcode.leitor"))

    if qrcode.validade_data > datetime.now():
        AlunoDAO().update_aumentar_saldo(aluno.matricula, qrcode.valor)
        QrCodeDAO().update_diminuir_qtd_usos(qrcode.token)
        return redirect(url_for("aluno.aluno", token=token))
    else:
        flash("Token vencido")
        return redirect(url_for("qrcode.leitor"))

    return render_template('qrcode/validar.html', token=qrcode.token)

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
