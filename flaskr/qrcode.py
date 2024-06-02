import secrets
import segno
import io
import imageio

from datetime import datetime
from flaskr.dao.aluno_dao import AlunoDAO
from flask import Blueprint, flash, redirect, render_template, request, url_for, session, jsonify
from pyzbar.pyzbar import decode
from flaskr.dao.qrcode_dao import QrCodeDAO

bp = Blueprint('qrcode', __name__, url_prefix='/qrcode')


@bp.route('/criar', methods=('GET', 'POST'))
def criar():
    """
    Função que exibe a página de criação de qrcode, permitindo que o usuário adicione o valor, a validade e a quantidade
    de usos do qrcode
    :return: renderiza a página de criação de qrcode
    """
    data = request.json
    valor = data['valor']
    validade_data = data['validade_data']
    qtd_usos = data['qtd_usos']

    try:
        validade_data = datetime.strptime(validade_data, '%Y-%m-%d')
    except ValueError as e:
        return jsonify({'message': f"Data invalida: {str(e)}"}), 400

    tk = QrCodeDAO()
    token = secrets.token_urlsafe()

    if tk.insert_qrcode(token, int(valor), validade_data, int(qtd_usos)):
        return jsonify({'token': token}), 200
    else:
        return jsonify({'message': "Erro ao criar o token"}), 400


@bp.route('/foto', methods=('GET', 'POST'))
def foto():
    """
    Função que exibe a foto do qrcode na tela a partir de um token. Se o token não for passado, um novo token é gerado.
    :return: Renderiza a página com a foto do qrcode
    """
    data = request.json
    token = data['token']
    if token == "last":
        token = recuperarUltimoToken()
    img = gerarQrcode(token)

    return jsonify({
        'token': token,
        'img': img
    }), 200


@bp.route('/leitor', methods=('GET', 'POST'))
def leitor():
    """
    Função que exibe a página do leitor de qrcode, permite que o usuário adicione o token manualmente ou escaneie o
    qrcode que resgatará o token e verificará se o token é válido e caso for, adicionará saldo na conta do usuário
    aluno
    :return: renderiza a página do leitor de qrcode
    """
    data = request.json
    id_form = data['id_form']

    if id_form == 'validate_qr':
        token = data['token']
        tk = QrCodeDAO()
        if tk.get_qrcode(token) is not None:
            return jsonify({
                'token': token
            }), 200
        else:
            return jsonify({'message': "Validate_qr - Token invalido"}), 400

    elif id_form == 'upload_file':
        file = data['file']
        if file and file.filename != '':
            # Carregar a imagem em memória usando imageio
            image = imageio.v2.imread(io.BytesIO(file.read()))
            # Decodificar o QR code
            decoded_objects = decode(image)
            if decoded_objects:
                token = decoded_objects[0].data.decode('utf-8')
                tk = QrCodeDAO()
                if tk.get_qrcode(token) is not None:
                    return jsonify({'token': token}), 200
                else:
                    return jsonify({'message': "upload_file - Erro ao validar o token"}), 400
            else:
                return jsonify({'message': "Nenhum QR code encontrado na imagem"}), 400

    return jsonify({'message': "Erro ao escolher o tipo de envio do token"}), 400


@bp.route('/validar', methods=('GET', 'POST'))
def validar():
    """
    Função que valida um token, adiciona saldo na conta do usuário aluno e o desativa.
    :param token: Token a ser utilizado no qrcode
    :return: Renderiza a página de sucesso
    """
    data = request.json
    token = data['token']
    matricula = data['matricula']

    aluno = AlunoDAO().get_aluno(matricula)
    qrcode = QrCodeDAO().get_qrcode(token)

    if qrcode is None:
        return jsonify({'message': "Token não existe"}), 400

    if qrcode.validade_data > datetime.now():
        AlunoDAO().update_aumentar_saldo(aluno.matricula, qrcode.valor)
        QrCodeDAO().update_diminuir_qtd_usos(qrcode.token)
        return jsonify({'message': "Token validado com sucesso"}), 200
    else:
        return jsonify({'message': "Token vencido"}), 400

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
