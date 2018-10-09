from flask import jsonify, request, g, url_for, current_app
from . import api
from ..models import Post, Permission
from .decorators import permission_required
from .. import db
from .errors import forbidden


@api.route('/posts/')
def get_posts():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
                                     error_out=False)
    posts = pagination.items
    prev_page = None
    if pagination.has_prev:
        prev_page = url_for('api.get_posts', page=page-1, _external=True)
    next_page = None
    if pagination.has_next:
        next_page = url_for('api.get_posts', page=page+1, _external=True)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev_page,
        'next': next_page,
        'count': pagination.total
    })


@api.route('/posts/<int:post_id>')
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_json())


@api.route('/posts/', methods=['POST'])
@permission_required(Permission.WRITE_ARTICLES)
def new_post():
    post = Post.from_json(request.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json()), 201, {'Location': url_for('api.get_post', id=post.id, _external=True)}


@api.route('/posts/<int:post_id>', methods=['PUT'])
@permission_required(Permission.WRITE_ARTICLES)
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if g.current_user != post.author and \
       not g.current_user.can(Permission.ADMINISTER):
        return forbidden('Insufficient permission')
    post.body = request.json.get('body', post.body)
    db.session.add(post)
    return jsonify(post.to_json())
