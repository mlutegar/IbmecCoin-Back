# utils.py
from flask import g


def validar_campos_transferencia(quantidade, destinatario):
    """
    Valida os campos do formulário de transferência.
    """
    if quantidade == "" or destinatario == "":
        return False, "Preencha todos os campos"
    elif not quantidade.isnumeric():
        return False, "Quantidade inválida"
    return True, ""


def obter_usuarios_transferencia(aluno_dao, remetente, destinatario):
    """
    Obtém os usuários remetente e destinatário do banco de dados.
    """
    remetente_usuario = aluno_dao.select_user_by_matricula(remetente)
    destinatario_usuario = aluno_dao.select_user_by_matricula(destinatario)
    if remetente_usuario == -1 or destinatario_usuario == -1:
        return None, None, "Usuário não encontrado"
    return remetente_usuario, destinatario_usuario, ""


def processar_transferencia(request, aluno_dao, transfer):
    """
    Processa a transferência de IbmecCoins.
    """
    quantidade = request.form['quantidade']
    remetente = g.user['matricula']
    destinatario = request.form['usuario']

    valido, mensagem = validar_campos_transferencia(quantidade, destinatario)
    if not valido:
        return False, mensagem

    remetente_usuario, destinatario_usuario, mensagem = obter_usuarios_transferencia(aluno_dao, remetente, destinatario)
    if remetente_usuario is None:
        return False, mensagem

    situacao, mensagem = transfer.transferir(int(quantidade), remetente_usuario, destinatario_usuario)
    return situacao, mensagem


def processar_grupo(request, aluno_dao, transfer):
    """
    Processa a criação de grupo para transferência de IbmecCoins.

    Parâmetros:
        request: objeto de solicitação contendo dados do formulário.
        aluno_dao: objeto de acesso ao banco de dados de alunos.
        transfer: objeto de transferência de IbmecCoins.

    Retorna:
        situacao (bool): indica se a operação foi bem-sucedida.
        mensagem (str): mensagem de feedback para o usuário.
    """
    nome_grupo = request.form.get('group_name')
    integrantes = request.form.get('members')
    remetente = g.user['matricula']

    if nome_grupo == "" or integrantes == "" or remetente == "":
        return False, "Preencha todos os campos"
    elif not integrantes.isnumeric():
        return False, "Número de integrantes inválido"

    remetente_usuario = aluno_dao.select_user_by_matricula(remetente)
    if remetente_usuario == -1:
        return False, "Usuário não encontrado"

    situacao, mensagem = transfer.criar_grupo(nome_grupo, remetente_usuario, int(integrantes))
    return situacao, mensagem


def invite_member(remetente, destinatario, grupo_id):
    """
    Envia um convite para um novo membro se juntar ao grupo.

    Parâmetros:
        remetente: o usuário que envia o convite.
        destinatario: o usuário que recebe o convite.
        grupo_id: o ID do grupo ao qual o usuário está sendo convidado.

    Retorna:
        situacao (bool): indica se a operação foi bem-sucedida.
        mensagem (str): mensagem de feedback para o usuário.
    """
    alunoDao = AlunoDao()

    # Verifica se o destinatário existe
    destinatario_usuario = alunoDao.select_user_by_matricula(destinatario)
    if destinatario_usuario == -1:
        return False, "Usuário destinatário não encontrado."

    # Envia o convite e define o status como 'pending'
    situacao = alunoDao.invite_to_group(remetente, destinatario, grupo_id)
    if not situacao:
        return False, "Falha ao enviar o convite."

    return True, "Convite enviado com sucesso."

def accept_invitation(usuario_id, grupo_id):
    """
    Aceita um convite para se juntar a um grupo.

    Parâmetros:
        usuario_id: o ID do usuário que está aceitando o convite.
        grupo_id: o ID do grupo ao qual o usuário está sendo convidado.

    Retorna:
        situacao (bool): indica se a operação foi bem-sucedida.
        mensagem (str): mensagem de feedback para o usuário.
    """
    alunoDao = AlunoDao()

    # Atualiza o status do convite para 'active'
    situacao = alunoDao.accept_group_invitation(usuario_id, grupo_id)
    if not situacao:
        return False, "Falha ao aceitar o convite."

    return True, "Convite aceito com sucesso."

