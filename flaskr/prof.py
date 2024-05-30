"""
Módulo que contém as funções relacionadas as ações de professor.
- A rota /transferencias: exibe a página de transferências de todas as transferências dos alunos.
- A rota /transferencias/<id>: exibe a página de transferências de um aluno específico.
- A rota /beneficiar: exibe a página de beneficiar um aluno.
- A rota /adicionar-loja: exibe a página de adicionar uma loja.
"""

from flask import Blueprint, render_template, flash, request

from flaskr.dao.aluno_dao import AlunoDao
from flaskr.dao.transferencia_dao import TransferenciaDao

bp = Blueprint('prof', __name__, url_prefix='/prof')

def get_all_alunos():
    """
    Função que retorna todos os alunos do banco de dados.
    :return: retorna todos os alunos do banco de dados
    """
    alunoDao = AlunoDao()
    alunos, mensagem = alunoDao.get_all_user_alunos()
    return alunos, mensagem

@bp.route('/beneficiar', methods=('GET', 'POST'))
def beneficiar():
    """
    Função que exibe a página de beneficiar um aluno.
    Essa função também é responsável por processar o post do formulário de beneficiar um aluno.
    Ele pega o valor "quantidade" e o valor "usuario" do formulario, verifica se eles estão vazios ou não e se
    a quantidade é um número válido. Se tudo estiver correto, ele chama a função creditar_saldo de AlunoDao e passa os
    valores como parâmetros.
    :return: renderiza a página de beneficiar um aluno
    """
    alunoDao = AlunoDao()

    if request.method == 'POST':
        quantidade = request.form['quantidade']
        matricula = request.form['usuario']

        if quantidade == "" or matricula == "":
            flash("Preencha todos os campos")
            return render_template('prof/beneficiar.html')
        elif not quantidade.isnumeric():
            flash("Quantidade inválida")

        aluno = alunoDao.get_aluno_by_matricula(matricula)

        if aluno == -1:
            flash("Usuário não encontrado")
            return render_template('prof/beneficiar.html')

        alunoDao.creditar_saldo(matricula, int(quantidade))
        flash("Aluno beneficiado com sucesso")

    alunos, mensagem = get_all_alunos()
    flash(mensagem)

    return render_template('prof/beneficiar.html', alunos=alunos)

@bp.route('/transferencias', methods=('GET', 'POST'))
def transferencias():
    """
    Função que exibe a página de transferências de todas as transferências dos alunos.
    :return: renderiza a página de transferências de todas as transferências dos alunos
    """
    transfer = TransferenciaDao()
    transferencias, mensagem = transfer.get_all_transacoes()

    if transferencias == []:
        flash(mensagem)
        return render_template('prof/transferencias.html')

    flash(mensagem)
    return render_template('prof/transferencias.html', transferencias=transferencias)