from flask import Blueprint, render_template, request, flash, session
from flaskr.dao.aluno_dao import AlunoDAO
from flaskr.dao.convite_dao import ConviteDAO
from flaskr.dao.grupo_dao import GrupoDAO
from flaskr.utils.transfer import processar_transferencia

bp = Blueprint('grupo', __name__, url_prefix='/grupo')


@bp.route('/informacao', methods=('GET', 'POST'))
def informacao():
    """
    Função que exibe a página de informações do grupo do aluno.
    """
    matricula = session['matricula']
    if matricula is None:
        return render_template('index.html')

    alunoDao = AlunoDAO()
    aluno = alunoDao.get_aluno(matricula)
    id_grupo = aluno.get_grupo_id()
    grupoDao = GrupoDAO()
    grupo = grupoDao.get_grupo_by_id(id_grupo)

    return render_template('grupo/informacao.html', grupo=grupo, aluno=aluno)


@bp.route('/criar', methods=('GET', 'POST'))
def criar():
    """
    Função que exibe a página de criação de grupo.
    """
    alunoDao = AlunoDAO()
    matricula = session['matricula']
    if matricula is None:
        return render_template('index.html')

    aluno = alunoDao.get_aluno(matricula)
    grupoDao = GrupoDAO()

    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']

        if not grupoDao.insert_grupo(nome, 5, descricao, aluno.matricula):
            error = 'Grupo já existe.'
            flash(error)
            return render_template('grupo/criar.html')
        else:
            return render_template(
                'grupo/informacao.html',
                grupo=grupoDao.get_grupo_by_matricula(aluno.matricula),
                aluno=aluno
            )

    return render_template('grupo/criar.html')


@bp.route('/transferir', methods=('GET', 'POST'))
def transferir():
    """
    Função que exibe a página de transferência de IbmecCoins.
    Essa função também é responsável por processar o post do formulário de transferência de IbmecCoins.
    """
    alunoDao = AlunoDAO()
    matricula = session['matricula']
    if matricula is None:
        return render_template('index.html')

    remetente = alunoDao.get_aluno(matricula)

    if request.method == 'POST':
        destinatario = request.form['destinatario']
        quantidade = request.form['quantidade']

        destinatario = alunoDao.get_aluno(destinatario)
        quantidade = int(quantidade)

        if destinatario is None:
            flash('Usuário não encontrado')
            return render_template('grupo/transferir.html')

        if not processar_transferencia(remetente, destinatario, quantidade):
            flash('Transferência não realizada')
            return render_template('grupo/transferir.html')

        flash('Transferência realizada com sucesso')
        return render_template('grupo/informacao.html')

    return render_template('grupo/transferir.html')


@bp.route('/convidar', methods=('GET', 'POST'))
def convidar():
    """
    Função que exibe a página de convite de alunos para o grupo.
    """
    alunoDao = AlunoDAO()
    grupoDao = GrupoDAO()
    conviteDao = ConviteDAO()

    matricula = session['matricula']
    if matricula is None:
        return render_template('index.html')
    remetente = alunoDao.get_aluno(matricula)
    grupo = grupoDao.get_grupo_by_id(remetente.get_grupo_id())

    if request.method == 'POST':
        destinatario = request.form['matricula']
        destinatario = alunoDao.get_aluno(destinatario)

        if destinatario is None:
            flash('Usuário não encontrado')
            return render_template('grupo/convidar.html')

        if not conviteDao.insert_convite(grupo.id_grupo, destinatario.matricula):
            flash('Convite não enviado')
            return render_template('grupo/convidar.html')

        flash('Convite enviado com sucesso')
        return render_template('grupo/informacao.html')

    return render_template('grupo/convidar.html')
