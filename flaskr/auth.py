import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.dao.aluno_dao import AlunoDao
from flaskr.dao.professor_dao import ProfessorDao
from flaskr.dao.user_dao import UserDao
from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

# registro_user: rota para registrar um aluno no sistema
@bp.route('/registro_user', methods=('GET', 'POST'))
def registro_user():
    aluno = AlunoDao()
    professor = ProfessorDao()
    user = UserDao()

    # Se o método for POST, significa que o formulário foi submetido
    if request.method == 'POST':
        matricula = request.form['matricula']
        senha = request.form['senha']
        tipo = request.form['tipo']
        error = None

        # Verifica se os campos foram preenchidos
        if not matricula:
            error = 'Matricula is required.'
        elif not senha:
            error = 'Senha is required.'
        elif not tipo or tipo not in ["aluno", "professor"]:
            error = 'Tipo is required.'

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
                    professor.insert(id)
            except user.get_db().IntegrityError:
                error = f"User {matricula} is already registered."
            else:
                return redirect(url_for("index"))
        flash(error)

    return render_template('auth/registro_user.html')

@bp.route('/login_user', methods=('GET', 'POST'))
def login_user():
    userDao = UserDao()

    if request.method == 'POST':
        matricula = request.form['matricula']
        senha = request.form['senha']
        db = get_db()
        error = None

        tipo = userDao.get_tipo_by_matricula(matricula)

        if tipo == "aluno":
            user = db.execute(
                'SELECT * FROM user u JOIN aluno a ON u.id_user = a.id_user WHERE matricula = ?', (matricula,)
            ).fetchone()

        user = db.execute(
            'SELECT * FROM user WHERE matricula = ?', (matricula,)
        ).fetchone()

        if user is None:
            error = 'Incorrect matricula.'
        elif not check_password_hash(user['senha'], senha):
            error = 'Senha incorreta.'

        if error is None:
            session.clear()
            session['user_id'] = user['id_user']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login_user.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    user_cargo = session.get('user_cargo')

    if user_id is None:
        g.user = None
    elif user_cargo == "0":
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id_user = ?', (user_id,)
        ).fetchone()
    elif user_cargo == "1":
        g.professor = get_db().execute(
            'SELECT * FROM user WHERE id_user = ?', (user_id,)
        ).fetchone()
    else:
        g.user = None


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login_aluno'))

        return view(**kwargs)

    return wrapped_view
