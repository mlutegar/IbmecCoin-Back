import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.dao.aluno_dao import AlunoDao
from flaskr.dao.professor_dao import ProfessorDao
from flaskr.dao.user_dao import UserDao
from flaskr.db import get_db
from flaskr.util.debugger import debugger

bp = Blueprint('auth', __name__, url_prefix='/auth')

# registro_user: rota para registrar um aluno no sistema
@bp.route('/registro_user', methods=('GET', 'POST'))
def registro_user():
    # Instanciando os DAOs
    aluno = AlunoDao()
    professor = ProfessorDao()
    user = UserDao()

    # Se o método for POST, significa que o formulário foi submetido
    if request.method == 'POST':
        matricula = request.form['matricula']
        senha = request.form['senha']
        tipo = request.form['tipo']
        error = None

        debugger(f"matricula: {matricula}, senha: {senha}, tipo: {tipo}, error: {error}")

        # Verifica se os campos foram preenchidos
        if not matricula:
            error = 'Matricula is required.'
        elif not senha:
            error = 'Senha is required.'
        elif not tipo or tipo not in ["aluno", "professor"]:
            error = 'Tipo is required.'

        if len(matricula) < 9:
            flash('Matrícula inválida.')
            return render_template('auth/registro_user.html')

        if len(senha) < 8:
            flash('Senha inválida.')
            return render_template('auth/registro_user.html')

        debugger(f"matricula: {matricula}, senha: {senha}, tipo: {tipo}, error: {error}")

        # Se não houver erro, tenta inserir o aluno no banco de dados, senão, exibe o erro na tela e não insere
        if error is None:
            try:
                if user.insert(matricula, generate_password_hash(senha), tipo) == 1:
                    id = user.get_id_by_matricula(matricula)
                    if id == -1:
                        error = f"Erro na obtenção do id do usuário {matricula}."
                        return error
                else:
                    error = f"Erro ao inserir usuário {matricula}."
                    return error

                if tipo == "aluno":
                    aluno.insert(id)
                elif tipo == "professor":
                    if professor.insert(id) == -1:
                        error = f"Erro ao inserir professor {matricula}."
                        return error
            except user.get_db().IntegrityError:
                error = f"User {matricula} is already registered."
            else:
                return redirect(url_for("index"))
        flash(error)

    return render_template('auth/registro_user.html')

# login_aluno: rota para logar um aluno no sistema
@bp.route('/login_user', methods=('GET', 'POST'))
def login_user():
    userDao = UserDao()

    if request.method == 'POST':
        matricula = request.form['matricula']
        senha = request.form['senha']

        if not matricula:
            flash('Matrícula é obrigatória.')
            return render_template('auth/login_user.html')

        if not senha:
            flash('Senha é obrigatória.')
            return render_template('auth/login_user.html')

        if len(matricula) < 9:
            flash('Matrícula inválida.')
            return render_template('auth/login_user.html')

        if len(senha) < 8:
            flash('Senha inválida.')
            return render_template('auth/login_user.html')

        error = None

        tipo = userDao.get_tipo_by_matricula(matricula)

        if tipo == -1:
            flash("Matrícula inválida.")
            return render_template('auth/login_user.html')

        if tipo == "aluno":
            user = userDao.select_aluno_by_matricula(matricula)
        elif tipo == "professor":
            user = userDao.select_professor_by_matricula(matricula)

        if user is None:
            error = 'Incorrect matricula.'
        elif not check_password_hash(user['senha'], senha):
            error = 'Senha incorreta.'

        # debug
        debugger(f"error: {error}")

        if error is None:
            session.clear()
            session['user_id'] = user['id_user']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login_user.html')

# load_logged_in_user: função que carrega o usuário logado
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        user = UserDao()
        if user.get_tipo_by_id(user_id) == "aluno":
            g.user = user.select_aluno(user_id)
        elif user.get_tipo_by_id(user_id) == "professor":
            g.user = user.select_professor(user_id)
        else:
            g.user = None

# logout: rota para deslogar um usuário
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# login_required: função que verifica se o usuário está logado
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login_aluno'))

        return view(**kwargs)

    return wrapped_view
