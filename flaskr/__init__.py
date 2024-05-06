import os

from flask import Flask, jsonify
import datetime

def create_app(test_config=None): # test_config=None é um argumento opcional
    # create and configure the app
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
    from . import db
    db.init_app(app)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # Route for returning data
    @app.route('/data')
    def get_data():
        """
        Retorna dados para exibição em uma aplicação React.
        """
        # Obtendo a data e hora atual
        x = datetime.datetime.now()

        # Retornando dados no formato JSON
        return jsonify({
            'Name': "geek",
            "Age": "22",
            "Date": x.strftime("%Y-%m-%d %H:%M:%S"),
            "Programming": "Python"
        })

    from . import auth, qrcode, debugger, blog
    app.register_blueprint(auth.bp)
    app.register_blueprint(qrcode.bp)
    app.register_blueprint(debugger.bp)
    app.register_blueprint(blog.bp)

    app.add_url_rule('/', endpoint='index')

    return app