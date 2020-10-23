from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models.auth.user import User


class LoginForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Re-Enter Password', validators=[
        DataRequired(), EqualTo('password')])
    submit = SubmitField('Register!')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('''Username already exists,
                please use a different one or reset your password here''')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('''Email is already registered,
                please reset your password here''')

# Password Reset Forms


class PasswordResetForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Re-Enter Password', validators=[
        DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password!')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password')


class EditProfileForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('last Name')
    email = StringField('Email', validators=[Email()])
    about_me = TextAreaField('Tell Us Something About You')
    submit = SubmitField('Update Profile')
    cancel = SubmitField('Cancel')
