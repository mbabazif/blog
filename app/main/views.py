from flask import render_template, request, redirect, url_for, abort
from . import main
from flask_login import login_required, current_user
from .. import db, photos
from ..models import User, Blog, Comments, Subscription
from .forms import PitchForm, CommentForm, UpdateProfile, SubscribeForm
from app.email import mail_message


@main.route('/')
def home():
    """
    Renders the home page
    """
    title = "Welcome | Florence blog"

    return render_template('home.html', title=title)


@main.route('/index')
@login_required
def index():
    """
    View blogs 
    """
    blogs = Blog.query.all()
    if blogs is None:
        abort(404)
    return render_template('index.html', blogs=blogs)


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username=uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user)


@main.route('/user/<uname>/update', methods=['GET', 'POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile', uname=user.username))

    return render_template('profile/update.html', form=form)


@main.route('/user/<uname>/update/pic', methods=['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username=uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile', uname=uname))


@main.route('/blog/new-blog/', methods=['GET', 'POST'])
@login_required
def new_blog():
    """
    Function that enables one to start a blog
    """
    form = PitchForm()

    if form.validate_on_submit():
        content = form.content.data
        title = form.title.data
        author = form.author.data
        new_blog = Blog(
            content=content,
            title=title,
            author=author,
            user_id=current_user.id)
        new_blog.save_blog()
        subs = Subscription.query.all()
        for sub in subs:
            mail_message("New Blog", "email/new_blog", sub.email)
        return redirect(url_for('main.index'))
    return render_template('new-blog.html', form=form)


@main.route('/view-blog/<int:id>', methods=['GET', 'POST'])
@login_required
def view_blog(id):
    """
    Returns the blog to be commented on
    """
    print(id)
    blogs = Blog.query.get(id)
    comments = Comments.get_comments(id)
    return render_template('view.html', blogs=blogs, comments=comments, id=id)


@main.route('/delete-blog/<int:id>', methods=['GET', 'POST'])
@login_required
def del_blog(id):
    """
    Function that enables one to delete a blog post
    """
    blog = Blog.query.get_or_404(id)
    if blog.user_id != current_user.id:
        abort(403)
    blog.delete_blog()
    return redirect(url_for('main.index'))


@main.route('/comment/<int:id>', methods=['GET', 'POST'])
@login_required
def blog_comment(id):
    """
    Function to post joke comments on specific joke
    """
    form = CommentForm()
    blogs = Blog.query.filter_by(id=id).first()
    if form.validate_on_submit():
        description = form.description.data
        new_comment = Comments(
            description=description, user_id=current_user.id, blog_id=blogs.id)
        new_comment.save_comment()
        return redirect(url_for('.index', id=blogs.id))
    return render_template('comments.html', form=form, blogs=blogs)


@main.route('/del-comment/<int:id>', methods=['GET', 'POST'])
@login_required
def del_comment(id):
    """
    Function that enables one to delete a comment made on their blog
    """
    comment = Comments.query.get_or_404(id)
    if comment.user_id != current_user.id:
        abort(403)
    comment.delete_comment()
    return redirect(url_for('.index'))


@main.route('/subscribe/', methods=['GET', 'POST'])
@login_required
def sub():
    """
    Function that enables one to subscribe to the blog
    """
    form = SubscribeForm()
    if form.validate_on_submit():
        subscription = Subscription(email=form.email.data)
        db.session.add(subscription)
        db.session.commit()
        return redirect(url_for('main.index'))

    return render_template('sub.html', form=form)
