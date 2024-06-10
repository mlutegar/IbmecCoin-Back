from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.dao.aluno_dao import AlunoDAO
from flaskr.dao.professor_dao import ProfessorDAO
from flaskr.dao.user_dao import UserDAO
from flaskr.utils.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/registro', methods=['POST'])
def registro():
    """
    Função para registrar um usuário.
    curl -X POST http://localhost:5000/auth/registro -H "Content-Type: application/json" -d "{\"matricula\": \"1\", \"nome\": \"Nome\", \"senha\": \"senha\", \"email\": \"email@example.com\", \"tipo\": \"aluno\"}"
    """
    data = request.json
    matricula = data.get('matricula')
    nome = data.get('nome')
    senha = data.get('senha')
    email = data.get('email')
    tipo = data.get('tipo')
    error = None

    dao = UserDAO()

    if not matricula:
        error = 'Matricula is required.'
    elif not senha:
        error = 'Senha is required.'
    elif not tipo or tipo not in ["aluno", "professor"]:
        error = 'Tipo is required.'

    if UserDAO().get_user(matricula) is not None:
        return jsonify({'message': 'User already exists'}), 400

    if tipo == "aluno":
        dao = AlunoDAO()
    elif tipo == "professor":
        dao = ProfessorDAO()

    if error is None:
        try:
            if tipo == "aluno":
                dao.insert_aluno(nome, matricula, generate_password_hash(senha), email)
            elif tipo == "professor":
                dao.insert_professor(nome, matricula, generate_password_hash(senha), email)
        except get_db().IntegrityError:
            return jsonify({'message': 'User already exists'}), 400
        else:
            user = dao.get_user(matricula)
            return jsonify({'message': 'User registered successfully', 'user': user.__dict__()}), 200

    return jsonify({'message': error}), 400


@bp.route('/login', methods=['POST'])
def login():
    """
    Função para conectar um usuário no sistema.
    curl -X POST http://localhost:5000/auth/login -H "Content-Type: application/json" -d "{\"matricula\": \"1\", \"senha\": \"senha\"}"
    """
    data = request.json
    matricula = data.get('matricula')
    senha = data.get('senha')

    if not matricula:
        return jsonify({'message': 'Matricula é obrigatoria.'}), 400

    if not senha:
        return jsonify({'message': 'Senha é obrigatoria.'}), 400

    user = UserDAO().get_user(matricula)

    if user is None or not check_password_hash(user.senha, senha):
        return jsonify({'message': 'Invalid credentials'}), 401

    return jsonify({'message': 'Login successful', 'user': user.__dict__()}), 200


# curl -X POST http://localhost:5000/auth/verificar-usuario -H "Content-Type: application/json" -d "{\"matricula\": \"1\"}"
@bp.route('/verificar-usuario', methods=['POST'])
def verificar_usuario():
    """
    Função para verificar se um usuário está logado.
    """
    data = request.json
    matricula = data.get('matricula')

    if not matricula:
        return jsonify({'message': 'Matricula é obrigatoria.'}), 400

    user = UserDAO().get_user(matricula)

    if user is None:
        return jsonify({'message': 'User not found'}), 400

    return jsonify({'message': 'User found', 'user': user.__dict__()}), 200
