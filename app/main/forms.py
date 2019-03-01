from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import Required, Email, EqualTo, ValidationError
from wtforms import ValidationError
from ..models import Subscription


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.', validators=[Required()])
    submit = SubmitField('Submit')


class PitchForm(FlaskForm):
    title = StringField('Title', validators=[Required()])
    author = TextAreaField("Who is the author?", validators=[Required()])
    content = TextAreaField(
        "What is your blog about?", validators=[Required()])
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    description = TextAreaField('Add comment', validators=[Required()])
    submit = SubmitField()


class SubscribeForm(FlaskForm):
    email = StringField('Email address', validators=[Required(), Email()])
    submit = SubmitField('Subscribe')

    def validate_email(self, email):
        email = Subscription.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError(
                'That email is already subscribed to our emailing list.')
