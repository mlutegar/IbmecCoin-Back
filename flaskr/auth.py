import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.dao.aluno_dao import AlunoDAO
from flaskr.dao.professor_dao import ProfessorDAO
from flaskr.dao.user_dao import UserDAO
from flaskr.utils.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/registro', methods=('GET', 'POST'))
def registro():
    """
    Rota para registrar um usuário no sistema
    :return: página de registro
    """
    db = get_db()
    dao = UserDAO()
    pagina = "registro"

    # Se o método for POST, significa que o formulário foi submetido
    if request.method == 'POST':
        matricula = request.form['matricula']
        nome = request.form['nome']
        senha = request.form['senha']
        email = request.form['email']
        tipo = request.form['tipo']
        error = None

        # Verifica se os campos foram preenchidos
        if not matricula:
            error = 'Matricula is required.'
        elif not senha:
            error = 'Senha is required.'
        elif not tipo or tipo not in ["aluno", "professor"]:
            error = 'Tipo is required.'

        if len(matricula) < 9:
            flash('Matrícula inválida.')
            return render_template('auth/registro.html')

        if len(senha) < 8:
            flash('Senha inválida.')
            return render_template('auth/registro.html')

        if tipo == "aluno":
            dao = AlunoDAO()
        elif tipo == "professor":
            dao = ProfessorDAO()

        if error is None:
            try:
                if tipo == "aluno":
                    dao.insert_aluno(nome, matricula, generate_password_hash(senha), email)
                    pagina = "aluno.aluno"
                elif tipo == "professor":
                    dao.insert_professor(nome, matricula, generate_password_hash(senha), email)
                    pagina = "professor.professor"
            except db.IntegrityError:
                pass
            else:
                db.commit()
                user = dao.get_user(matricula)
                logar(user)
                return redirect(url_for(pagina))

    return render_template('auth/registro.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """
    Rota para conectar um usuário no sistema
    :return: página de login
    """
    dao = UserDAO()

    if request.method == 'POST':
        matricula = request.form['matricula']
        senha = request.form['senha']

        if not matricula:
            flash('Matrícula é obrigatória.')
            return render_template('auth/login.html')

        if not senha:
            flash('Senha é obrigatória.')
            return render_template('auth/login.html')

        error = None
        user = dao.get_user(matricula)

        if user is None:
            error = 'Incorrect matricula.'
        elif not check_password_hash(user.senha, senha):
            error = 'Senha incorreta.'

        if error is None:
            if user.tipo == "aluno":
                dao = AlunoDAO()
                user = dao.get_aluno(matricula)
            elif user.tipo == "professor":
                dao = ProfessorDAO()
                user = dao.get_professor(matricula)

            logar(user)

            if user.tipo == "aluno":
                return redirect(url_for('aluno.aluno'))
            elif user.tipo == "professor":
                return redirect(url_for('professor.professor'))
        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    """
    Função que carrega o login
    :return: usuário logado
    """
    matricula = session.get('matricula')

    if matricula is None:
        g.user = None
    else:
        dao = UserDAO()
        user = dao.get_user(matricula)
        if user.tipo == "aluno":
            dao = AlunoDAO()
            g.user = dao.get_aluno(matricula)
        elif user.tipo == "professor":
            dao = ProfessorDAO()
            g.user = dao.get_professor(matricula)
        else:
            g.user = None


@bp.route('/logout')
def logout():
    """
    Função que desconecta o usuário
    :return: página inicial
    """
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    """
    Função que verifica se o usuário está logado
    :param view: Função que será verificada
    :return: Função que verifica se o usuário está logado
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login_aluno'))

        return view(**kwargs)

    return wrapped_view


def logar(user):
    """
    Função que loga o usuário
    """
    user_str = str(user.matricula)
    session.clear()
    session['matricula'] = user_str
