# -*- coding: utf-8 -*-
from flask import *

from flask_login import current_user, login_user ,logout_user, login_required
from application.models import User
import application.forms as Forms
from application import app, db

from flask import request
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required
def index():

    return render_template('index.html', user=current_user, title='Home Page')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = Forms.LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = Forms.RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, role=User.ROLE_USER)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/admin')
@login_required
def admin():
    return redirect(url_for('admin'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))