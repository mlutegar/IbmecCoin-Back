from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.dao.aluno_dao import AlunoDao

bp = Blueprint('blog', __name__)

ad = AlunoDao()

@bp.route('/')
def index():
    posts = ad.get_all()
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            ad.insert(title, g.user['id'])
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id, check_author=True):
    post = ad.select(id)

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            ad.update(title, id)
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    ad.delete(id)
    return redirect(url_for('blog.index'))

# Função para vê o saldo do aluno
@bp.route('/saldo', methods=('GET', 'POST'))
@login_required
def saldo():
    saldoAluno = ad.get_saldo(g.user['id'])
    return render_template('blog/saldo.html', saldo=saldoAluno)
