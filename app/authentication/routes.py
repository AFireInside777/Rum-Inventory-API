from flask import Blueprint, render_template, flash, redirect, request, url_for
from models import User, db
from forms import UserLoginForm
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():

    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            user = User(email, password=password)

            db.session.add(user)
            db.session.commit()

            # currentUsers = User.query.all()
            # for user in currentUsers:
            #     print(user.email)

            flash(f'You have successfully created a user account for {email}. You may log in.') #this does not show in the browser -->3-6-2024, this is because there is HTML that has to be written as well.
            return redirect(url_for('site.home'))
    except:
        raise Exception('Invalid form data: Please check your form.')
    return render_template('signup.html', form=form)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                return redirect(url_for('site.profile'))
            else:
                flash('You have failed in your attempt to access this content.', 'auth-failed')
    except:
        raise Exception('Invalid form data: Please check your form.')
    return render_template('login.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.home'))