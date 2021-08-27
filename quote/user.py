from flask import Blueprint, render_template, session, redirect, url_for, request, flash, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from .categories import create_cats
from werkzeug.utils import secure_filename
from .models import User, Post, Tag
from .database import get_db
from datetime import datetime
import os

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route('/profile/', methods=['GET', 'POST'])
def profile():
    if request.method == 'GET':

        if session is None:
            return redirect(url_for('blog.login'))
        else:
            db = get_db()
            user = User.objects(id=session['user_id']).first()
            return render_template("user/profile.html", user=user)

    db = get_db()
    new_password = request.form.get('password')
    user = User.objects(id=session['user_id']).first()
    user.password = generate_password_hash(new_password, method='sha256')
    user.save()
    return redirect(url_for('user.profile'))


@bp.route('/posts-list/')
def posts_list():
    if session:
        db = get_db()
        user_id = session["user_id"]
        first_name = session["first_name"]
        user_posts = Post.objects(author=user_id)
        return render_template("user/dashboard.html", user_posts=user_posts, first_name=first_name)


@bp.route('/create-post/', methods=['GET', 'POST'])
def create_post():
    if session:

        if request.method == 'POST':
            title = request.form.get("title")
            author = session['user_id']
            content = request.form.get("the-textarea")
            categories = request.form.get("category")
            status = True
            pub_date = datetime.now()
            tags = request.form.get("new_tag")
            tags = tags[0:len(tags) - 1].split(" ")
            tags = list(set(tags))
            file = request.files.get('image')

            if len(tags) > 6:
                flash('You can only choose 6 tags, Please try again.', 'error')
                return redirect(url_for('user.create_post'))

            if file:
                file_name = secure_filename(file.filename)
                file_ext = os.path.splitext(file_name)[1]

                if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:
                    flash('Your image must be one of these types: [.jpg, .png, .gif].', 'error')
                    return redirect(url_for('user.create_post'))

                file.save('quote/static/images/posts_images/' + file_name)
                image = file_name

            db = get_db()

            db_tag_names = []
            db_tag_obj = Tag.objects()
            all_new_tags = []

            for item in db_tag_obj:
                db_tag_names.append(item.name)

            for tag in tags:

                if tag not in db_tag_names:
                    new_tag = Tag(
                        name=tag
                    )
                    new_tag.save()
                    all_new_tags.append(new_tag)
                else:
                    tag_existed = Tag.objects(name=tag).first()
                    all_new_tags.append(tag_existed)

            new_post = Post(
                title=title,
                author=author,
                content=content,
                categories=[{"children": categories}],
                status=status,
                tags=list(set(all_new_tags)),
                pub_date=pub_date,
                image=image
            )
            new_post.save()

            return redirect(url_for('blog.home'))

        return render_template("user/create_post.html", categories=create_cats())

    else:
        return redirect(url_for('blog.login'))


@bp.route('/edit-post/<post_id>/', methods=['GET', 'POST'])
def edit_post(post_id):
    if session:
        post = Post.objects(id=post_id).first()
        if request.method == 'POST':
            title = request.form.get("title")
            content = request.form.get("erfan")

            tags = request.form.get("new_tag")
            tags = tags[0:len(tags) - 1].split(" ")
            tags = list(set(tags))

            if len(tags) > 6:
                # flash('You can only choose 6 tags, Please try again.', 'error')
                return redirect(url_for('user.posts_list'))

            db = get_db()

            db_tag_names = []
            db_tag_obj = Tag.objects()
            all_new_tags = []

            for item in db_tag_obj:
                db_tag_names.append(item.name)

            for tag in tags:

                if tag not in db_tag_names:
                    new_tag = Tag(
                        name=tag
                    )
                    new_tag.save()
                    all_new_tags.append(new_tag)
                else:
                    tag_existed = Tag.objects(name=tag).first()
                    all_new_tags.append(tag_existed)

            post.content = content
            post.title = title
            # Using set for removing repetitious tags
            post.tags = list(set(all_new_tags))
            post.save()

            return redirect(url_for('blog.home'))

        return render_template("user/edit_post.html", categories=create_cats(), post=post)

    else:
        return redirect(url_for('blog.login'))


@bp.route('/change_password/', methods=['POST'])
def change_password():
    if session is None:
        return redirect(url_for('blog.login'))

    db = get_db()
    old_password = request.form.get('old_password')
    new_password = request.form.get('password')
    user = User.objects(id=session['user_id']).first()
    if check_password_hash(user["password"], old_password):
        user.password = generate_password_hash(new_password, method='sha256')
        user.save()
        flash('Your password successfully changed.')
        return redirect(url_for('user.profile'))

    flash('Your old password is incorrect.', 'error')
    return redirect(url_for('user.profile'))
