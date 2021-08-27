from flask import Blueprint, session, url_for, redirect, request, jsonify, flash
from datetime import datetime
from .models import User, Comment, Post, Tag
from .database import get_db

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route('/create_comment/', methods=['POST'])
def create_comment():
    if request.method == 'POST':
        db = get_db()
        comment = request.form.get('comment')
        post_id = request.form.get('postId')
        user_id = request.form.get('userId')

        post = Post.objects(id=post_id).first()

        # Create a comment
        user = User.objects(id=user_id).first()
        new_comment = Comment(owner=user, text=comment, created_date=datetime.now())
        new_comment.save()

        post.comments.append(new_comment)
        post.save()
        return jsonify(comment)


@bp.route('/post-delete/<post_id>/', methods=['POST'])
def post_delete(post_id):
    if request.method == "POST":
        db = get_db()
        post = Post.objects(id=post_id).first()
        print(post_id)
        post.delete()
        return "OK"


@bp.route('/post_deactivate/<post_id>/', methods=['POST'])
def post_deactivate(post_id):
    if request.method == "POST":
        db = get_db()
        print(post_id)
        post = Post.objects(id=post_id).first()
        print(post.status)
        # print(post_id)
        if post.status:
            post.status = False
            post.save()
            print(post.status)
            return 'Deactivated'
        else:
            post.status = True
            post.save()
            print(post.status)

            return "Activated"
        # return f'OK'


@bp.route('/tags/', methods=['GET', 'POST'])
def tags():
    if request.method == 'GET':
        db = get_db()
        obj = []
        tags = Tag.objects()

        for item in tags:
            item = item.to_mongo().to_dict()
            del item["_id"]
            obj.append(item)

        return jsonify(obj)


@bp.route('/like/', methods=['GET', 'POST'])
def like():
    if request.method == "POST":
        db = get_db()

        # Get data from ajax
        data = request.get_data(as_text=True).split('&')
        # User id who liked the post
        user_id_from_ajax = data[0].split('=')[1]
        # Post id which is user liked
        post_id_from_ajax = data[1].split('=')[1]

        # Get user from database
        user = User.objects(id=user_id_from_ajax).first()
        # Get post from database
        post = Post.objects(id=post_id_from_ajax).first()

        if user in post.likes:
            post.likes.remove(user)
            post.save()
            # print('Bud pak kardam.')
            return 'Deleted'
        else:
            post.likes.append(user)
            post.save()
            # print('NaBud ezafe kardam.')
            return 'Added'


@bp.route('/search/<title>/', methods=['GET', 'POST'])
def search(title):

    if request.method == 'GET':
        db = get_db()
        posts = Post.objects(title=title)
        post_obj = []

        for post in posts:
            if str(post.title) == (title):
                post = post.to_mongo().to_dict()
                del post["categories"]
                del post["likes"]
                del post["comments"]
                del post["tags"]
                del post["author"]
                post["_id"] = str(post["_id"])
                post_obj.append(post)

        print(post_obj)
        return jsonify(post_obj)
