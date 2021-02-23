from application import db, login
import werkzeug.security as security
import flask_login

import json
from json import JSONEncoder


class User(flask_login.UserMixin, db.Model):
    # статические константы для опредления классов
    ROLE_USER = 1
    ROLE_ADMIN = 2

    # поля класса
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.Integer)

    def is_admin(self):
        return self.role == User.ROLE_ADMIN

    def set_password(self, password):
        self.password_hash = security.generate_password_hash(password)

    def check_password(self, password):
        return security.check_password_hash(self.password_hash, password)

    @staticmethod
    def deseialize(usr_json):
        usr_dict = json.loads(usr_json)
        usr = User(
            usr_dict['id'],
            usr_dict['username'],
            usr_dict['password'],
            usr_dict['role']
        )
        return usr

    def serialize(self):
        return {
            "username": self.username,
            "role": self.role,
            "id": self.id
        }

    @staticmethod
    def init_json(json_str):
        usr = User.deseialize(json_str)
        return usr

    @staticmethod
    def init(self, id, username, password, role=ROLE_USER):
        usr = User(id,username,password,role)
        return usr

    def __repr__(self):
        return '<User {}>'.format(self.username)


class UserEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            return obj.serialize()
        return super().default(obj)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@login.request_loader
def load_user(request):
    token = request.headers.get('Authorization')
    if token is None:
        token = request.args.get('token')

    if token is not None:
        username, password = token.split(":")  # naive token
        user_entry = User.get(username)
        if (user_entry is not None):
            user = User(user_entry[0], user_entry[1])
            if (user.password == password):
                return user
    return None


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    body = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
