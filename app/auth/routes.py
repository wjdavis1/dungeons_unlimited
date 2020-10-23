from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, EditProfileForm
from app.auth.forms import PasswordResetForm, PasswordResetRequestForm
from app.models.auth.user import User
from app.auth.email import password_reset_email


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('''Invalid Login Information,
                Please Verify Your Input and Try Again!''')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congrats, you are now registered')
        return redirect(url_for('auth.login'))
    if len(form.errors.items()) > 0:
        for field_name, error_message in form.errors.items():
            print('{} : {}'.format(field_name, error_message))
            flash('{}'.format(error_message))
    return render_template('registration.html', title='Register', form=form)


@bp.route('/password_reset_request', methods=['GET', 'POST'])
def password_reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            password_reset_email(user)
        flash('Check Your email registered for password reset instructions!')
        return redirect(url_for('auth.login'))
    return render_template(
        'reset_password_request.html',
        title='Reset Password',
        form=form)


@bp.route('/password_reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been successfully reset!')
        return redirect(url_for('auth.login'))
    return render_template('reset_password.html', form=form)


@bp.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():

    form = EditProfileForm()
    if form.cancel.data:
        return redirect(url_for('main.index'))
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user is not None:
            flash('The email entered is already on record, please verify your email address')
            return render_template('edit_profile.html', title='Edit Profile', form=form)
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your profile information has been updated!')
    return render_template('edit_profile.html', title='Edit Profile', form=form)
