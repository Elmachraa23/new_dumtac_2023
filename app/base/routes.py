from flask import redirect, request, url_for, render_template
from flask_login import current_user, login_user, login_required, logout_user

import logging

from app import db
from app.base import blueprint
from app.base.forms import SigninForm
from app.base.models import User


@blueprint.route('/')
def route_default():
    return redirect(url_for('site_blueprint.route_landing'))


@blueprint.route('/page_<error>')
def route_errors(error):
    return render_template('errors/page_{}.html'.format(error))


@blueprint.before_app_request
def last_seen_updater():
    if current_user.is_authenticated:
        current_user.last_seen = db.func.now()
        db.session.commit()


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SigninForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form._user.email).first()
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    else:
        logging.info(f'Failed login attempt {request.remote_addr} : {form.email.data}')
    return render_template('login.html', form=form)


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('base_blueprint.signin_view'))