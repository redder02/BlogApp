from flask import render_template, request, redirect, url_for, jsonify, session
from models.post import Post
from models.user import User
from models import db
from utils.decorators import jwt_token_required
from . import post_routes

@post_routes.route('/posts', methods=['GET'])
@jwt_token_required
def posts():
    current_user = session.get('username')
    user = User.query.filter_by(username=current_user).first()
    all_posts = Post.query.all()
    return render_template('posts.html', posts=all_posts, current_user=user)

@post_routes.route('/post/new', methods=['GET', 'POST'])
@jwt_token_required
def new_post():
    current_user = session.get('username')
    user = User.query.filter_by(username=current_user).first()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_post = Post(title=title, content=content, author=user)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('post.posts'))
    return render_template('new_post.html')

@post_routes.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@jwt_token_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    current_user = session.get('username')
    if post.author.username != current_user:
        return jsonify({"message": "You do not have permission to edit this post."}), 403
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        return redirect(url_for('post.posts'))
    return render_template('edit_post.html', post=post)

@post_routes.route('/post/<int:post_id>/delete', methods=['POST'])
@jwt_token_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    current_user = session.get('username')
    if post.author.username != current_user:
        return jsonify({"message": "You do not have permission to delete this post."}), 403
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('post.posts'))

# @post_routes.route('/post/<int:post_id>/like', methods=['POST'])
# @jwt_token_required
# def like_post(post_id):
#     post = Post.query.get_or_404(post_id)
    