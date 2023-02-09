from flask import Flask


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
        app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
        app.config["UPLOAD_EXTENSIONS"] = [".jpg", ".png", ".gif"]

    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists

    # register the database commands

    from . import api, blog, user

    # register the blueprints
    app.register_blueprint(blog.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(api.bp)

    return app
