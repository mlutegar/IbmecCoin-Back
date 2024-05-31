import os

from flaskr.dao.user_dao import UserDAO
from flaskr.utils import db
from flask import Flask, render_template, redirect, url_for, session


def create_app(test_config=None):
    """
    Cria a aplicação Flask principal.
    :param test_config: Argumento opcional que permite passar configurações para a aplicação
    :return: retorna a aplicação Flask criada
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Inicializando o banco de dados
    from flaskr.utils import db
    db.init_app(app)

    @app.route('/')
    def index():
        """
        Rota principal da aplicação, retorna uma mensagem de boas-vindas.
        :return: Retorna uma mensagem de boas-vindas
        """
        if 'matricula' in session:
            matricula = session['matricula']
            dao = UserDAO()
            user = dao.get_user(matricula)
            if user.tipo == 'aluno':
                return redirect(url_for('aluno.aluno'))
            elif user.tipo == 'professor':
                return redirect(url_for('professor.professor'))

        return render_template('index.html')

    from . import aluno, auth, grupo, professor, qrcode, turma
    app.register_blueprint(aluno.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(grupo.bp)
    app.register_blueprint(professor.bp)
    app.register_blueprint(qrcode.bp)
    app.register_blueprint(turma.bp)

    app.add_url_rule('/', endpoint='index')

    return app
