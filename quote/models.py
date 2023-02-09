from mongoengine import (CASCADE, BooleanField, DateTimeField, Document,
                         EmbeddedDocument, EmbeddedDocumentField, ListField,
                         ReferenceField, StringField)


class User(Document):
    user_name = StringField(max_length=50, required=True)
    first_name = StringField(max_length=50, required=True)
    last_name = StringField(max_length=50, required=True)
    password = StringField(max_length=100, required=True)
    email = StringField(max_length=50)
    phone_number = StringField(max_length=15, required=True)
    image = StringField(max_length=200, required=True)


class Post(Document):
    title = StringField(max_length=250, required=True)
    author = ReferenceField("User", reverse_delete_rule=CASCADE)
    content = StringField(max_length=5000)
    categories = ListField()
    image = StringField(max_length=200)
    status = BooleanField(required=True, default=True)
    pub_date = DateTimeField()
    likes = ListField()
    comments = ListField()
    tags = ListField()

    meta = {
        "auto_create_index": True,
        "index_background": True,
        "indexes": [
            {"name": "category", "fields": ("categories",)},
            {"name": "tag", "fields": ("tags",)},
        ],
    }


class Comment(Document):
    owner = ReferenceField("User", reverse_delete_rule=CASCADE)
    text = StringField(max_length=250)
    created_date = DateTimeField()


class Tag(Document):
    name = StringField(max_length=50)


class Category(Document):
    parent = StringField(max_length=50)
    children = ListField(max_length=5)
