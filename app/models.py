from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    """
    Creates User class
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, index=True)
    pass_secure = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    blogs = db.relationship('Blog', backref='user', lazy='dynamic')
    comments = db.relationship('Comments', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'User {self.username}'

    @property
    def password(self):
        """
        Function that blocks access to the password
        """
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_secure, password)


class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    title = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author = db.Column(db.String(255))
    date_posted = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    comments = db.relationship('Comments', backref='blog', lazy='dynamic')

    def save_blog(self):
        db.session.add(self)
        db.session.commit()

    def delete_blog(self):
        db.session.delete(self)
        db.session.commit()

    def update_blog(self):
        Blog.query.filter_by(id).update()
        db.session.commit()

    @classmethod
    def get_blogs(cls):
        blogs = Blog.query.all()
        return blogs


class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    blog_id = db.Column(db.Integer, db.ForeignKey("blogs.id"))
    description = db.Column(db.String(500))

    def save_comment(self):
        """
        Function that saves the comments made on a blog
        """
        db.session.add(self)
        db.session.commit()

    def delete_comment(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_comments(self, id):
        comment = Comments.query.filter_by(blog_id=id).all()
        return comment

    def __repr__(self):
        return f'Comment: {self.description}'


class Subscription(UserMixin, db.Model):
    __tablename__ = 'subs'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, index=True, nullable=False)

    def __repr__(self):
        return f'{self.email}'


class Quotes():
    def __init__(self, id, author, quote):
        self.id = id
        self.author = author
        self.quote = quote
