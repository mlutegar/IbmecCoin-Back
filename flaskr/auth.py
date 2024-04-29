import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/registro_aluno', methods=('GET', 'POST'))
def registro_aluno():
    if request.method == 'POST':
        # Recebe os dados do formulário
        matricula = request.form['matricula']
        senha = request.form['senha']
        db = get_db()
        error = None

        if not matricula:
            error = 'Matricula is required.'
        elif not senha:
            error = 'Senha is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO aluno (matricula, senha) VALUES (?, ?)",
                    (matricula, generate_password_hash(senha)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {matricula} is already registered."
            else:
                return redirect(url_for("auth.login_aluno"))

        flash(error)

    return render_template('auth/registro_aluno.html')

@bp.route('/registro_professor', methods=('GET', 'POST'))
def registro_professor():
    if request.method == 'POST':
        # Recebe os dados do formulário
        matricula = request.form['matricula']
        senha = request.form['senha']
        db = get_db()
        error = None

        if not matricula:
            error = 'Matricula is required.'
        elif not senha:
            error = 'Senha is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO professor (matricula, senha) VALUES (?, ?)",
                    (matricula, generate_password_hash(senha)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {matricula} is already registered."
            else:
                return redirect(url_for("auth.login_professor"))

        flash(error)

    return render_template('auth/registro_professor.html')

@bp.route('/login_aluno', methods=('GET', 'POST'))
def login_aluno():
    if request.method == 'POST':
        matricula = request.form['matricula']
        senha = request.form['senha']
        db = get_db()
        error = None
        aluno = db.execute(
            'SELECT * FROM aluno WHERE matricula = ?', (matricula,)
        ).fetchone()

        if aluno is None:
            error = 'Incorrect matricula.'
        elif not check_password_hash(aluno['senha'], senha):
            error = 'Senha incorreta.'

        if error is None:
            session.clear()
            session['user_id'] = aluno['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login_aluno.html')

@bp.route('/login_professor', methods=('GET', 'POST'))
def login_professor():
    if request.method == 'POST':
        matricula = request.form['matricula']
        senha = request.form['senha']
        db = get_db()
        error = None
        professor = db.execute(
            'SELECT * FROM professor WHERE matricula = ?', (matricula,)
        ).fetchone()

        if professor is None:
            error = 'Incorrect matricula.'
        elif not check_password_hash(professor['senha'], senha):
            error = 'Incorrect senha.'

        if error is None:
            session.clear()
            session['user_id'] = professor['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login_professor.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.aluno = None
    else:
        g.aluno = get_db().execute(
            'SELECT * FROM aluno WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.aluno is None:
            return redirect(url_for('auth.login_aluno'))

        return view(**kwargs)

    return wrapped_view
