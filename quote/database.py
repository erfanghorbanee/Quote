from flask import g
from mongoengine import connect


def get_db():

    if "db" not in g:
        g.db = connect("blog")

    return g.db
