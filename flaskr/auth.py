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
        password = request.form['password']
        db = get_db()
        error = None

        if not matricula:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO aluno (matricula, password) VALUES (?, ?)",
                    (matricula, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {matricula} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/registro_aluno.html')

@bp.route('/registro_professor', methods=('GET', 'POST'))
def registro_professor():
    if request.method == 'POST':
        # Recebe os dados do formulário
        matricula = request.form['matricula']
        password = request.form['password']
        db = get_db()
        error = None

        if not matricula:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO professor (matricula, password) VALUES (?, ?)",
                    (matricula, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {matricula} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/registro_professor.html')

@bp.route('/login_aluno', methods=('GET', 'POST'))
def login_aluno():
    if request.method == 'POST':
        matricula = request.form['matricula']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM aluno WHERE matricula = ?', (matricula,)
        ).fetchone()

        if user is None:
            error = 'Incorrect matricula.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login_aluno.html')

@bp.route('/login_professor', methods=('GET', 'POST'))
def login_professor():
    if request.method == 'POST':
        matricula = request.form['matricula']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM professor WHERE matricula = ?', (matricula,)
        ).fetchone()

        if user is None:
            error = 'Incorrect matricula.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login_professor.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM aluno WHERE id = ?', (user_id,)
        ).fetchone()


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
