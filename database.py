from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta
from flask.helpers import flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import path

from werkzeug.security import generate_password_hash, \
    check_password_hash

# import mysql.connector
# from mysql.connector import errorcode


app = Flask(_name_)
app.config["SECRET_KEY"] = "my-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://chuong:chuong@localhost/test"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=1)

db = SQLAlchemy(app)


# db.app = app

class User(db.Model):
    # _tablename_ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(300), nullable=False)
    bio = db.Column(db.String(100))
    avatar = db.Column(db.String(1014))
    rank_id = db.Column(db.Integer)
    user_rela = db.relationship('States', backref=db.backref('user', lazy=True))

    def __init__(self, user_name, email, password, bio, avatar=0, rank_id=0):
        self.user_name = user_name
        self.email = email
        self.password = generate_password_hash(password)
        self.bio = bio
        self.avatar = avatar
        self.rank_id = rank_id

    def check_password(self, password_hash):
        return check_password_hash(self.password, password_hash)


class States(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    blog_id = db.Column(db.Integer, db.ForeignKey('blog_post.id'))
    comment = db.Column(db.String(1014))


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_cover = db.Column(db.String(1014))
    date = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.String(1014), nullable=False)
    subtitle = db.Column(db.String(1014))
    body = db.Column(db.String(10845), nullable=False)
    BlogPost_rela = db.relationship('States', backref=db.backref('BlogPost', lazy=True))


with app.app_context():
    if not path.exists("user.db"):
        db.create_all()
        print("Created database!")


@app.route('/select/user')
def select():
    # data_user = User.query.filter_by(user_name='chuong').first()
    users = User.query.all()
    html = '';
    for user in users:
        html = html + "<br>" + user.user_name;

    return html


@app.route('/insert', methods=["GET"])
def insert_test():
    new_user = User('username1', 'havanchuong@gmail.com', '12345678', 'bio');
    db.session.add(new_user)
    db.session.commit()
    return 'Da insert du lieu'


@app.route('/test_checkpass')
def check_pass():
    # s = Session();
    user = User.query.filter_by(user_name='username1').first()
    if user:
        if user.check_password('12345678') == True:
            return "mat khau dung"
        else:
            return 'sai'
    else:
        return 'khong co username như v'