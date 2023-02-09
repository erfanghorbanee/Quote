import os

from flask import (Blueprint, current_app, flash, jsonify, redirect,
                   render_template, request, session, url_for)
from textblob import TextBlob
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from .categories import create_cats
from .database import get_db
from .models import Category, Comment, Post, Tag, User
from .Utils import random_post, reading_time

bp = Blueprint("blog", __name__)


@bp.route("/home/")
@bp.route("/")
def home():
    db = get_db()
    user = session
    posts = Post.objects(status=True)
    tags = Tag.objects()
    # Random post
    r_t = random_post()
    if r_t:
        return render_template(
            "blog/index.html",
            categories=create_cats(),
            user=user,
            posts=posts,
            tags=tags,
            rand_post=r_t,
        )
    return render_template(
        "blog/index.html", categories=create_cats(), user=user, posts=posts, tags=tags
    )


@bp.route("/post/<post_id>/")
def post(post_id):
    db = get_db()
    user = session
    post_details = Post.objects(id=post_id).first()

    # Detect language from title for setting text direction
    blobline = TextBlob(post_details.title)
    language = blobline.detect_language()

    return render_template(
        "blog/post.html",
        categories=create_cats(),
        post=post_details,
        user=user,
        reading_time=reading_time(post_details.content),
        language=language,
    )


@bp.route("/category-posts/<category_name>/")
def category(category_name):
    db = get_db()
    user = session
    posts = Post.objects(status=True)
    tags = Tag.objects()
    post_with_category = list()
    for item in posts:
        if category_name in item.categories[0].values():
            post_with_category.append(item)
    return render_template(
        "blog/posts_by_category.html",
        user=user,
        posts=post_with_category,
        categories=create_cats(),
        tags=tags,
    )


@bp.route("/posts-by-tag/<tag_name>/")
def post_by_tags(tag_name):
    db = get_db()
    user = session
    posts = Post.objects(status=True)
    post_obj = []
    tags = Tag.objects()

    for post in posts:
        for tag in post.tags:
            if str(tag.name) == (tag_name):
                post_obj.append(post)
    return render_template(
        "blog/posts_by_tag.html",
        user=user,
        posts=post_obj,
        categories=create_cats(),
        tags=tags,
    )


@bp.route("/tag-posts/<tag_id>", methods=["GET", "POST"])
def tag(tag_id):
    if request.method == "GET":
        db = get_db()
        posts = Post.objects(status=True)
        post_obj = []

        for post in posts:
            for tag in post.tags:
                if str(tag.id) == (tag_id):
                    # print(tag.id,"==", tag_id)
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


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        image = None
        user_name = request.form.get("user_name")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        password = request.form.get("password")
        email = request.form.get("email")
        phone_number = request.form.get("phone_number")
        file = request.files.get("profile_image")

        if file:
            file_name = secure_filename(file.filename)
            file_ext = os.path.splitext(file_name)[1]

            if file_ext not in current_app.config["UPLOAD_EXTENSIONS"]:
                flash(
                    "Your image must be one of these types: [.jpg, .png, .gif].",
                    "error",
                )
                return redirect(url_for("blog.register"))

            file.save("quote/static/images/profile_images/" + file_name)
            image = file_name

        db = get_db()
        username_exists = User.objects(user_name=user_name).first()

        if username_exists:
            flash("Username is already in use.", "error")
        else:
            new_user = User(
                user_name=user_name,
                first_name=first_name,
                last_name=last_name,
                password=generate_password_hash(password, method="sha256"),
                phone_number=phone_number,
                email=email,
                image=image,
            )

            new_user.save()

            return redirect(url_for("blog.login"))

    return render_template("user/register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        password = request.form.get("password")
        user_name = request.form.get("user_name")
        db = get_db()
        user = User.objects(user_name=user_name).first()

        # Check if user exists with this  username.
        if user:
            if check_password_hash(user["password"], password):

                session.clear()
                session["first_name"] = user.first_name
                session["user_id"] = str(user.id)
                session["profile_image"] = user.image

                return redirect(url_for("blog.home"))
            else:
                flash("Password is incorrect.", "error")

        else:
            flash("Username does not exist.", "error")

    return render_template("user/login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("blog.home"))
