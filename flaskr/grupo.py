from flask import Blueprint, render_template, request, flash, session
from flaskr.dao.aluno_dao import AlunoDAO
from flaskr.dao.convite_dao import ConviteDAO
from flaskr.dao.grupo_dao import GrupoDAO
from flaskr.dao.transacao_dao import TransacaoDAO

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
    id_grupo = aluno.get_id_grupo()
    grupoDao = GrupoDAO()
    grupo = grupoDao.get_grupo_by_id(id_grupo)

    return render_template('grupo/informacao.html', grupo=grupo, aluno=aluno)


@bp.route('/criar', methods=('GET', 'POST'))
def criar():
    """
    Função que exibe a página de criação de grupo.
    """
    if 'matricula' not in session:
        return render_template('index.html')
    matricula = session['matricula']

    aluno = AlunoDAO().get_aluno(matricula)
    grupoDao = GrupoDAO()

    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']

        if not grupoDao.insert_grupo(nome, 5, descricao, aluno.matricula):
            error = 'Grupo já existe.'
            flash(error)
            return render_template('grupo/criar.html')
        else:
            flash('Grupo criado com sucesso')
            aluno.id_grupo = grupoDao.get_grupo_by_matricula(aluno.matricula).id_grupo

            if not AlunoDAO().update_aluno(aluno):
                flash('Erro ao atualizar aluno')
                return render_template('grupo/criar.html')

            return render_template(
                'grupo/informacao.html',
                grupo=grupoDao.get_grupo_by_matricula(aluno.matricula),
                aluno=aluno
            )

    return render_template('grupo/criar.html')


@bp.route('/transferir/<destinatario>', methods=('GET', 'POST'))
def transferir(destinatario):
    """
    Função que exibe a página de transferência de IbmecCoins.
    Essa função também é responsável por processar o post do formulário de transferência de IbmecCoins.
    """
    if 'matricula' not in session:
        return render_template('index.html')

    matricula = session['matricula']
    remetente = AlunoDAO().get_aluno(matricula)

    if request.method == 'POST':
        destinatario = request.form['usuario']
        quantidade = request.form['quantidade']

        destinatario = AlunoDAO().get_aluno(destinatario)
        quantidade = int(quantidade)

        if destinatario is None or quantidade == "":
            flash('Usuário não encontrado')
            return render_template('grupo/transferir.html')

        if not TransacaoDAO().insert_transacao(remetente.matricula, destinatario.matricula, quantidade):
            flash('Não foi possível processar a transferência')
            return render_template('grupo/transferir.html')

        flash('Transferência realizada com sucesso')
        return render_template(
            'grupo/informacao.html',
            aluno=remetente,
            grupo=GrupoDAO().get_grupo_by_id(remetente.get_id_grupo())
        )

    return render_template('grupo/transferir.html', destinatario=destinatario)


@bp.route('/convidar', methods=('GET', 'POST'))
def convidar():
    """
    Função que exibe a página de convite de alunos para o grupo.
    """
    if 'matricula' not in session:
        return render_template('index.html')
    matricula = session['matricula']

    alunoDao = AlunoDAO()
    grupoDao = GrupoDAO()
    conviteDao = ConviteDAO()
    remetente = alunoDao.get_aluno(matricula)
    grupo = grupoDao.get_grupo_by_id(remetente.get_id_grupo())

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
        return render_template('grupo/informacao.html', grupo=grupo, aluno=remetente)

    return render_template('grupo/convidar.html')


@bp.route('/convites', methods=('GET', 'POST'))
def convites():
    """
    Função que exibe a página de convites recebidos.
    """
    if 'matricula' not in session:
        return render_template('index.html')
    matricula = session['matricula']
    
    aluno = AlunoDAO().get_user(matricula)
    convites_lista = ConviteDAO().get_all_convites_by_matricula(aluno.matricula)

    return render_template('grupo/convites.html', convites=convites_lista, aluno=aluno)


@bp.route('/aceitar/<id_convite>', methods=('GET', 'POST'))
def aceitar(id_convite):
    """
    Função que aceita um convite de um grupo.
    """
    if 'matricula' not in session:
        return render_template('index.html')
    matricula = session['matricula']

    user = AlunoDAO().get_aluno(matricula)
    convite = ConviteDAO().get_convite(id_convite)

    if convite is None:
        flash('Convite não encontrado')
        return render_template('grupo/convites.html')

    if AlunoDAO().aceitar_convite(convite.id_grupo, convite.convidado_matricula):
        flash('Convite aceito com sucesso')
        grupo = GrupoDAO().get_grupo_by_id(convite.id_grupo)
        user.id_grupo = grupo.id_grupo
        AlunoDAO().update_aluno(user)
        ConviteDAO().delete_convite(convite.id_convite)

        return render_template('grupo/informacao.html', grupo=grupo, aluno=user)

    return render_template('grupo/aceitar.html', id_convite=id_convite)
